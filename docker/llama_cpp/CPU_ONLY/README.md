Launch with cpu only:
```bash
docker build -t llama-cpu .
docker run --rm -p 5000:5000 -v C:\Users\shmouel\Documents\bigIA:/app/ llama-cpu
```