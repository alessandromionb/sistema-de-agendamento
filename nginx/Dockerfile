FROM nginx:1.25-alpine

RUN apk add --no-cache openssl \
    && mkdir -p /etc/nginx/certs \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/certs/key.pem \
        -out /etc/nginx/certs/cert.pem \
        -subj "/CN=localhost"

# Remove a configuração padrão do NGINX
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuração customizada
COPY nginx.conf /etc/nginx/nginx.conf

# Copia os arquivos estáticos do frontend
COPY html/ /usr/share/nginx/html/

EXPOSE 8080 8443

CMD ["nginx", "-g", "daemon off;"]
