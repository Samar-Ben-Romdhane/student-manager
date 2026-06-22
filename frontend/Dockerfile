FROM nginx:1.28-alpine

LABEL maintainer="student-manager"

# Mettre à jour tous les packages Alpine pour corriger les CVE système
RUN apk upgrade --no-cache

RUN rm -rf /usr/share/nginx/html/*
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/
COPY assets /usr/share/nginx/html/assets

EXPOSE 80
