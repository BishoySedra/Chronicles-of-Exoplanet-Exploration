# build image
docker build -t nasa_ai_api_image .

# run container
docker run -d -p 8000:8000 --name nasa_ai_api_container nasa_ai_api_image