import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()
model = genai.GenerativeModel("gemini-2.5-flash")

@app.post("/api/categorize")
async def categorize_transactions(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Vain CSV tiedostot ovat sallittuja")

    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Tiedoston lukeminen epäonnistui")

    prompt = f"""
    Analysoi alla oleva CSV muotoinen tiliote.
    Kategorisoi jokainen ostos loogiseen kategoriaan kuten Ruoka, Asuminen, Viihde tai Liikenne.
    Laske lisäksi kunkin kategorian kokonaissumma.

    Palauta data tismalleen tässä JSON muodossa:
    {{
        "transactions": [
            {{
                "date": "Päivämäärä",
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
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Tekoäly epäonnistui datan käsittelyssä")