FROM nginx:1.25-alpine

# Remove a configuração padrão do NGINX
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuração customizada
COPY nginx.conf /etc/nginx/nginx.conf

# Copia os arquivos estáticos do frontend
COPY html/ /usr/share/nginx/html/

EXPOSE 8080 8443

CMD ["nginx", "-g", "daemon off;"]