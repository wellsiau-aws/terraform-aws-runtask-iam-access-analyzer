# Terraform Cloud Run Tasks with IAM Access Analyzer

Sample demonstration of Run Tasks integration with IAM Access Analyzer (IA2) to validate IAM policy. This demonstration uses Run Task Post Plan with endpoint served by Lambda Function URL. The IAM policy validation is done using Step Function integrated with IAM Access Analyzer.

![Diagram](./diagram/RunTask-EventBridge.png)

## Getting started

First, clone and deploy the AWS infrastructure including Lambda function URL, EventBridge rules and Step functions.

TODO fix:
```
cd event-bridge/
# change the org name in lambda/runtask_request/handler.py#L35 to your TFC org
make all
```

```
git clone git@github.com:wellsiau-aws/runtask-iam-access-analyzer.git
cd runtask-iam-access-analyzer/event-bridge
terraform init
terraform apply
```

Copy the function URL output (`runtask_eventbridge_url`) and use it on the next step.

Next, retrieve the HMAC key value from AWS Secrets Manager. 

Use the function URL output and the HMAC value when setting up the Run Task in Terraform CLoud. 

Create new workspace and attach the Run Task, use Post Plan mode.

Run Terraform apply to test.