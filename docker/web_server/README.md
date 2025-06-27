Launch web server at port 8000 (edit src/web_server/server.py and -p to change it)

```bash
docker build -t llm-web-server .
docker run --rm -p 8000:8000 -v C:\Users\shmouel\Documents\bigIA:/app/ llm-web-server
```