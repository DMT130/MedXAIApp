from preprocessing import read_normal_image, read_dcm_image, preprocess_normal, preprocess_dcm, predict, im_show_dcm, im_show_normal
from fastapi import FastAPI, File, UploadFile
import base64
import cv2
import numpy as np
import uuid
from io import BytesIO
from fastapi.responses import FileResponse, Response, StreamingResponse, JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

origins = [
    "https://medxaiapp-frontend-fc2s4lwtyq-uc.a.run.app",
    "http://localhost:3000",
    "http://localhost"
]


middleware = [
    Middleware(CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
]

app = FastAPI(middleware=middleware)

SIZE = (1024, 1024)

IMAGEDIR = "pngimages/"

@app.get('/')
async def front_page():
    return {'front':'Home'}

@app.post("/file/")
async def predict_image(file: UploadFile = File(...)):
    extention = file.filename.split('.')[-1]
    file.filename = f"{uuid.uuid4()}.{extention}"
    contents = await file.read()

    #with open(f"{IMAGEDIR}{file.filename}", "wb") as buffer:
    #    buffer.write(contents)

    if extention in ("jpg", "jpeg", "png"):
        Nimage = read_normal_image(contents)
        image = preprocess_normal(Nimage)
        info, bbs, labels = predict(image)
        showim = im_show_normal(Nimage)
        showim = np.array(showim)
        try:
            H, W = showim.shape
            showim = np.stack([showim, showim, showim], axis=2)
        except:
            H, W, _ = showim.shape
        for i,j in zip(bbs, info):
            xmin, ymin, w, h = i
            widh = int(w)
            heigh = int(h)
            X = int(xmin)
            Y = int(ymin)
            showim = cv2.rectangle(showim, (X, Y), (widh, heigh), (0, 0, 255), 2)
            showim = cv2.putText(showim, j, (X, Y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        #path = f"{IMAGEDIR}{file.filename}"
        res, im_png = cv2.imencode(".png", showim)
        with open("image.png", "wb") as buffer:
            encoded_image_string = base64.b64encode(im_png)
        payload = {
            "mime" : "bytes",
            "image": encoded_image_string,
            "classes":info,
            "BoundingBox":(np.array(bbs).astype('int')).tolist()
        }
        #return StreamingResponse(BytesIO(im_png.tobytes()), media_type="image/png")
        return payload
        #return Response()
    elif extention in ['dicom', 'dcm', 'dicm','dcom']:
        #image = read_dcm_image(f"{IMAGEDIR}{file.filename}")
        Nimage = read_dcm_image(contents)
        H, W = Nimage.shape
        show = im_show_dcm(Nimage)
        showim = np.array(show)
        showim = np.stack([showim, showim, showim], axis=2)
        image = preprocess_dcm(Nimage)
        info, bbs, labels = predict(image)
        for i,j in zip(bbs, info):
            xmin, ymin, w, h = i
            widh = int(w)
            heigh = int(h)
            X = int(xmin)
            Y = int(ymin)
            showim = cv2.rectangle(showim, (X, Y), (widh, heigh), (0, 0, 255), 2)
            showim = cv2.putText(showim, j, (X, Y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        res, im_png = cv2.imencode(".png", showim)
        with open("image.png", "wb") as buffer:
            encoded_image_string = base64.b64encode(im_png)
        payload = {
            "mime" : "bytes",
            "image": encoded_image_string,
            "classes":list(np.array(info).flatten()),
            "BoundingBox":(np.array(bbs).astype('int')).tolist()
        }
        return payload
