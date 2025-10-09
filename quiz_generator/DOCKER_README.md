# Quiz Generator Docker Setup

This document explains how to build and run the Quiz Generator application using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop all services:**
   ```bash
   docker-compose down
   ```

4. **View logs:**
   ```bash
   docker-compose logs quiz-generator
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t quiz-generator .
   ```

2. **Run the container:**
   ```bash
   docker run -it --rm \
     -v $(pwd)/outputs:/app/outputs \
     -v $(pwd)/src/quiz_generator/dataset:/app/src/quiz_generator/dataset \
     --env-file .env \
     quiz-generator
   ```

## Services

The Docker Compose setup includes:

- **quiz-generator**: Main application container that runs CrewAI flows
- **qdrant**: Vector database for RAG functionality (accessible at http://localhost:6333)

## Environment Variables

Create a `.env` file in the project root with your configuration. The current setup uses:

- `MLFLOW_TRACKING_URI=file:///app/mlruns` - Local file system MLflow tracking
- `PYTHONPATH=/app/src` - Python path configuration

Add your additional environment variables as needed:

```env
# OpenAI Configuration (example)
OPENAI_API_KEY=your_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
AZURE_OPENAI_API_KEY=your_azure_api_key_here

# Other configuration variables as needed
```

## Volume Mounts

- `./outputs:/app/outputs` - Persists generated quiz files
- `./src/quiz_generator/dataset:/app/src/quiz_generator/dataset` - Access to training datasets
- `./.env:/app/.env:ro` - Environment configuration (read-only)

## Ports

- `6333` - Qdrant HTTP API
- `8000` - Quiz Generator app port (available for web interface)

## Application Details

### Dockerfile Structure

The current Dockerfile:
- Uses `python:3.11-slim` as the base image
- Installs essential packages: CrewAI, markdown processing tools (markdown-pdf, markdown2, md2pdf, pdfkit)
- Copies source code and pyproject.toml
- Installs the local package in editable mode
- Runs `crewai flow kickoff` as the default command

### Docker Compose Configuration

The compose file sets up:
- **quiz-generator-app**: Main application container with volume mounts and network configuration
- **qdrant-db**: Vector database using the latest Qdrant image
- **quiz-network**: Bridge network for service communication
- **qdrant_data**: Named volume for persistent Qdrant storage

## Development

### Interactive Development

Run the container with an interactive shell:

```bash
docker run -it --rm \
  -v $(pwd):/app \
  --env-file .env \
  quiz-generator bash
```

### Debugging

View container logs:
```bash
docker-compose logs -f quiz-generator
```

Execute commands inside running container:
```bash
docker-compose exec quiz-generator bash
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change port mappings in `docker-compose.yml`
2. **Permission issues**: Ensure proper file permissions for mounted volumes
3. **Memory issues**: Increase Docker Desktop memory allocation
4. **Environment variables**: Verify `.env` file exists and is properly formatted
5. **CrewAI flow issues**: Check that all required dependencies are installed and configured

### Logs

Check application logs:
```bash
docker-compose logs quiz-generator
```

Check Qdrant logs:
```bash
docker-compose logs qdrant
```

### Container Status

Check running containers:
```bash
docker-compose ps
```