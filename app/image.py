import torch
import os
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
from controlnet_aux import MidasDetector

# ---- LOAD CONTROLNET ----
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-depth",
    torch_dtype=torch.float32
)

# ---- LOAD PIPELINE ----
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float32
)

pipe = pipe.to("mps")

# ---- OPTIMIZATION ----
pipe.enable_attention_slicing()
pipe.vae.enable_slicing()

# ---- LOAD IP-ADAPTER ----
pipe.load_ip_adapter(
    "h94/IP-Adapter",
    subfolder="models",
    weight_name="ip-adapter_sd15.bin"
)

# ---- LOAD REFERENCE IMAGE ----
ref_image = load_image("assets/robot.png")

# ---- DEPTH ESTIMATOR ----
depth_estimator = MidasDetector.from_pretrained("lllyasviel/Annotators")

def generate_image(prompt: str, idx: int):
    os.makedirs("output/images", exist_ok=True)

    generator = torch.Generator(device="mps").manual_seed(42 + idx)

    # ---- CREATE DEPTH MAP FROM REFERENCE ----
    depth_image = depth_estimator(ref_image)

    full_prompt = f"""
    same exact robot from reference image,
    identical design, identical proportions,
    yellow and white robot, blue eyes,
    do not redesign character,

    {prompt},

    cinematic lighting, high quality
    """

    negative_prompt = """
    different robot, redesign, new character,
    different head, different body proportions,
    extra limbs, deformed, blurry
    """

    image = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        image=depth_image,  # ControlNet input
        ip_adapter_image=ref_image,
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=generator,
        cross_attention_kwargs={"scale": 0.75}
    ).images[0]

    path = f"output/images/scene_{idx}.png"
    image.save(path)

    print(f"Saved: {path}")