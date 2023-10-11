
resource "aws_elasticache_subnet_group" "default" {
  name       = "elasticache-subnet"
  subnet_ids = concat(module.vpc.public_subnets.*, module.vpc.private_subnets.*)
}

resource "aws_elasticache_replication_group" "default" {
  replication_group_id          = "elasticache-cluster"
  description                   = "Redis cluster for My food"

  node_type            = "cache.t4g.micro"
  port                 = 6379
  parameter_group_name = "default.redis7.cluster.on"

  snapshot_retention_limit = 5
  snapshot_window          = "00:00-05:00"

  subnet_group_name          = "${aws_elasticache_subnet_group.default.name}"
  automatic_failover_enabled = true

  replicas_per_node_group = 1
  num_node_groups         = 1

}
