###############################################
# RÉSEAU DE BASE (VPC ET SOUS-RÉSEAUX)
###############################################

# VPC pour notre application
resource "aws_vpc" "spotilike_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Sous-réseaux publics (requis pour RDS et ECS)
resource "aws_subnet" "public" {
  count                   = 2  # AWS exige au moins 2 zones pour RDS
  vpc_id                  = aws_vpc.spotilike_vpc.id
  cidr_block              = count.index == 0 ? "10.0.1.0/24" : "10.0.2.0/24"
  availability_zone       = count.index == 0 ? "${var.aws_region}a" : "${var.aws_region}b"
  map_public_ip_on_launch = true  # Attribut des IPs publiques automatiquement
  
  tags = {
    Name = "${var.project_name}-subnet-${count.index + 1}"
  }
}

# Passerelle internet pour accéder à internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.spotilike_vpc.id
  
  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Table de routage pour les sous-réseaux
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.spotilike_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  
  tags = {
    Name = "${var.project_name}-rt"
  }
}

# Association des sous-réseaux à la table de routage
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
} 