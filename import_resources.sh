#!/bin/bash
# filepath: /Users/maxmengeringhausen/IPI/devops/fastapi-spotlike/import_resources.sh

set -e

# Récupérer l'ID du compte AWS
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cd terraform

# Vérifier si le terraform state existe déjà
terraform init

# Essayer d'importer chaque ressource - utiliser || true pour continuer même si l'import échoue
echo "Tentative d'import des ressources existantes..."

terraform import aws_iam_role.ecs_task_execution_role spotlike-task-execution-role || true
terraform import aws_iam_role.app_role spotlike-app-role || true
terraform import aws_iam_policy.s3_access_policy arn:aws:iam::${AWS_ACCOUNT_ID}:policy/spotlike-s3-access || true
terraform import aws_db_subnet_group.spotlike_db_subnet_group spotlike-db-subnet-group || true
terraform import aws_cloudwatch_log_group.spotlike_logs /ecs/spotlike-logs || true

# Pour le load balancer et les target groups, il faut les ARNs exacts
# On peut essayer de les récupérer via AWS CLI
ALB_ARN=$(aws elbv2 describe-load-balancers --names spotlike-alb --query 'LoadBalancers[0].LoadBalancerArn' --output text 2>/dev/null || echo "")
if [ ! -z "$ALB_ARN" ] && [ "$ALB_ARN" != "None" ]; then
    terraform import aws_lb.spotlike_alb $ALB_ARN || true
fi

API_TG_ARN=$(aws elbv2 describe-target-groups --names spotlike-api-tg --query 'TargetGroups[0].TargetGroupArn' --output text 2>/dev/null || echo "")
if [ ! -z "$API_TG_ARN" ] && [ "$API_TG_ARN" != "None" ]; then
    terraform import aws_lb_target_group.api_tg $API_TG_ARN || true
fi

FRONTEND_TG_ARN=$(aws elbv2 describe-target-groups --names spotlike-frontend-tg --query 'TargetGroups[0].TargetGroupArn' --output text 2>/dev/null || echo "")
if [ ! -z "$FRONTEND_TG_ARN" ] && [ "$FRONTEND_TG_ARN" != "None" ]; then
    terraform import aws_lb_target_group.frontend_tg $FRONTEND_TG_ARN || true
fi

terraform import aws_ssm_parameter.db_password /Spotilike/prod/db-password || true

echo "Import terminé. Certaines ressources peuvent avoir échoué si elles n'existaient pas déjà."