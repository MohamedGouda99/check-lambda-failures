#!/bin/bash

# Get the Lambda function ARN
lambda_arn=$(aws lambda list-functions --query "Functions[?FunctionName=='error_handler'].FunctionArn" --output text)

# Remove the existing Arn value
sed -i '/^\(\s*Arn: >-\)/d' cloudwatch.yml

# Add the new Arn value with proper indentation
sed -i "/^\(\s*Targets:\)/a\ \ \ \ \ \ \ \ Arn: >-\n\ \ \ \ \ \ \ \ \  $lambda_arn" cloudwatch.yml
