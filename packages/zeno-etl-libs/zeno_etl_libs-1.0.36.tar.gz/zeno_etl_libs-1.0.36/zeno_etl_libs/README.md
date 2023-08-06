# Zeno Etl Libs custom library 
Custom library holds all the helper functions that are commonly utilized across the entire project.

## config:
- Holds a common.py file, which is being utilized to get the secrets from AWS secrets manager.

## db: 
- Holds a db.py, which holds up the connections and various related functions for various databases such as MySQL,
- Redshift, MSSQL and PostgreSQL, MongoDB.
- Various functions in db.py include starting of connections, executing of certain user queries and ultimately close of
- the connections.

## django
- This particular folder holds an api.py file, which in turn helps in Django integration via APIs.

## helper
- This folder holds multiple.py files to help with the execution of main job scripts

### 1. aws
- This sub folder contains a s3.py files, which basically lets user do s3 operations from a glue or sagemaker job,
- such as save a file to s3, download a specific file from s3 etc.

### 2. clevertap
- This folder contains a .py file with name clevertap.py, the basic functions within this .py file helps one to
- effectively run clevertap job by using clevertap API.

### 3. disprz
- This folder holds disprz.py, which just like the clevertap, helps jobs related to lnd-ma-disprz via API.

### 4. email
- this folder holds email.py, which basically allows user to send out a specific file from s3 as a mail attachment,
- this .py file can be used to send out error logs as well as output files as email attachment.

### 5. fresh_service
- This folder contains a .py file which helps in the execution of freshservice job, this .py file contains the API.

### 6. google
- This folder holds 2 folders, related to google API, the use case is as follows -- 

#### i. playstore
- This folder holds a .py file named playstore.py, this .py helps with connecting with google playstore and getting the
- reviews from playstore.

#### ii. sheet
- This folder contains a sheet.py file, which helps user to download or upload data to a Google sheet.

### 7. Parameter
- This folder houses a job-parameter.py, which basically helps user in connecting to redshift table and getting the 
- input parameters based on job_id.

### 8. run_notebook
- This folder houses a .py file which helps user to execute certain functions related to Sagemaker jobs, such as
- executing a sagemaker job.

