{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "secretsmanager:DescribeSecret",
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "${resource_runtask_hmac}",
            "Effect": "Allow",
            "Sid": "SecretsManagerGetHMAC"
        },
        {
            "Action": "events:PutEvents",
            "Resource": "arn:${data_aws_partition}:events:${data_aws_region}:${data_aws_account_id}:event-bus/${var_event_bus_name}",
            "Effect": "Allow",
            "Sid": "EventBridgePut"
        }
    ]
}