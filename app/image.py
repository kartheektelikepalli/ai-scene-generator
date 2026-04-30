from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
import torch
import os
from PIL import Image

# 🔥 Load BOTH pipelines
text2img_pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to("mps")

img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to("mps")

NEGATIVE = """
multiple robots, duplicate, extra limbs, extra head, deformed,
mutated, different character, blurry, low quality, cropped, cut off
"""

def generate_image(prompt: str, idx: int):
    os.makedirs("output/images", exist_ok=True)

    generator = torch.Generator(device="mps").manual_seed(42)

    # 🔥 Add strong style anchor
    full_prompt = f"cartoon robot character, yellow body, clean design, {prompt}"

    if idx == 1:
        # ✅ TRUE generation (text → image)
        image = text2img_pipe(
            full_prompt,
            negative_prompt=NEGATIVE,
            height=768,
            width=768,
            num_inference_steps=30,
            guidance_scale=7.5,
            generator=generator
        ).images[0]

    else:
        # ✅ Maintain consistency using previous image
        init_image = Image.open(f"output/images/scene_{idx-1}.png").resize((768, 768))

        image = img2img_pipe(
            full_prompt,
            image=init_image,
            strength=0.75,
            guidance_scale=7.5,
            negative_prompt=NEGATIVE,
            generator=generator
        ).images[0]

    path = f"output/images/scene_{idx}.png"
    image.save(path)

    print(f"Saved: {path}")