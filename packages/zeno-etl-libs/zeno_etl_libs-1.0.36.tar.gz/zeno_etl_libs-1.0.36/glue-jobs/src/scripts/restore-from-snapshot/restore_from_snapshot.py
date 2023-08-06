import argparse
import sys
import os
import boto3
import time

from zeno_etl_libs.helper import helper

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-ss', '--source_schema_name', default="prod2-generico", type=str, required=False)
parser.add_argument('-ts', '--target_schema_name', default="public", type=str, required=False)
parser.add_argument('-lt', '--list_of_tables', default=None, type=str, required=False)
parser.add_argument('-et', '--email_to', default="kuldeep.singh@zeno.health", type=str, required=False)
parser.add_argument('-si', '--snapshot_identifier', default=None, type=str, required=False)
parser.add_argument('-re', '--reason_code', default="na", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

logger = get_logger()
logger.info(f"env: {env}")

source_schema_name = args.source_schema_name
list_of_tables = args.list_of_tables
email_to = args.email_to
reason_code = args.reason_code

snapshot_identifier = args.snapshot_identifier
snapshot_date = snapshot_identifier[-19:-9]
logger.info(f"snapshot_date: {snapshot_date}")

target_schema_name = args.target_schema_name
# target_schema_name = f"snap-{snapshot_date}"

logger.info(f"source_schema_name: {source_schema_name}")
logger.info(f"target_schema_name: {target_schema_name}")
logger.info(f"list_of_tables: {list_of_tables}")
logger.info(f"email_to: {email_to}")
logger.info(f"snapshot_identifier: {snapshot_identifier}")
logger.info(f"reason_code: {reason_code}")

if snapshot_identifier is None:
    raise Exception("Please provide proper snapshot identifier")

if not list_of_tables:
    raise Exception("Please provide list of tables")

if env == 'prod':
    source_database_name = 'prod2-generico'
    cluster_identifier = 'prod-mysql-redshift-cluster-1'
else:
    source_database_name = 'dev'
    cluster_identifier = 'stag-mysql-redshift-cluster-1'

""" since we have single database in redshift so keeping source and target db same """
target_database_name = source_database_name


list_of_tables = list_of_tables.split(",")
client = boto3.client('redshift')
email = Email()

rs_db = DB(read_only=False)
rs_db.open_connection()

# """ create target schema before restoring """
# query = f"""
# CREATE SCHEMA IF NOT EXISTS  "{target_schema_name}"
# """
# rs_db.execute(query=query)

success_tables_list = []
failed_tables_list = []

for i in list_of_tables:
    logger.info(f"started table: {i}")
    new_table_name = i + '-' + str(reason_code) +'-' + str(snapshot_date)
    # new_table_name = i

    table_info = helper.get_table_info(db=rs_db, table_name=new_table_name, schema=target_schema_name)
    if isinstance(table_info, type(None)):
        logger.info(f"Table: {new_table_name} is absent.")
    else:
        success_tables_list.append(i)
        logger.info(f"Table already exists: {new_table_name}, moving to next table")
        table_restore_status = "Already Present"
        email.send_email_file(
            subject=f"[Table Restoration], Table: {i}, Status: {table_restore_status}",
            mail_body=f"Status: {table_restore_status} \nTable: {i} \nSnapshot Date: {snapshot_date} \nCluster Identifier: {cluster_identifier} \nMessage: None",
            to_emails=email_to, file_uris=[], file_paths=[])
        continue

    response = client.restore_table_from_cluster_snapshot(
        ClusterIdentifier=cluster_identifier,
        SnapshotIdentifier=snapshot_identifier,
        SourceDatabaseName=source_database_name,
        SourceSchemaName=source_schema_name,
        SourceTableName=i,
        TargetDatabaseName=target_database_name,
        TargetSchemaName=target_schema_name,
        NewTableName=new_table_name
    )
    logger.info(f"response: {response}")
    table_restore_status = response['TableRestoreStatus']['Status']
    table_restore_request_id = response['TableRestoreStatus']['TableRestoreRequestId']
    message = ""
    while table_restore_status not in ('SUCCEEDED', 'FAILED', 'CANCELED'):
        time.sleep(60)
        response = client.describe_table_restore_status(
            ClusterIdentifier=cluster_identifier,
            TableRestoreRequestId=table_restore_request_id,
            MaxRecords=20
        )
        for r in response['TableRestoreStatusDetails']:
            table_restore_status = r['Status']
            logger.info(f"Status: {r['Status']}")
            message = r.get("Message")

    if table_restore_status == 'SUCCEEDED':
        success_tables_list.append(i)
    else:
        failed_tables_list.append(i)

    email.send_email_file(
        subject=f"[Table Restoration], Table: {i}, Status: {table_restore_status}",
        mail_body=f"Status: {table_restore_status} \nTable: {i} \nSnapshot Date: {snapshot_date} \nCluster Identifier: {cluster_identifier} \nMessage:{message}",
        to_emails=email_to, file_uris=[], file_paths=[])

email.send_email_file(
    subject=f"[Table Restoration], Full Status: Success-{len(success_tables_list)}, Failed-{len(failed_tables_list)}",
    mail_body=f"Table succesfully restored: {success_tables_list} \nTable restore failed: {failed_tables_list} \nSnapshot Date: {snapshot_date} \nCluster Identifier: {cluster_identifier}",
    to_emails=email_to, file_uris=[], file_paths=[])