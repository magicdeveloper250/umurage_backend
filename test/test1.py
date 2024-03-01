import requests

image = requests.get(
    "https://res.cloudinary.com/dqlv0vkoe/image/upload/magic%20developerf763fa28-4860-4201-a68a-2bb63c8895c12024-02-28_14:37:02.135030"
)
print(image.content)
