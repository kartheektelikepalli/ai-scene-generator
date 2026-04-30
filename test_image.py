import warnings
warnings.filterwarnings("ignore")
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

pipe = pipe.to("mps")  # Mac GPU

image = pipe(
    "single robot, one character only, solo, isolated subject, full body robot, centered composition, clean plain background, no other objects, colorful cartoon style, consistent character design, vibrant colors",
    negative_prompt="multiple robots, two robots, group, collage, grid, cropped, cut off, partial body, extra limbs, background clutter",
    height=768,
    width=768
).images[0]
image.save("test.png")
print("Saved test.png")