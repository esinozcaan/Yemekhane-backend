# uvicorn main:app

import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO
from fastapi.responses import FileResponse
from ultralytics import YOLO
from PIL import Image
import json
from calculate import *
from model import *
import traceback

app = FastAPI()


PORT = 3001
BASE_DIR = os.path.expanduser("~")

MODEL_PATH = "best.pt"


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

with open("food.json", "r", encoding="utf-8") as file:
    food_items = json.load(file)


@app.post("/predict", response_model=ResponseModel)
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model yüklenemedi. Lütfen daha sonra tekrar deneyin."}

    try:
        file_bytes = await file.read()
        image = Image.open(BytesIO(file_bytes)).convert("RGB")

        temp_image_path = "uploaded_image.jpg"
        image.save(temp_image_path)

        results = model.predict(source=temp_image_path, conf=0.25)

        # name randomizer
        random_name = np.random.randint(0, 1000000)

        detections = {}
        for result in results:
            result.save(f"{random_name}.png")
            for cls in result.boxes.cls.tolist():
                class_name = model.names[int(cls)]
                if class_name in detections:
                    detections[class_name] += 1
                else:
                    detections[class_name] = 1

        result, menu = calculate_result(detections, food_items)

        annotated_image_path = f"{random_name}.png"

        return ResponseModel(
            items=result,
            menu=menu,
            annotated_image_path=annotated_image_path,
        )

    except Exception as e:
        tb = traceback.format_exc()
        return ResponseModel(error=str(tb))


@app.get("/{image_path}")
async def get_image(image_path):

    return FileResponse(f"{image_path}")

