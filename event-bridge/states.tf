# Update Alternate Contacts
resource "aws_sfn_state_machine" "runtask_states" {
  name       = "${var.name_prefix}-runtask-statemachine"
  role_arn   = aws_iam_role.runtask_states.arn
  definition = templatefile("${path.module}/states/runtask_states.asl.json", {
    resource_runtask_request      = aws_lambda_function.runtask_request.arn
    resource_runtask_fulfillment  = aws_lambda_function.runtask_fulfillment.arn
    resource_runtask_callback     = aws_lambda_function.runtask_callback.arn
  })
}
