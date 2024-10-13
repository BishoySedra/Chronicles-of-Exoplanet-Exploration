# Use the ollama/ollama image as the base image
FROM ollama/ollama

# Set the working directory
WORKDIR /app

# Pull the llama3.2 model during the build process
RUN ollama pull llama3.2

# Expose port 11434 for external access
EXPOSE 11434

# Start the server
CMD ["ollama", "serve"]
