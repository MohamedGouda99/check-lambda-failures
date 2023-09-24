import boto3

role_name = "TerminateEC2Role"

# Initialize the AWS IAM client
iam_client = boto3.client('iam')

# Get a list of attached policies
response = iam_client.list_attached_role_policies(RoleName=role_name)

# Open a file for writing
with open("policies_output.txt", "w") as output_file:
    for policy in response['AttachedPolicies']:
        policy_name = policy['PolicyName']
        policy_arn = policy['PolicyArn']
        
        # Get the policy version
        policy_response = iam_client.get_policy(PolicyArn=policy_arn)
        default_version_id = policy_response['Policy']['DefaultVersionId']
        
        # Get the policy document
        policy_version_response = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=default_version_id)
        policy_json = policy_version_response['PolicyVersion']['Document']
        
        # Write to file
        output_file.write(f"Policy Name: {policy_name}\n")
        output_file.write(f"Policy JSON: {policy_json}\n\n")
