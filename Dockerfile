# Optional Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files into the container.
COPY . /app

# Install dependencies without cache for a smaller image.
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app.
EXPOSE 8000

# Set a production environment variable (optional).
ENV ENV=production

# Run the FastAPI app using Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
