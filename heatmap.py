import os
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def generate_heatmap_local(json_path, image_path, object_filter):
    with open(json_path, "r") as f:
        data = json.load(f)

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Base image not found.")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    heat = np.zeros((height, width), dtype=np.float32)

    for hit in data.get("hits", {}).get("hits", []):
        messages = (
            hit.get("_source", {}).get("deepstream-msg", []) +
            hit.get("fields", {}).get("deepstream-msg", [])
        )

        for entry in messages:
            parts = entry.split("|")
            if len(parts) >= 7 and parts[5] == object_filter:
                x_min, y_min, x_max, y_max = map(float, parts[1:5])
                x = int((x_min + x_max) / 2)
                y = int((y_min + y_max) / 2)
                if 0 <= x < width and 0 <= y < height:
                    heat[y, x] += 1

    if np.max(heat) == 0:
        raise ValueError(f"None '{object_filter}' found.")

    heat_blurred = gaussian_filter(heat, sigma=10)
    norm_heat = heat_blurred / np.max(heat_blurred)

    plt.figure(figsize=(12, 8))
    plt.imshow(image_rgb, alpha=0.5)
    plt.imshow(norm_heat, cmap='jet', alpha=0.6, interpolation='bilinear')
    plt.axis("off")

    os.makedirs("static", exist_ok=True)
    out_path = "static/output.png"
    plt.savefig(out_path, bbox_inches="tight", pad_inches=0)
    plt.close()

    return out_path
