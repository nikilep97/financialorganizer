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

@app.post("/api/categorize")
async def categorize_transactions(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Ainoastaan CSV tiedostot kelpaavat")

    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Tiedoston lukeminen epaonnistui")

    prompt = f"""
    Analysoi alla oleva CSV muotoinen tiliote.
    Kategorisoi jokainen ostos loogiseen kategoriaan kuten Ruoka, Asuminen, Viihde tai Liikenne.
    Laske lisaksi kunkin kategorian kokonaissumma.

    Palauta data tismalleen tassa JSON muodossa:
    {{
        "transactions": [
            {{
                "date": "Paivamaara",
                "description": "Ostoksen kuvaus",
                "amount": "Summa numerona",
                "category": "Kategoria"
            }}
        ],
        "summary": [
            {{
                "category": "Kategoria",
                "total": "Kategorian kokonaissumma numerona"
            }}
        ]
    }}

    Tiliote:
    {csv_text}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Tekoaly epaonnistui datan kasittelyssa")
    
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Jos polku ei ala kohdalla api, palauta index.html
        if not full_path.startswith("api"):
            return FileResponse("dist/index.html")
        raise HTTPException(status_code=404)