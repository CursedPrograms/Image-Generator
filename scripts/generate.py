"""
generate.py - the Image-Generator without the questions, for other programs
(DREAM paints her dreams with it). Same SDXL-Turbo pipelines as
image_generator.py, driven by arguments instead of input().

    python scripts/generate.py --prompt "a red fox in snow" --out fox.jpg
    python scripts/generate.py --prompt "as a watercolour" --init in.jpg --out out.jpg
    python scripts/generate.py --job job.json      # many images, one model load
    python scripts/generate.py --download          # just fetch the model

A job file:
    {"prompt": "...", "keyframe": "key.jpg",            text-to-image (optional)
     "frames": [["in1.jpg", "out1.jpg"], ...],          image-to-image, each in -> out
     "strength": 0.5, "size": 512, "seed": 1234}

Each image is written as soon as it's done, so a job that gets killed part
way still leaves what it finished. --model picks another turbo model, e.g.
stabilityai/sd-turbo (smaller: fits a 4 GB GPU and 8 GB of RAM).
"""

import argparse
import json
import os
import sys

DEFAULT_MODEL = "stabilityai/sdxl-turbo"


def load_pipelines(model, device):
    import torch
    from diffusers import AutoPipelineForImage2Image, AutoPipelineForText2Image

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    t2i = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=dtype, variant="fp16")
    if device == "cuda":
        t2i.enable_model_cpu_offload()   # only the part that's working sits on the GPU
        t2i.enable_attention_slicing()
    else:
        t2i.to("cpu")
    t2i.set_progress_bar_config(disable=True)
    i2i = AutoPipelineForImage2Image.from_pipe(t2i)
    return t2i, i2i


def generator_for(seed):
    import torch
    return None if seed is None else torch.Generator("cpu").manual_seed(int(seed))


def text_to_image(t2i, prompt, size, seed, steps=1):
    return t2i(prompt=prompt, num_inference_steps=steps, guidance_scale=0.0,
               width=size, height=size, generator=generator_for(seed)).images[0]


def image_to_image(i2i, prompt, init_path, size, strength, seed, steps=2):
    from diffusers.utils import load_image
    init = load_image(init_path).convert("RGB").resize((size, size))
    # turbo models need steps * strength >= 1
    steps = max(steps, int(1 / max(strength, 0.05)) + 1)
    return i2i(prompt, image=init, num_inference_steps=steps, strength=strength,
               guidance_scale=0.0, generator=generator_for(seed)).images[0]


def save(img, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    img.save(path, quality=92)
    print(f"wrote {path}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt")
    ap.add_argument("--out")
    ap.add_argument("--init", help="image-to-image: the picture to start from")
    ap.add_argument("--strength", type=float, default=0.5)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--job", help="JSON job file (see above)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--download", action="store_true", help="fetch the model and exit")
    args = ap.parse_args()

    if args.download:
        from diffusers import AutoPipelineForText2Image
        AutoPipelineForText2Image.from_pretrained(args.model, variant="fp16")
        print(f"{args.model} is ready.")
        return 0

    if args.job:
        with open(args.job, encoding="utf-8") as f:
            job = json.load(f)
    elif args.prompt and args.out:
        job = {"prompt": args.prompt, "strength": args.strength, "size": args.size, "seed": args.seed}
        if args.init:
            job["frames"] = [[args.init, args.out]]
        else:
            job["keyframe"] = args.out
    else:
        ap.error("give --prompt and --out, or --job")

    t2i, i2i = load_pipelines(args.model, args.device)
    prompt, size, seed = job["prompt"], int(job.get("size", 512)), job.get("seed")
    strength = float(job.get("strength", 0.5))
    if job.get("keyframe"):
        save(text_to_image(t2i, prompt, size, seed), job["keyframe"])
    for src, dst in job.get("frames", []):
        save(image_to_image(i2i, prompt, src, size, strength, seed), dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
