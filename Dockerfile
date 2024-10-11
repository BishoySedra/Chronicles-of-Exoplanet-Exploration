# Use the ollama/ollama image as the base image
FROM ollama/ollama

# Set the working directory (optional, adjust as needed)
WORKDIR /app

# Expose port 11434 for external access
EXPOSE 11434

RUN docker exec -it ollama /bin/sh

# Pull the llama3.1 model during the build process
RUN ollama pull llama3.1

# Run the ollama service with the llama3.1 model
CMD ["ollama", "run", "llama3.1", "--port", "11434"]
