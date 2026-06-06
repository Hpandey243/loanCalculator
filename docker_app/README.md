# Loan Calculator — Docker

## 1. Build the image

Builds a local Docker image from the `Dockerfile` in the project root.

```bash
docker build -t loan-calculator .
```

## 2. Push to Docker Hub

Tags the local image with your Docker Hub repo name and uploads it to the registry.

```bash
docker tag loan-calculator abhinavanil9/loan-calculator:latest
docker push abhinavanil9/loan-calculator:latest
```

## 3. Pull from Docker Hub

Downloads the published image to any machine — no source code needed.

```bash
docker pull abhinavanil9/loan-calculator:latest
```

## 4. Run locally

Starts the container and maps port 8000 so the app is accessible on your machine.

```bash
docker run -p 8000:8000 abhinavanil9/loan-calculator:latest
```

## 5. Verify the container is running

Lists all running containers — confirm `loan-calculator` appears with status `Up`.

```bash
docker ps
```

Open http://localhost:8000 in your browser.
