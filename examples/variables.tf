/*
  *
  * Optional Variables
  *
  */

variable "runtask_name" {
  type        = string
  description = "The name attached to the run task"
  default     = "aws-iam-analyzer"
}

variable "runtask_description" {
  type        = string
  description = "The description give to the attached run task (optional)"
  default     = "This Run Task analyzes your AWS IAM Policy before apply"
}

variable "runtask_enforcement_level" {
  type        = string
  description = "The description give to the attached run task (optional)"
  default     = "mandatory"
}

variable "runtask_stage" {
  type        = string
  description = "The description give to the attached run task (optional)"
  default     = "post_plan"
}

/*
  *
  * Required Variables
  *
  */

variable "runtask_eventbridge_url" {
  type        = string
  description = "The URL of your run task created from the event bridge output"
}

variable "runtask_hmac" {
  type        = string
  description = "The HMAC key for the run task"
}