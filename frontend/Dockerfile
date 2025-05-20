# Étape 1 : Construction de l'application Angular
FROM --platform=linux/amd64 node:18 AS build

# Définir le répertoire de travail
WORKDIR /frontend

# Copier les fichiers nécessaires
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code et construire l'application
COPY . .
RUN npm run build --prod

# Étape 2 : Serveur pour les fichiers statiques (Nginx)
FROM --platform=linux/amd64 nginx:alpine

# Copier les fichiers Angular générés dans le répertoire Nginx
COPY --from=build /frontend/dist/frontend/browser/ /usr/share/nginx/html/

# Copier notre configuration nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf.template

# Ajouter un script de démarrage pour remplacer les variables d'environnement
RUN echo '#!/bin/sh' > /docker-entrypoint.sh && \
    echo 'envsubst "\${LOAD_BALANCER_DNS}" < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf' >> /docker-entrypoint.sh && \
    echo 'nginx -g "daemon off;"' >> /docker-entrypoint.sh && \
    chmod +x /docker-entrypoint.sh

# Exposer le port (par défaut 80 pour Nginx)
EXPOSE 80
CMD ["/docker-entrypoint.sh"]