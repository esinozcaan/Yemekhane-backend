
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import uvicorn
from io import BytesIO
from fastapi.responses import FileResponse
from ultralytics import YOLO
from PIL import Image

app = FastAPI()


PORT = 3001
BASE_DIR = os.path.expanduser("~")  

# Model dosya yolunu belirle
MODEL_PATH = os.path.join(BASE_DIR, "Desktop", "best.pt") 

# Modeli yükle ve hata kontrolü ekle
def load_my_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model dosyası {MODEL_PATH} bulunamadı.")
    model = YOLO(MODEL_PATH)
    return model

try:
    model = load_my_model()
    print("Model başarıyla yüklendi.")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    model = None


# Dinamik olarak JSON dosyasının yolunu belirleyelim

PLANTS_JSON_PATH = os.path.join(BASE_DIR, "Desktop", "food.json") 

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model yüklenemedi. Lütfen daha sonra tekrar deneyin."}

    try:
        file_bytes = await file.read()  # Dosyayı bayt olarak oku
        image = Image.open(BytesIO(file_bytes)).convert("RGB") 

        results = model.predict(image, conf=0.25)
        detections = {}
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls.item())
                class_name = model.names[class_id]
                detections[class_name] = detections.get(class_name, 0) + 1

        return {"detections": detections}
    except Exception as e:
        return {"error": f"Bir hata oluştu: {e}"}


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(f"Server will be available at PORT: {PORT}")
    print("=" * 50 + "\n")
    uvicorn.run("main:app", host='0.0.0.0', port=PORT, reload=True)
