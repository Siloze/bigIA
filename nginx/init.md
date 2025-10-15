openssl genpkey -algorithm RSA -out /etc/nginx/jwt_signing.key -pkeyopt rsa_keygen_bits:2048
openssl rsa -in /etc/nginx/jwt_signing.key -pubout -out /etc/nginx/jwt_public.pem

liens discussion chatgpt pour mettre en place:
https://chatgpt.com/share/688e35e5-8b64-800c-89c5-45550ae3471c