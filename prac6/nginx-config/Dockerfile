# Dockerfile for Nginx
FROM nginx:latest

# Eliminar la configuración por defecto de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar tu configuración personalizada de Nginx
COPY ./nginx-config/default.conf /etc/nginx/conf.d/default.conf

# Crear la carpeta para los archivos estáticos
RUN mkdir -p /var/www/static

# Configurar permisos si es necesario
RUN chown -R nginx:nginx /var/www/static

# Exponer los puertos
EXPOSE 1337
EXPOSE 443

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]


