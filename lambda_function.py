import boto3
import json

def lambda_handler(event, context):
    # Initialize the AWS Lambda client
    lambda_client = boto3.client('lambda')
    
    # Initialize the AWS SNS client
    sns_client = boto3.client('sns')
    
    # Get a list of all Lambda functions in your AWS account
    response = lambda_client.list_functions()
    all_functions = response['Functions']
    
    # Dictionary to store the status of each Lambda function
    function_statuses = {}
    
    for function in all_functions:
        function_name = function['FunctionName']
        try:
            # Invoke the Lambda function
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse'  # Use 'Event' for asynchronous invocation
            )
    
            # Parse the payload JSON from the response
            payload = json.loads(response['Payload'].read().decode('utf-8'))
    
            # Check if the Lambda function executed successfully
            if 'statusCode' in payload and payload['statusCode'] == 200:
                function_statuses[function_name] = "Success"
            else:
                function_statuses[function_name] = "Failed"
        except Exception as e:
            # If an exception occurs during invocation, consider it a failure
            function_statuses[function_name] = "Failed"
    
    # Check if any function has failed and trigger an SNS notification
    for function_name, status in function_statuses.items():
        if status == "Failed":
            # Send an SNS notification
            sns_topic_arn = 'arn:aws:sns:us-east-2:629161141964:mytopic'
            sns_message = f"Lambda function {function_name} has failed."
            sns_client.publish(TopicArn=sns_topic_arn, Message=sns_message)
    
    # You can now analyze the function_statuses dictionary to determine which functions failed
    # For example, you can log the results or take other actions based on the statuses.
    
    # Return the function statuses in the response body
    response_body = {
        'statusCode': 200,
        'body': json.dumps({
            'FunctionStatuses': function_statuses
        })
    }
    
    return response_body
