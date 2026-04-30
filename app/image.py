from diffusers import StableDiffusionPipeline
import torch
import os

# load once (important)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)
pipe = pipe.to("mps")

def generate_image(prompt: str, idx: int):
    os.makedirs("output/images", exist_ok=True)

    generator = torch.Generator(device="mps").manual_seed(42)


    image = pipe(
        prompt,
        negative_prompt="multiple robots, duplicate, extra limbs, extra head, deformed, mutated, different character",
        height=768,
        width=768,
        generator=generator
    ).images[0]

    path = f"output/images/scene_{idx}.png"
    image.save(path)

    print(f"Saved: {path}")