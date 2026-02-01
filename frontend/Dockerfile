FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set working directory
WORKDIR /usr/share/nginx/html

# Remove default html files
RUN rm -rf ./*

# Copy frontend files
COPY index.html .
COPY app.js .
COPY pay-bill.html .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
