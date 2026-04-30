import torch
import os
from diffusers import StableDiffusionPipeline
from diffusers.utils import load_image

# ---- LOAD PIPELINE ----
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
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


def generate_image(prompt: str, idx: int):
    os.makedirs("output/images", exist_ok=True)

    generator = torch.Generator(device="mps").manual_seed(42 + idx)

    full_prompt = f"""
        same robot as reference image,
        yellow and white humanoid robot,
        round rectangular head,
        two large blue circular eyes,
        smooth plastic body,
        short limbs, rounded joints,
        consistent character design,

        {prompt},

        cinematic lighting, 3D render, high quality
        """
    negative_prompt = """
        different robot, multiple robots, different character,
        blue robot, red robot, humanoid variation,
        extra limbs, deformed, mutated,
        blurry, low quality
        """

    image = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        ip_adapter_image=ref_image,
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=generator,
        cross_attention_kwargs={"scale": 0.75}  # 🔥 KEY FIX
    ).images[0]

    path = f"output/images/scene_{idx}.png"
    image.save(path)

    print(f"Saved: {path}")