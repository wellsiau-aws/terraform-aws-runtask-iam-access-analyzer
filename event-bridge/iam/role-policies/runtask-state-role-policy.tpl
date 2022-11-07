{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:${data_aws_partition}:lambda:${data_aws_region}:${data_aws_account_id}:function:${var_name_prefix}*:*"
            ]
        }
    ]
}
