FROM nginx:1.21.1-alpine

COPY mynginx.tmp /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/
COPY entrypoint.sh /home/
ENTRYPOINT ["/home/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]