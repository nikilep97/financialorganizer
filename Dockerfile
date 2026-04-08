# Rakennetaan frontend
FROM node:20 AS build-stage
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Rakennetaan lopullinen kontti
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Kopioidaan rakennettu frontend build-vaiheesta
COPY --from=build-stage /frontend/dist ./dist
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]