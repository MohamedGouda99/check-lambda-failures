#!/bin/bash

# Define the path to your Python script
python_script="lambda_function.py"

# Use AWS CLI to get the SNS Topic ARN
new_sns_topic_arn=$(aws sns list-topics --query 'Topics[0].TopicArn' --output text)

# Check if new_sns_topic_arn is not empty
if [ -z "$new_sns_topic_arn" ]; then
  echo "Failed to retrieve SNS Topic ARN."
  exit 1
fi

# Use sed to delete the existing sns_topic_arn value and replace it with the new value
sed -i "s|sns_topic_arn = .*|sns_topic_arn = '$new_sns_topic_arn'|" $python_script

echo "SNS topic ARN updated in $python_script"
