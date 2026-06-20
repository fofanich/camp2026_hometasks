import os

from dotenv import load_dotenv
load_dotenv()

import cv2
import numpy as np
import requests
import gradio as gr

# backend address; 
API_URL = os.getenv("API_URL", "http://[IP_ADDRESS]")

def run_upscale(image, scale_label):
    if image is None:
        raise gr.Error("Upload image first")

    scale = int(scale_label.replace("x", "")) 

    # Gradio gives RGB; OpenCV works with BGR
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    ok, buf = cv2.imencode(".png", bgr)
    image_bytes = buf.tobytes()

    # send the same request to the backend as through Swagger
    try:
        resp = requests.post(
            f"{API_URL}/upscale",
            files={"file": ("input.png", image_bytes, "image/png")},
            data={"scale": scale},
            timeout=60,
        )
    except requests.ConnectionError:
        raise gr.Error("Backend is not responding. Start uvicorn main:app first")

    if resp.status_code != 200:
        raise gr.Error(f"Backend error: {resp.text}")

    # response -> model image
    model_bgr = cv2.imdecode(np.frombuffer(resp.content, np.uint8), cv2.IMREAD_COLOR)
    model_rgb = cv2.cvtColor(model_bgr, cv2.COLOR_BGR2RGB)

    # "before": normal enlargement to the same size for comparison
    h, w = model_bgr.shape[:2]
    bicubic_rgb = cv2.cvtColor(
        cv2.resize(bgr, (w, h), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB
    )

    return (bicubic_rgb, model_rgb) # before, after for ImageSlider


with gr.Blocks() as demo:
    gr.Markdown("# Upscale images (FSRCNN)")

    image_input = gr.Image(type="numpy", label="Upload image")
    scale_choice = gr.Radio(["x2", "x4"], value="x2", label="Scale")
    run_button = gr.Button("Increase", variant="primary")

    slider = gr.ImageSlider(type="numpy", label="Left - normal enlargement, right - model")

    run_button.click(run_upscale, inputs=[image_input, scale_choice], outputs=slider)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0") # 0.0.0.0 to make it visible from Docker