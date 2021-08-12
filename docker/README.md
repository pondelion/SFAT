
- build 

```bash
SFAT$ sudo docker build -t sfat -f docker/Dockerfile .
```

- run

```bash
SFAT$ sudo docker run -p 8501:8501 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY sfat
```