# Terraform Cloud Run Tasks with IAM Access Analyzer

Sample demonstration of Run Tasks integration with IAM Access Analyzer (IA2) to validate IAM policy. This demonstration uses Run Task Post Plan with endpoint served by Lambda Function URL. The IAM policy validation is done using Step Function integrated with IAM Access Analyzer.

![Diagram](./diagram/RunTask-EventBridge.png)

# Getting started

## Step 1 

* Clone the repository and change the directory

```bash
git clone git@github.com:wellsiau-aws/runtask-iam-access-analyzer.git
cd runtask-iam-access-analyzer/event-bridge
```

* Change the org name in the file [`provider.tf`](/event-bridge/provider.tf#L5) to your TFC org, optionally you can configure the workspace name too.

```t
  terraform {

    cloud {
      # TODO: Change this to your Terraform Cloud org name.
      organization = "tfc-integration-sandbox"
      .
      .
```

* Make Lambda files

```
cd event-bridge/
make all
```

* Apply the Terraform Configuration, this will require you to configure the AWS credentials in Terraform Cloud. [Follow these instructions to learn more](https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-create-variable-set).

```bash
echo 'tfc_org="tfc-integration-sandbox"' | tee tf.auto.tfvars
terraform init
terraform apply
```

* Copy the function URL output (`runtask_eventbridge_url`) and use it on the next step.

```bash
.
.
Apply complete! Resources: 28 added, 0 changed, 22 destroyed.

Outputs:

runtask_eventbridge_url = "https://<enter_your_generated_aws_url_here>"
runtask_hmac = <sensitive>
```

* To view the run task hmac key, use the following

```bash
terraform output -raw runtask_hmac
```

## Step 2 

* Next, retrieve the HMAC key value and use is along with the function URL output when setting up the Run Task in Terraform Cloud. 

```
cd examples/
```

* Change the org name in the file [`main.tf`](/examples/main.tf#L9) file in 2 locations, optionally you can configure the workspace name too.

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

* In order to create and configure the run tasks, you need to have Terraform Cloud keys stored as Variable/Variable Sets in the workspace

![TFC Configure Variable Set](diagram/TerraformCloud-VariableSets.png?raw=true "Configure Terraform Cloud Variable Set")

 * Create and attach the run task using the following command

```bash
echo 'runtask_eventbridge_url="<enter_your_generated_aws_url_here>"' >> tf.auto.tfvars
echo 'runtask_hmac="<enter_your_runtask_hmac_here>"' >> tf.auto.tfvars

terraform init
terraform apply
```

* Successfull creation of the run task should look something like this:

```bash
.
.
.
tfe_organization_run_task.aws-iam-analyzer: Creation complete after 2s [id=task-MPeju2LbLexXBzhg]
tfe_workspace_run_task.aws-iam-analyzer-attach: Creating...
tfe_workspace_run_task.aws-iam-analyzer-attach: Creation complete after 1s [id=wstask-YXFF3NSXtjx9xCMP]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```
 
## Step 3
  
* Uncomment these lines in the [`main.tf`](/examples/main.tf#L59) file.

```bash
.
.
.
# provider "aws" {
#   # TODO: Specify the region you like to use.
#   region = "us-east-2"
# }

# data "aws_ami" "amazon2" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["amzn2-ami-hvm-*-x86_64-ebs"]
#   }

#   owners = ["amazon"]
# }

# resource "aws_instance" "ec2" {
#   ami           = data.aws_ami.amazon2.id
#   instance_type = "t3.nano"
# }
```
* To test the run task let's try to deploy an EC2 instance in AWS. This will require you to configure the AWS credentials in Terraform Cloud. [Follow these instructions to learn more](https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-create-variable-set).

```bash
terraform init -upgrade
terraform plan
```

* The result should look something like this:

```bash
.
.
.
Plan: 1 to add, 0 to change, 0 to destroy.

Post-plan Tasks:

All tasks completed! 1 passed, 0 failed           (2s elapsed)

│ aws-iam-analyzer ⸺   Passed
│ 0 ERROR, 0 SECURITY_WARNING, 0 SUGGESTION, 0 WARNING
│ Details: https://kx7o9wj3me.execute-api.us-east-1.amazonaws.com
│ 
│ 
│ Overall Result: Passed
```

