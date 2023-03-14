FROM openresty/openresty:alpine

WORKDIR /usr/local/openresty

ADD root /

EXPOSE 8080

CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]