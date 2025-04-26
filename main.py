from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

MODEL = tf.keras.models.load_model("potato_disease_model.keras")
CLASS_NAMES = ["Early_Blight","Late_blight","Healthy"]




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend domain when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/ping")
async def ping():
    return "Hello World"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image,0)

    predction = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predction[0])]
    confidence = np.max(predction[0])

    return{
        'class':predicted_class,
        'confidence':float(confidence)
    }

    

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)