#%%
import torch
from backbones_unet.model.unet import Unet
import matplotlib.pyplot as plt
from torchvision import transforms
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import os
import cv2
import torch.nn as nn
from torchvision import transforms

def generate_feature_maps(image_path, feature_map_path):
    model = Unet(
        backbone='resnet34',  # or any other pretrained backbone
        in_channels=3,
        num_classes=1,
        pretrained=True
    )
    
    greyscale = 1 #
    
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485*greyscale, 0.456*greyscale, 0.406*greyscale], std=[0.229*greyscale, 0.224*greyscale, 0.225*greyscale])
    ])
            
    target_channel_name ='fm_Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)_31.png'

    files = [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]
    for idx, file in enumerate(files):
        print(f'processing {idx+1} of {len(files)} -----------------')
        input_image = os.path.join(image_path, file)
        #name, extension = os.path.splitext(file_name)
        output_image =  os.path.join(feature_map_path, file)

        image = Image.open(input_image)
        input_tensor = transform(image).unsqueeze(0)  # Add batch dimension

        feature_maps = {}
        
        def hook_fn(module, input, output):
            feature_maps[module] = output.detach()

        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                module.register_forward_hook(hook_fn)

        with torch.no_grad():
            output = model(input_tensor)

        print(f'feature_maps size = {len(feature_maps)}')
        
        layer_count_to_save = 1
        cur_layer_count = 0
        for layer, feature_map in feature_maps.items():
            if cur_layer_count > layer_count_to_save:
                break
            
            if feature_map.dim() == 4:  # Ensure it's a 4D tensor (batch, channels, height, width)
                for i in range(feature_map.size(1)):
                    filename= f'fm_{layer}_{i}.png'
                    if target_channel_name != filename:
                        continue
                    feature_map_numpy = feature_map[0, i].cpu().numpy() 
                    
                    # Normalize the feature map to 0-255
                    feature_map_normalized = cv2.normalize(feature_map_numpy, None, 0, 255, cv2.NORM_MINMAX)

                    # Convert to uint8 (required for saving as an image)
                    feature_map_uint8 = feature_map_normalized.astype(np.uint8)

                    resized_image = cv2.resize(feature_map_uint8, (512, 512))
                    # Save the image
                    cv2.imwrite(output_image, resized_image)
                    print(f'saving feature map: {output_image}')
            
            cur_layer_count += 1
    print('All feature maps saved!')
        
if __name__ == "__main__":
    # Specify the folder containing input images and the output folder for feature maps
    image_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Example_image\images' 
    feature_map_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\feature_map'
    
    # Ensure the output directory exists
    os.makedirs(feature_map_path, exist_ok=True)
    
    # Generate and save feature maps for all images in the folder
    generate_feature_maps(image_path, feature_map_path)

#%%
