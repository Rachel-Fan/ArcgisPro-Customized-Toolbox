import torch
from backbones_unet.model.unet import Unet
import matplotlib.pyplot as plt
from torchvision import transforms
from PIL import Image
import os
import cv2
import numpy as np
import torch.nn as nn

def generate_feature_maps(image_path, feature_map_path):
    # Initialize the U-Net model with ResNet-34 backbone
    model = Unet(
        backbone='resnet34',  # Or another backbone of choice
        in_channels=3,
        num_classes=1,
        pretrained=True
    )
    
    greyscale = 1  # Multiplier for normalization, can adjust this as needed
    
    # Define the transformation pipeline for input images
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize to 256x256
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize(mean=[0.485 * greyscale, 0.456 * greyscale, 0.406 * greyscale], 
                             std=[0.229 * greyscale, 0.224 * greyscale, 0.225 * greyscale])  # Normalize
    ])
    
    # Get a list of all files in the image folder
    files = [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]
    
    for idx, file in enumerate(files):
        print(f'Processing {idx+1} of {len(files)}: {file}')
        input_image_path = os.path.join(image_path, file)
        image_name, _ = os.path.splitext(file)  # Extract image name (without extension)
        
        # Create a folder for each image in the output directory
        image_feature_map_dir = os.path.join(feature_map_path, image_name)
        os.makedirs(image_feature_map_dir, exist_ok=True)

        # Load and preprocess the image
        image = Image.open(input_image_path)
        input_tensor = transform(image).unsqueeze(0)  # Add batch dimension

        # Dictionary to hold feature maps
        feature_maps = {}

        # Define a hook function to capture feature maps during forward pass
        def hook_fn(module, input, output):
            feature_maps[module] = output.detach()

        # Register hooks for all Conv2d layers in the model
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                module.register_forward_hook(hook_fn)

        # Perform a forward pass through the model to generate feature maps
        with torch.no_grad():
            _ = model(input_tensor)

        print(f'Feature maps size = {len(feature_maps)}')

        # Loop through each layer and extract feature maps
        for layer, feature_map in feature_maps.items():
            if feature_map.dim() == 4:  # Check if it's a 4D tensor (batch, channels, height, width)
                num_channels = feature_map.size(1)  # Get the number of channels

                # Iterate over all channels in the feature map
                for i in range(num_channels):
                    filename = f'fm_{layer}_{i}.png'
                    
                    # Convert the feature map to numpy
                    feature_map_numpy = feature_map[0, i].cpu().numpy()
                    
                    # Normalize the feature map to 0-255 range
                    feature_map_normalized = cv2.normalize(feature_map_numpy, None, 0, 255, cv2.NORM_MINMAX)
                    feature_map_uint8 = feature_map_normalized.astype(np.uint8)

                    # Resize the feature map to 512x512 for easier visualization
                    resized_image = cv2.resize(feature_map_uint8, (512, 512))

                    # Save the feature map to the appropriate folder
                    output_image_path = os.path.join(image_feature_map_dir, filename)
                    cv2.imwrite(output_image_path, resized_image)
                    print(f'Saving feature map: {output_image_path}')

    print('All feature maps saved!')

if __name__ == "__main__":
    # Specify the folder containing input images and the output folder for feature maps
    image_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Example_image\images' 
    feature_map_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Example_image\feature_map'
    
    # Ensure the output directory exists
    os.makedirs(feature_map_path, exist_ok=True)
    
    # Generate and save feature maps for all images in the folder
    generate_feature_maps(image_path, feature_map_path)
