from PIL import Image

def text_to_bin(text):
    """Convert text to a binary string."""
    return ''.join(format(ord(char), '08b') for char in text)

def hide_text(image_path, output_path, text):
    """Hide text in an image using LSB steganography."""
    img = Image.open(image_path)
    binary_text = text_to_bin(text) + '1111111111111110'  # Add delimiter to mark the end
    binary_text_index = 0
    
    pixels = img.load()  # Access the pixels in the image
    #print(type(pixels))
    "3*W*H"
    for y in range(img.height):
        for x in range(img.width):
            if binary_text_index >= len(binary_text):  # Stop if message is fully embedded
                break

            r, g, b = pixels[x, y]
            print(r,g,b)



            r = (r & ~1) | int(binary_text[binary_text_index])  # Embed bit in the red channel
            print(r & ~1)
            binary_text_index += 1


            if binary_text_index < len(binary_text):
                g = (g & ~1) | int(binary_text[binary_text_index])  # Embed bit in the green channel
                binary_text_index += 1

            if binary_text_index < len(binary_text):
                b = (b & ~1) | int(binary_text[binary_text_index])  # Embed bit in the blue channel
                binary_text_index += 1

            pixels[x, y] = (r, g, b)

        if binary_text_index >= len(binary_text):
            break

    img.save(output_path)
    print("Text hidden in image successfully!")

# Usage example
hide_text('F:/Jalil/new python prac/coin.jpg', '5_img.png', 'hello')


