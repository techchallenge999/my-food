resource "aws_iam_role" "eks-cluster" {
  name = "eks-cluster-${var.cluster_name}"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::447798043017:root",
        "Service": [
            "eks.amazonaws.com",
            "elasticloadbalancing.amazonaws.com"
        ]
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

resource "aws_iam_role" "pod_execution_role" {
  name = "eks-fargate-profile-myfood"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Condition": {
          "ArnLike": {
              "aws:SourceArn": "arn:aws:eks:us-east-1:447798043017:fargateprofile/*"
          }
        },
        "Principal": {
          "Service": "eks-fargate-pods.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role" "eks-fargate-profile" {
  name = "eks-fargate-profile"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks-fargate-pods.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "myfood_AmazonEKSFargatePodExecutionRolePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role       = aws_iam_role.eks-fargate-profile.name
}

resource "aws_eks_fargate_profile" "fargate_profile" {
  cluster_name           = aws_eks_cluster.cluster.name
  fargate_profile_name   = "fargate_profile"
  pod_execution_role_arn = aws_iam_role.eks-fargate-profile.arn
  subnet_ids             = module.vpc.private_subnets.*

  selector {
    namespace = "default"
  }
  selector {
    namespace = "kube-system"
  }

  selector {
    namespace = "kube-public"
  }

  selector {
    namespace = "kube-node-lease"
  }

  depends_on = [aws_iam_role_policy_attachment.myfood_AmazonEKSFargatePodExecutionRolePolicy, module.vpc]
}

resource "null_resource" "k8s_patcher" {
  depends_on = [aws_eks_fargate_profile.fargate_profile]

  triggers = {
    endpoint = aws_eks_cluster.cluster.endpoint
    ca_crt   = base64decode(aws_eks_cluster.cluster.certificate_authority[0].data)
    token    = data.aws_eks_cluster_auth.default.token
  }

  provisioner "local-exec" {
    command = <<EOH
      cat >/tmp/ca.crt <<EOF
      ${base64decode(aws_eks_cluster.cluster.certificate_authority[0].data)}
      EOF
      kubectl \
        --server="${aws_eks_cluster.cluster.endpoint}" \
        --certificate_authority=/tmp/ca.crt \
        --token="${data.aws_eks_cluster_auth.default.token}" \
        patch deployment coredns \
        -n kube-system --type json \
        -p='[{"op": "remove", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'
    EOH
  }

  lifecycle {
    ignore_changes = [triggers]
  }
}
