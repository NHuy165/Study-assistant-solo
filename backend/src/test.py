from backend.src.AI_services.utils import embed

text = "FastAPI is a modern web framework for building APIs with Python"

response = embed(text)

print(response)
