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

model = Unet(
    backbone='resnet34',  # or any other pretrained backbone
    in_channels=3,
    num_classes=1,
    pretrained=True
)
#%%
parameters_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\feature_parameters'

for name, param in model.named_parameters(): #
    targeted_layers = ['encoder.conv1.weight']
    if param.requires_grad:
        if name not in targeted_layers:
            continue
        
        print(f"Layer: {name}")
        print(f"Shape: {param.shape}")
        # print(f"Values: {param.data}")
        # print("-----------------------------------")
        
        #numpy
        # Convert parameter data to numpy array
        param_data = param.data.cpu().numpy()
        filename = os.path.join(parameters_path, f"{name.replace('.', '_')}.npy")
        np.save(filename, param_data)
        print(f"Saved parameter data to {filename}")
        
        #text
        filename = os.path.join(parameters_path, f"{name.replace('.', '_')}.txt")
        # Save the parameter data to a text file
        with open(filename, 'w') as f:
            f.write(f"Layer: {name}\n")
            f.write(f"Shape: {param.shape}\n")
            f.write("Values:\n")
            np.savetxt(f, param_data.reshape(-1, param_data.shape[-1]), fmt='%.6f')
            print(f'saved parameter to text file: {filename}')
print("parameter saving done")

#%%
impage_path =  r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Archive\Non_Zero\All\image\BA_OR_21_tile_308.png' 
image = Image.open(impage_path)

# Convert image to numpy array
img_array = np.array(image)

# Print array shape
print(f"Array shape: {img_array.shape}")

# Print data type
print(f"Data type: {img_array.dtype}")

# Print min and max values
print(f"Min value: {img_array.min()}")
print(f"Max value: {img_array.max()}")

# Print mean value
print(f"Mean value: {img_array.mean()}")
#%%
#%%
from torchvision import transforms

greyscale = 1 #
# Assuming you have an image loaded as 'image'
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485*greyscale, 0.456*greyscale, 0.406*greyscale], std=[0.229*greyscale, 0.224*greyscale, 0.225*greyscale])
])
input_tensor = transform(image).unsqueeze(0)  # Add batch dimension
#%%
#%%
print(f"Tensor shape: {input_tensor.shape}")
print(f"Tensor type: {input_tensor.dtype}")
print(f"Min value: {input_tensor.min().item()}")
print(f"Max value: {input_tensor.max().item()}")
print(f"Mean value: {input_tensor.mean().item()}")
plt.figure(figsize=(10, 5))
plt.hist(input_tensor.numpy().flatten(), bins=50)
plt.title('Histogram of input tensor values')
plt.xlabel('Pixel values')
plt.ylabel('Frequency')
plt.show()
#%%
#%%
# Create hooks to capture feature maps
feature_maps = {}

def hook_fn(module, input, output):
    feature_maps[module] = output.detach()

for name, module in model.named_modules():
    if isinstance(module, torch.nn.Conv2d):
        module.register_forward_hook(hook_fn)
#%%
#%%
with torch.no_grad():
    output = model(input_tensor)
#%%
#%%
mask = torch.sigmoid(output).squeeze().numpy()
#mask = np.where(mask > 0.5, 1, 0) ### optional

#  Display the original image and the segmentation mask
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

#resize image
base_width = 256
# w_percent = (base_width / float(image.size[0]))
# h_size = int((float(image.size[1]) * float(w_percent)))

# Resize the image
resized_image = image.resize((base_width, base_width), Image.LANCZOS)

# Original image
ax1.imshow(resized_image)
ax1.set_title('Original Image')
ax1.axis('off')

# Segmentation mask
ax2.imshow(mask, cmap='jet')
ax2.set_title('Segmentation Mask')
ax2.axis('off')

plt.tight_layout()
plt.show()

# , overlay the mask on the original image
overlay = resized_image.copy()
overlay = np.array(overlay)
mask_rgb = np.stack([mask]*3, axis=-1)
overlay = overlay * (1 - mask_rgb) + mask_rgb * 255

plt.figure(figsize=(8, 8))
plt.imshow(overlay.astype(np.uint8))
plt.title('Segmentation Overlay')
plt.axis('off')
plt.show()
#%%
#%%
import matplotlib.pyplot as plt

def plot_feature_maps(feature_maps, num_features=5):
    feature_map_path = r''
    for layer, feature_map in feature_maps.items():
        if feature_map.dim() == 4:  # Ensure it's a 4D tensor (batch, channels, height, width)
            fig, axes = plt.subplots(1, num_features, figsize=(15, 3))
            fig.suptitle(f"Feature Maps for {layer}")
            for i in range(num_features):
                if i < feature_map.size(1):
                    axes[i].imshow(feature_map[0, i].cpu().numpy(), cmap='viridis')
                    axes[i].axis('off')
            plt.show()
            


def save_feature_maps(feature_maps, feature_map_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\feature_map' ):
    layer_count_to_save = 2
    cur_layer_count = 0
    for layer, feature_map in feature_maps.items():
        if cur_layer_count > layer_count_to_save:
            break
        
        if feature_map.dim() == 4:  # Ensure it's a 4D tensor (batch, channels, height, width)
            for i in range(feature_map.size(1)):
                filename= os.path.join(feature_map_path, f"fm_{layer}_{i}.png")
                feature_map_numpy = feature_map[0, i].cpu().numpy() 
                
                # Normalize the feature map to 0-255
                feature_map_normalized = cv2.normalize(feature_map_numpy, None, 0, 255, cv2.NORM_MINMAX)

                # Convert to uint8 (required for saving as an image)
                feature_map_uint8 = feature_map_normalized.astype(np.uint8)

                # Save the image
                cv2.imwrite(filename, feature_map_uint8)
                print(f'saving feature map: {filename}')
        
        cur_layer_count += 1
    print('All feature maps saved!')
  

save_feature_maps(feature_maps)
#%%

