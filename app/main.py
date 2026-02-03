from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import numpy as np
import cv2

app = FastAPI()

@app.post("/process-image")
async def process_image(file: UploadFile):
    # Read image as binary
    contents = await file.read()
    file.close()

    # Convert binary data to a NumPy array
    nparr = np.frombuffer(contents, np.uint8)
    
    # Convert NumPy array to OpenCV image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert color image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Output image to file
    filename_raw = file.filename.split('.')
    filename_gray = f'{filename_raw[0]}_gray.{filename_raw[1]}'
    cv2.imwrite(f'processed_img/{filename_gray}', img)

    return FileResponse(
        path=f'processed_img/{filename_gray}',
        filename=filename_gray)