#! /bin/sh
###
## script will reside at the ssh_stag-php-billing1 server it self
# ssh -i ~/.ssh/id_rsa ubuntu@stag-workstation.generico.in
# ssh_stag-php-billing1
###
# echo "enter snapshot year-month(eg. 2021-04).?"
# read -r year_month
#year_month=$year_month
echo "start time: $(date)"
year_month="2021-09"
#echo "snapshot to be restored: prod2-$year_month-06-02-00-generico.sql.gz"

# shellcheck disable=SC2164
# go to vol3 because snapshots are big files
#cd /vol3/database/

# switch to super doer(sudo)
# sudo  su

# Download the snapshot from s3 to database folder

snapshot_name=prod2-"$year_month"-01-02-00-generico.sql
s3cmd get s3://prod-generico-storage/mysql/"$snapshot_name".gz
echo "S3 Download done at: $(date)"

# extracting the zip
#zcat "$snapshot_name".gz > "$snapshot_name"

# replacing the prod2-generico DB with yearmonth-generico
# shellcheck disable=SC2039

plain_year_month=$(echo "$year_month" | sed 's:[!@#$%^&*()=-]::g')
echo "$plain_year_month"
#sed -i "s#prod2\-generico#'$plain_year_month'\-generico#" "$snapshot_name"

# split the dump for specific tables
# shellcheck disable=SC2006
echo "Start: table spliting"
sh mysqldumpsplitter.sh --source "$snapshot_name".gz --extract DBTABLE --match_str "prod2-generico.(inventory|invoices|drugs|invoice-items|stores|distributors|store-dc-mapping|inventory-1|invoice-items-1|return-items|returns-to-dc|debit-notes)" --decompression gzip --compression none --output_dir ./out/tables/"$plain_year_month"/
echo "End: table spliting at: $(date)"

db_password="dev-server"
db_name="generico_$plain_year_month"
echo "$db_name", "$db_password"

mysql -u admin -h stag-mysql.cdaq46oaug4x.ap-south-1.rds.amazonaws.com -p"$db_password" -e "drop database IF EXISTS $db_name;"
mysql -u admin -h stag-mysql.cdaq46oaug4x.ap-south-1.rds.amazonaws.com -p"$db_password" -e "create database IF NOT EXISTS $db_name;"

# mysql -u server -p"$db_password" -e "drop database IF EXISTS $db_name;"
# mysql -u server -p"$db_password" -e "create database IF NOT EXISTS $db_name;"

# import all the tables
echo "Start: table import to DB"
for filename in ./out/tables/"$plain_year_month"/*.sql; do
   echo "$filename start at: $(date)"
   mysql -u admin -h stag-mysql.cdaq46oaug4x.ap-south-1.rds.amazonaws.com -p"$db_password" "$db_name" < "$filename"
   # mysql -u server -p"$db_password" "$db_name" < "$filename"
done
