# Étape 1 : Construction de l'application Angular
FROM node:18 AS build

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
FROM nginx:alpine

# Copier les fichiers Angular générés dans le répertoire Nginx
COPY --from=build /frontend/dist/frontend/browser /usr/share/nginx/html

# Exposer le port (par défaut 80 pour Nginx)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]