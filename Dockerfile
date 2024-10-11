# Use the ollama/ollama image as the base image
FROM ollama/ollama

# Set the working directory (optional)
WORKDIR /app

# Start the ollama service, pull the model, and stop the process in one command
RUN nohup ollama serve & sleep 5 && ollama pull llama3.2

# Expose port 11434 for external access
EXPOSE 11434