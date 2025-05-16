module "vpc_spotlike" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  

  name = "spotlike-vpc"
  cidr = "10.0.0.0/16"  # CIDR différent pour éviter les conflits

  azs             = ["eu-west-3a", "eu-west-3b", "eu-west-3c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  # Activation de la NAT Gateway pour permettre aux ressources dans les sous-réseaux privés
  # d'accéder à Internet (important pour les mises à jour, téléchargements de packages, etc.)
  enable_nat_gateway = true
  
  # Une seule NAT Gateway pour économiser des coûts (en production, vous pourriez en avoir une par AZ)
  single_nat_gateway = true
  
  
  # Crée des tables de routage dédiées pour chaque sous-réseau
  one_nat_gateway_per_az = false

  # Active DNS dans le VPC
  enable_dns_hostnames = true
  enable_dns_support   = true

  # Configuration EIP pour NAT Gateway (utilisant domain au lieu de vpc)
  map_public_ip_on_launch = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "spotlike"
  }

  # Tags pour les sous-réseaux publics (utile pour les ingress controllers Kubernetes)
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  # Tags pour les sous-réseaux privés
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }
}