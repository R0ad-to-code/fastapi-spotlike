#!/bin/bash
set -e

# Se placer dans le dossier du projet
cd "$(dirname "$0")"

# Se placer dans le dossier Terraform
cd terraform

# Récupérer les modifications
echo "🔄 Récupération des modifications Terraform..."
terraform plan -out=tfplan

# Appliquer les modifications
echo "🚀 Application des modifications..."
terraform apply tfplan

# Générer le script pour reconstruire et déployer les images
cd ..
echo "🛠️ Mise à jour des images Docker..."
./build_push_image.sh

echo "✅ Infrastructure mise à jour avec succès!"
echo "🔍 Les URLs peuvent être obtenues avec: cd terraform && terraform output" 