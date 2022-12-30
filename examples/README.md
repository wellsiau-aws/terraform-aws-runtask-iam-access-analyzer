# Usage Example

You must first deploy the module by following [guide](../README.md#Usage) as referenced in the solution README.

## Attach Run Task in Terraform Cloud Workspace

Follow the steps below to attach the run task created from the module into a new **demo workspace**. 

* Use the provided example below to launch simple AWS IAM resources and inspect it with IAM Access Analyzer.

  ```bash
  cd ../examples/
  ```

* Change the org name in the file [`examples/provider.tf`](provider.tf#L5) to your TFC org.

  ```
  terraform {

    cloud {
      # TODO: Change this to your Terraform Cloud org name.
      organization = "<enter your org name here>"
      workspaces {
        tags = ["env:aws-run-task-demo"]
      }
    }
    ...
  }   
  ```

* Populate the required variables, change the placeholder value below.
  ```bash
  echo 'tfc_org="<enter your org name here>"' >> tf.auto.tfvars
  echo 'aws_region="<enter the AWS region here>"' >> tf.auto.tfvars
  echo 'runtask_id="<enter the Run Task ID output from previous module deployment>"' >> tf.auto.tfvars
  echo 'demo_workspace_name="<enter the new demo workspace name here>"' >> tf.auto.tfvars
  ```

* Initialize Terraform Cloud. When prompted, enter the name of the new demo workspace as you specified in the previous step.
  ```bash
  terraform init
  ```

* Configure the AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in Terraform Cloud, i.e. using variable sets. [Follow these instructions to learn more](https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-create-variable-set).

 * Enable the flag to attach the run task to the demo workspace.
   ```bash
   echo 'flag_attach_runtask="true"' >> tf.auto.tfvars
   terraform apply
   ```

* Navigate back to Terraform Cloud, locate the new demo workspace and confirm that the Run Task is attached to the demo workspace. ![TFC Run Task in Workspace](../diagram/TerraformCloud-RunTaskWorkspace.png?raw=true "Run Task attached to the demo workspace")


## Test IAM Access Analyzer using Run Task

The following steps deploy simple IAM policy with invalid permissions. This should trigger the Run Task to send failure and stop the apply.

* Enable the flag to deploy invalid IAM policy to the demo workspace.
  ```bash
  echo 'flag_deploy_invalid_resource="true"' >> tf.auto.tfvars
  terraform apply
  ```

* Terraform apply will fail due to several error. Use the CloudWatch link to review the errors.