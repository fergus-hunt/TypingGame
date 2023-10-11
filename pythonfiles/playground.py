import rembg
import numpy as np
from PIL import Image

# Load the input image


def get_images( path, size):
        for i in range(size): 
            if i < 10: 
                image_path = f"{path}/tile00{i}.png"
            else: 
                image_path = f"{path}/tile0{i}.png"
            input_image = Image.open(image_path)
            input_array = np.array(input_image)
            output_array = rembg.remove(input_array)

# Create a PIL Image from the output array
            output_image = Image.fromarray(output_array)

            # Save the output image
            output_image.save(f'{image_path}')
                    
            # Convert the input image to a numpy array

get_images("images/gameboy-character", 32)