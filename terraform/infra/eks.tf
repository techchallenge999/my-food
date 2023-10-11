resource "aws_iam_role" "eks-cluster" {
  name = "eks-cluster-${var.cluster_name}"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "amazon-eks-cluster-policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks-cluster.name
}

resource "aws_eks_cluster" "cluster" {
  name            = var.cluster_name
  version         = var.cluster_version
  role_arn        = aws_iam_role.eks-cluster.arn

  vpc_config {
    subnet_ids         = concat(module.vpc.public_subnets.*, module.vpc.private_subnets.*)
  }

  depends_on      = [aws_iam_role_policy_attachment.amazon-eks-cluster-policy, module.vpc]
}
