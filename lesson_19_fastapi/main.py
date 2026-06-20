import io
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse

from ml import upscale_image

app = FastAPI()

@app.get("/")
def greet():
    return {"message": "Hello! It's working!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upscale")
async def upscale(file: UploadFile, scale: int = Form(2)):
    image_bytes = await file.read()
    try:
        result_bytes = upscale_image(image_bytes, scale) # call ml function
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) # throw error if something goes wrong

    return StreamingResponse(io.BytesIO(result_bytes), # image in bytes -> send to frontend via HTTP
        media_type="image/png",)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)