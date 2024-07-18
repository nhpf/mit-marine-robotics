import argparse
import os

from fish_detection import load_model, get_grounding_output, load_image, plot_boxes_to_image

# cfg
input_dir = 'input'
image_path = f'{input_dir}/photo.png'
text_prompt = 'fish'
output_dir = 'output'
box_threshold = 0.35
text_threshold = 0.25
token_spans = None
model = load_model("GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", "GroundingDINO/weights/groundingdino_swint_ogc.pth")
# make dir
os.makedirs(output_dir, exist_ok=True)
os.makedirs(input_dir, exist_ok=True)
# load image
image_pil, image = load_image(image_path)
cpu_only = True
# load model

# visualize raw image
image_pil.save(os.path.join(output_dir, "raw_image.jpg"))

# set the text_threshold to None if token_spans is set.
if token_spans is not None:
    text_threshold = None
    print("Using token_spans. Set the text_threshold to None.")


# run model
print('run model')

boxes_filt, pred_phrases = get_grounding_output(
    model, image, text_prompt, box_threshold, text_threshold, cpu_only=cpu_only, token_spans=eval(f"{token_spans}")
)

# visualize pred
size = image_pil.size
pred_dict = {
    "boxes": boxes_filt,
    "size": [size[1], size[0]],  # H,W
    "labels": pred_phrases,
}
# import ipdb; ipdb.set_trace()
image_with_box = plot_boxes_to_image(image_pil, pred_dict)[0]
print(os.path.join(output_dir, "pred.jpg"))
image_with_box.save(os.path.join(output_dir, "pred.jpg"))