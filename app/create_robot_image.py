from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to("mps")

prompt = """
small yellow cartoon robot,
round head,
big black eyes,
simple limbs,
full body,
centered,
plain white background
"""

image = pipe(prompt, num_inference_steps=30).images[0]
image.save("assets/robot.png")