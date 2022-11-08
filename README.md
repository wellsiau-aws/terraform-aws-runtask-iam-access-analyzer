# Terraform Cloud Run Tasks with IAM Access Analyzer

Sample demonstration of Run Tasks integration with IAM Access Analyzer (IA2) to validate IAM policy. This demonstration uses Run Task Post Plan with endpoint served by Lambda Function URL. The IAM policy validation is done using Step Function integrated with IAM Access Analyzer.

![Diagram](./diagram/RunTask-EventBridge.png)

## Getting started

### Step 1 

Clone and deploy the AWS infrastructure including Lambda function URL, EventBridge rules and Step functions.

[TODO: fix] Change the org name in the file [`/event-bridge/lambda/runtask_request/handler.py`](/event-bridge/lambda/runtask_request/handler.py#L35) to your TFC org:

```py
# Change the org name
if event["payload"]["detail"]["organization_name"] == "wellsiau-org":
```

Make Lambda files

```
cd event-bridge/
make all
```

```
git clone git@github.com:wellsiau-aws/runtask-iam-access-analyzer.git
cd runtask-iam-access-analyzer/event-bridge
terraform init
terraform apply
```

Copy the function URL output (`runtask_eventbridge_url`) and use it on the next step.

### Step 2 

Next, retrieve the HMAC key value from AWS Secrets Manager and use is along with the function URL output when setting up the Run Task in Terraform Cloud. 

```
cd examples/
```

Make sure you have the capability to create a new workspace in Terraform Cloud, we'll be creating a new workspace with name "test-aws-runtask", 

Input your Terraform Cloud org name in [`main.tf`](/examples/main.tf#L9) file in 2 locations

```t
.
.
.
  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "<enter your org name here>"
  }
.
.
.
data "tfe_organization" "org" {
  # TODO: Change this to your Terraform Cloud org name.
  name = "<enter your workspace name here>"
}
.
.
.
```

Create the run task using the following command

```bash
terraform init
terraform apply \
-var runtask_eventbridge_url="<your run task event bridge url here>" \ 
-var runtask_hmac="<your run task HMAC key here>"
```

### Step 3

To test the run task let's try to deploy an EC2 instance in AWS. Uncomment the last few lines in the [`main.tf`](/examples/main.tf#L59) file