#!/bin/bash

# Script pour corriger les imports dans les fichiers Python
find app -type f -name "*.py" -exec sed -i '' 's/from app\./from /g' {} \;
find app -type f -name "*.py" -exec sed -i '' 's/import app\./import /g' {} \;

echo "Imports corrigés dans tous les fichiers Python" 