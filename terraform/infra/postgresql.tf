resource "aws_db_instance" "default" {
  allocated_storage = var.allocated_storage
  storage_type = var.storage_type
  engine = var.engine
  engine_version = var.engine_version
  instance_class = var.instance_class
  db_name= var.name
  username = var.username
  password = var.password
  port = var.port
  identifier = var.identifier
  skip_final_snapshot = var.skip_final_snapshot
  publicly_accessible    = true
}
