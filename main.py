import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

# API-reitit pitää määritellä ennen staattisia tiedostoja
@app.post("/api/categorize")
async def categorize_transactions(file: UploadFile = File(...)):
    # ... (pidä aiempi koodi samana tässä) ...
    pass

# Tarjoile React-sovelluksen staattiset tiedostot dist-kansiosta
# Varmista, että dist-kansio on kopioitu Docker-konttiin
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse("dist/index.index.html")