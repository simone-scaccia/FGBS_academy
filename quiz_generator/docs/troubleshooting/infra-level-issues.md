# Infrastructure-Level Issues

*(Template refs: Annex IV ¶2(l))*  

## Common Infrastructure Issues

### 1. Docker not running
- **Symptom:** `Error response from daemon: Cannot connect to the Docker daemon`  
- **Cause:** Docker Desktop (or the Docker daemon) is not started.  
- **Mitigation:**  
  - Start Docker Desktop (Windows/macOS).  
  - On Linux, ensure the service is active:  
    ```bash
    systemctl status docker
    systemctl start docker
    ```

---

### 2. Qdrant volume corruption
- **Symptom:** Flow crashes with `Service internal error: File exists (os error 17)`  
- **Cause:** corrupted or conflicting Qdrant Docker volume.  
- **Mitigation:**  
  ```bash
  docker stop qdrant
  docker rm qdrant
  docker volume rm qdrant-storage
  docker volume create qdrant-storage
  docker run --name qdrant \
    -p 6333:6333 -p 6334:6334 \
    -v qdrant-storage:/qdrant/storage \
    qdrant/qdrant:latest
