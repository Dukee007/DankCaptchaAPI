import io
from flask import Flask, jsonify, request
import numpy as np
import requests
import torch
from PIL import Image
import cv2
from skimage.metrics import structural_similarity
from ultralytics import YOLO


def similarity(answer_emoji, captcha_emoji):
    answer_emoji_with_alpha = cv2.cvtColor(answer_emoji, cv2.COLOR_BGR2BGRA)
    mask = (answer_emoji_with_alpha[..., 3] > 0).astype(np.uint8) * 255
    answer_emoji_with_alpha = cv2.merge([answer_emoji_with_alpha[..., 0:3], mask])
    downscaled_answer_emoji = cv2.resize(
        answer_emoji_with_alpha,
        (captcha_emoji.shape[1], captcha_emoji.shape[0]),
        interpolation=cv2.INTER_AREA,
    )

    sim, _ = structural_similarity(
        downscaled_answer_emoji,
        captcha_emoji,
        full=True,
        data_range=255,
        multichannel=True,
        channel_axis=-1,
    )
    return sim


def crop_images(img_pil):
    model = YOLO("best.pt")
    result = model.predict(
        img_pil,
        imgsz=640,
        save_crop=True,
        project="runs/predict",
        name="exp",
        save_conf=True,
    )[0]

    masks = result.masks.data
    boxes = result.boxes.data
    clss = boxes[:, 5]
    people_indices = torch.where(clss == 0)
    people_masks = masks[people_indices]
    people_mask = torch.any(people_masks, dim=0).int() * 255

    people_mask_np = people_mask.cpu().numpy()
    pil_mask = Image.fromarray(people_mask_np).convert("L")
    img_pil = img_pil.convert("RGBA")
    pil_mask_resized = pil_mask.resize(img_pil.size, Image.ANTIALIAS)
    img_pil.putalpha(pil_mask_resized)

    cropped_images = []

    for idx, box in enumerate(boxes[people_indices]):
        x1, y1, x2, y2, _, _ = box
        x1, y1, x2, y2 = map(
            int, (x1.item(), y1.item(), x2.item(), y2.item())
        )  # Convert tensor coordinates to integers
        cropped = img_pil.crop((x1, y1, x2, y2))
        cropped_cv2 = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGBA2BGRA)
        cropped_images.append(cropped_cv2)
        cropped.save(f"runs/predict/exp/segment_{idx}.png", "PNG")

    return cropped_images


api = Flask(__name__)

@api.route('/solve', methods=['POST'])
def parse_request():
  data = request.get_json()
  captcha_url = data['captcha']
  opts = data['opts']

  response = requests.get(captcha_url)

  image_data = io.BytesIO(response.content)
  img_pil = Image.open(image_data)

  segmented_emojis = crop_images(img_pil)

  similarities = [0] * 5

  for button_idx, emoji in opts.items():
    button_idx = int(button_idx)
    response = requests.get(emoji)
    emoji_data = io.BytesIO(response.content)
    emoji_pil = Image.open(emoji_data)
    emoji_np = np.asarray(emoji_pil)
    emoji_bgr = cv2.cvtColor(emoji_np, cv2.COLOR_RGB2BGR)

    for segmented_emoji in segmented_emojis:
        similarities[button_idx] += similarity(emoji_bgr, segmented_emoji)

  print(similarities)
  best_match_index = similarities.index(max(similarities))

  data = {
    'best_match_index': best_match_index,
    'similarity': similarities[best_match_index]
  }
  return jsonify(data)

if __name__ == '__main__':
    api.run(debug=False, port=42003)