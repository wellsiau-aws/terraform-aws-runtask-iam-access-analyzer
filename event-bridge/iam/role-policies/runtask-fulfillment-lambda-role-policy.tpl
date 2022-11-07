{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "access-analyzer:ValidatePolicy"
            ],
            "Resource": "arn:${data_aws_partition}:access-analyzer:${data_aws_region}:${data_aws_account_id}:*",
            "Effect": "Allow",
            "Sid": "AccessAnalyzerOps"
        }
    ]
}