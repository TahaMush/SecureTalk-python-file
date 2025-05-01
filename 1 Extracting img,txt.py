from PIL import Image

def bin_to_text(binary):
    """Convert binary string to text."""
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

def extract_text(image_path):
    """Extract hidden text from an image using LSB steganography."""
    img = Image.open("C:/Users/Amir Jalil Khan/Desktop/New folder/output_image.png")
    binary_data = ""

    pixels = img.load()  # Access the pixels in the image

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]

            binary_data += str(r & 1)  # Extract LSB from red channel
            binary_data += str(g & 1)  # Extract LSB from green channel
            binary_data += str(b & 1)  # Extract LSB from blue channel

            # Check if end delimiter is found
            if '1111111111111110' in binary_data:
                binary_data = binary_data[:binary_data.index('1111111111111110')]
                break
        else:
            continue
        break

    text = bin_to_text(binary_data)
    print("Hidden text:", text)
    return text

# Usage example
extract_text('377_img.png')
