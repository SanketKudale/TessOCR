import json
import cv2
import os

# Load the annotation file
with open('UAE_ID_Card.json', 'r') as file:
    annotations = json.load(file)

for key, value in annotations['_via_img_metadata'].items():
    # Extract image name and regions from the annotations
    image_name = value['filename']
    regions = value['regions']

    # Read the image
    image = cv2.imread(os.path.join('images/', image_name))

    for region in regions:
        # Get the bounding box coordinates
        x = region['shape_attributes']['x']
        y = region['shape_attributes']['y']
        width = region['shape_attributes']['width']
        height = region['shape_attributes']['height']

        # Extract the text region from the image
        text_region = image[y:y+height, x:x+width]

        # Save the extracted region
        save_path = os.path.join('utils/', f"{image_name}_region_{region['region_attributes']['name']}.png")
        cv2.imwrite(save_path, text_region)
