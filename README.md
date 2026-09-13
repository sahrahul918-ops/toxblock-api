# ToxBlock AI 🛡️

A real-time, AI-powered browser extension designed to dynamically detect and blur toxic text and explicit images on WhatsApp Web. 

## 🚀 Features
* **Real-Time DOM Scanning:** Utilizes JavaScript `MutationObserver` to continuously scan dynamically loaded React elements on WhatsApp Web without impacting browser performance.
* **Multimodal AI Detection:** 
  * **Text:** Processes incoming chat bubbles through a custom NLP pipeline (`jigsaw_model.pkl` & TF-IDF vectorizer).
  * **Images:** Uses OpenAI's **CLIP** (`clip-vit-base-patch32`) zero-shot classification to inspect image URLs for weapons, blood, and gore.
* **Click-to-Reveal:** Implements brute-force CSS injection to bypass strict WhatsApp stylesheets, allowing users to click a masked message to temporarily reveal it.
* **Seamless Backend:** A high-performance asynchronous **FastAPI** server that communicates with the frontend via secure **ngrok** tunnels.

## 🛠️ Tech Stack
* **Frontend:** JavaScript (ES6+), WebExtensions API, HTML5/CSS3
* **Backend:** Python 3, FastAPI, Uvicorn, ngrok
* **Machine Learning:** PyTorch, Hugging Face Transformers, Scikit-learn, Pillow (PIL)

## ⚙️ How it Works
1. The extension injects `content.js` into WhatsApp Web, targeting specific message container classes (e.g., `.selectable-text`).
2. Text and image URLs are forwarded to `background.js`, which sends an async POST request to the FastAPI server via an ngrok tunnel.
3. The AI processes the payload. If confidence thresholds are exceeded (e.g., > 35% for weapons), a `True` flag is returned.
4. The extension applies an overriding grey mask and blur filter to the specific DOM element.
