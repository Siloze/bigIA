Make sure to have nvidia-docker install:
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

Launch with gpu:
```bash
docker build -t llama-gpu .
docker run --rm -p 5000:5000 --gpus all C:\Users\shmouel\Documents\bigIA:/app/ llama-gpu
```
