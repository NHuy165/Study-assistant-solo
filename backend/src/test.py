from backend.src.services.study.utils import embed

text = "FastAPI is a modern web framework for building APIs with Python"

response = embed(text)

print(response)
