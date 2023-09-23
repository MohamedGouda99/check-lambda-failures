import boto3
import zipfile
import os

# Initialize AWS clients
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

# Define the file and S3 bucket information
# function_name = 'error_handler'
s3_bucket_name = 'osabucket12329484118'
zip_file_name = 'lambda_function.zip'

# Zip the Python file and dependencies
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('lambda_function.py')
    for root, dirs, files in os.walk('dependencies'):
        for file in files:
            file_path = os.path.join(root, file)
            arc_name = os.path.relpath(file_path, 'dependencies')
            zipf.write(file_path, arcname=arc_name)

# Upload the zip file to S3
s3_client.upload_file(zip_file_name, s3_bucket_name, zip_file_name)
#os.remove(zip_file_name)



