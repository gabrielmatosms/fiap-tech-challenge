module "eks_admins_iam" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-group-with-policies"
  version = "5.3.1"

  name = "eks-admin"

  group_users = [
    "admin" # This should be your IAM user or role
  ]

  attach_iam_self_management_policy = true

  custom_group_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
    "arn:aws:iam::aws:policy/AmazonEKSServicePolicy",
  ]

  custom_group_policies = [
    {
      name   = "eks-full-access"
      policy = data.aws_iam_policy_document.eks_full_access.json
    }
  ]
}

data "aws_iam_policy_document" "eks_full_access" {
  statement {
    sid    = "EKSFullAccess"
    effect = "Allow"

    actions = [
      "eks:*",
    ]

    resources = ["*"]
  }
} 