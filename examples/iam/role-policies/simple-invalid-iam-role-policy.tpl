{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "secretsmanager:DescribeSecret",
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "arn:${data_aws_partition}:secretsmanager:${data_aws_region}:${data_aws_account_id}:secret:${var_name_prefix}",
            "Effect": "Allow",
            "Sid": "SecretsManagerRead"
        },
        {
            "Action": "events:PutEvents",
            "Resource": "arn:${data_aws_partition}:events:${data_aws_region}:${data_aws_account_id}:event-bus/${var_name_prefix}",
            "Effect": "Allow",
            "Sid": "EventBridgePut"
        }
    ]
}