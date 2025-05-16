resource "aws_db_subnet_group" "spotlike_db_subnet_group" {
  name       = "spotlike-db-subnet-group"
  subnet_ids = module.vpc_spotlike.private_subnets
  
  tags = {
    Name = "spotlike-db-subnet-group"
  }
}



resource "aws_db_instance" "spotlike_postgres" {
  identifier             = "spotlike-db"
  allocated_storage      = 5
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  db_name                = "spotilike_db"
  username               = "postgres"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.spotlike_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.spotlike_db_sg.id]
  skip_final_snapshot    = true
  
  tags = {
    Name = "spotlike-postgres-db"
  }
}