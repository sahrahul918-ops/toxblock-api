from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import requests
from io import BytesIO
from PIL import Image
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Text NLP Model & Vectorizer
model = joblib.load('jigsaw_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# 2. Pre-Trained Zero-Shot Vision Model (OpenAI CLIP)
print("Loading zero-shot vision model...")
# Using CLIP for dynamic, text-based image classification
image_classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
print("Vision model ready!")

@app.post("/check_post")
async def check_post(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text:
        return {"is_toxic": False}
    transform_text = vectorizer.transform([text])
    prediction = model.predict(transform_text)[0]
    return {"is_toxic": bool(prediction)}

@app.post("/check_image")
async def check_image(request: Request):
    data = await request.json()
    url = data.get("url", "")
    
    if not url or not url.startswith("http"):
        return {"is_toxic": False}
        
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=3)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        
        # Dynamically define the classes we want the AI to look for
        candidate_labels = ["blood and gore", "weapon or knife", "safe and normal"]
        results = image_classifier(img, candidate_labels=candidate_labels)
        
        top_result = results[0]
        print(f"Image analysis: {top_result}") # Prints the highest confidence match to your terminal
        
        # Trigger blur if it detects our dangerous labels with >= 60% confidence
        toxic_labels = ["blood and gore", "weapon or knife"]
        is_toxic = (top_result["label"] in toxic_labels and top_result["score"] >= 0.60)
        
        return {"is_toxic": is_toxic}
    except Exception as e:
        print(f"Error inspecting image: {e}")
        return {"is_toxic": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)