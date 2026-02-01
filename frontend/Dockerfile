FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY dist/ ./

RUN rm index.html && ln -s /index.html index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon_off;"]