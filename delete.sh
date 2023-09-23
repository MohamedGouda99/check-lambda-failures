aws s3 rm s3://osabucket12329484118 --recursive
aws cloudformation delete-stack \
--stack-name $1 --region=$2