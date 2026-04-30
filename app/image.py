import torch
import os
from PIL import Image
import numpy as np
import cv2

from diffusers import (
    StableDiffusionControlNetPipeline,
    ControlNetModel
)

# ---- LOAD MODELS ----
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny"
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet
)

pipe = pipe.to("mps")  # Mac GPU

# ---- EDGE DETECTOR ----
def create_canny(image: Image.Image):
    image = np.array(image)
    edges = cv2.Canny(image, 100, 200)
    edges = np.stack([edges]*3, axis=-1)
    return Image.fromarray(edges)

# ---- MAIN FUNCTION ----
def generate_image(prompt: str, idx: int):
    os.makedirs("output/images", exist_ok=True)

    generator = torch.Generator(device="mps").manual_seed(42)

    # Scene chaining
    if idx == 1:
        base = Image.new("RGB", (768, 768), "gray")  # NOT white
    else:
        base = Image.open(f"output/images/scene_{idx-1}.png")

    control_image = create_canny(base)

    full_prompt = f"""
    single small yellow robot,
    round head,
    big black eyes,
    cartoon style,
    clean background,
    centered,
    {prompt}
    """

    image = pipe(
        prompt=full_prompt,
        image=control_image,
        negative_prompt="multiple robots, duplicate, deformed, realistic human, messy background",
        num_inference_steps=30,
        generator=generator
    ).images[0]

    path = f"output/images/scene_{idx}.png"
    image.save(path)

    print(f"Saved: {path}")