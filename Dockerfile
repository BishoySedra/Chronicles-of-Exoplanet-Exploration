# Use the ollama/ollama image as the base image
FROM ollama/ollama

# Set the working directory
WORKDIR /app

# Expose port 11434 (Heroku dynamically assigns this though)
EXPOSE 11434

# Pull the llama3.2 model during the build process
RUN ollama serve & ollama pull llama3.2

# Ensure the app binds to the $PORT variable Heroku provides
CMD ["sh", "-c", "ollama serve --port $PORT"]
