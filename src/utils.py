import os
from typing import Any
from uuid import uuid4

import requests


def get_image_price(params: dict[str, Any]) -> float | None:
    if params.get("image_model") == "dall-e-2":
        match params.get("image_size"):
            case "256x256":
                return 0.016
            case "512x512":
                return 0.018
            case "1024x1024":
                return 0.02

    if params.get("image_model") == "dall-e-3":
        if params.get("image_quality") == "standard" and params.get("image_resolution") == "1024x1024":
            return 0.04
        if params.get("image_quality") == "hd" and set(params["image_resolution"].split("x")) == set(["1024", "1792"]):
            return 0.12
        else:
            return 0.08

    return None


def download_file(url: str) -> str:
    filename = os.path.join(os.getcwd(), "img", str(uuid4()) + ".jpg")

    with open(filename, "wb") as f:
        response = requests.get(url, timeout=5)
        f.write(response.content)

    return filename
