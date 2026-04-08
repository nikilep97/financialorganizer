#  Rakennetaan frontend
FROM node:20 AS build-stage
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

# Rakennetaan sovellus
RUN npm run build

# Rakennetaan lopullinen Python-kontti
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopioidaan taustajärjestelmän koodi
COPY . .

# Kopioidaan rakennettu käyttöliittymä oikeaan paikkaan
COPY --from=build-stage /frontend/dist ./dist

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]