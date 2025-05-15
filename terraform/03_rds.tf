###############################################
# BASE DE DONNÉES RDS (POSTGRESQL)
###############################################

# Groupe de sous-réseaux pour RDS
resource "aws_db_subnet_group" "db_subnet" {
  name       = "${var.project_name}-db-subnet"
  subnet_ids = aws_subnet.public[*].id  # Utilise les sous-réseaux publics
  
  tags = {
    Name = "${var.project_name}-db-subnet"
  }
}

# Base de données PostgreSQL (tier gratuit)
resource "aws_db_instance" "postgres" {
  identifier             = "${var.project_name}-db"
  engine                 = "postgres"
  engine_version         = "15.3"
  instance_class         = "db.t2.micro" # Gratuit pendant 12 mois
  allocated_storage      = 20
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = "default.postgres15"
  db_subnet_group_name   = aws_db_subnet_group.db_subnet.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  skip_final_snapshot    = true
  
  tags = {
    Name = "${var.project_name}-db"
  }
} 