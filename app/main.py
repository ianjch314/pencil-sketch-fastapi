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

    # Perform manual pencil sketch effect
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_inverted = 255 - img_gray
    img_inverted_blur = cv2.GaussianBlur(img_inverted, (21, 21), 0)
    img_inverted_blur = 255 - img_inverted_blur
    img_pencil_sketch = img_gray/img_inverted_blur*255

    # Output image to file
    filename_raw = file.filename.split('.')
    filename_pencil_sketch = f'{filename_raw[0]}_pencil_sketch.{filename_raw[1]}'
    cv2.imwrite(f'processed_img/{filename_pencil_sketch}', img_pencil_sketch)

    return FileResponse(
        path=f'processed_img/{filename_pencil_sketch}',
        filename=filename_pencil_sketch)