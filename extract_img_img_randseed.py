import random
from PIL import Image


def int_to_bin(value, bits=8):
    """Convert an integer to a binary string of given length."""
    return format(value, f'0{bits}b')


def bin_to_int(binary):
    """Convert a binary string to an integer."""
    return int(binary, 2)


def extract_secret_image(stego_img_path, output_secret_img_path, seed=42):
    """
    Extract the secret RGB image from a stego RGB image using 4 LSBs and random slots.

    Args:
        stego_img_path (str): Path to the stego image.
        output_secret_img_path (str): Path to save the extracted secret image.
        seed (int): Seed for random slot generation to ensure reproducibility.
    """
    # Open the stego image
    stego_img = Image.open(stego_img_path).convert('RGB')
    stego_pixels = stego_img.load()
    cover_width, cover_height = stego_img.size

    # Step 1: Retrieve the secret image dimensions from the first two pixels
    secret_width = stego_pixels[0, 0][0] * 256 + stego_pixels[0, 0][1]
    secret_height = stego_pixels[0, 1][0] * 256 + stego_pixels[0, 1][1]

    # Step 2: Generate the same random slots used during embedding
    random.seed(seed)
    available_slots = [(x, y) for y in range(cover_height) for x in range(cover_width) if y > 1]
    random_slots = random.sample(available_slots, secret_width * secret_height)

    # Step 3: Create a new RGB image for the secret image
    secret_img = Image.new('RGB', (secret_width, secret_height))
    secret_pixels = secret_img.load()

    # Step 4: Extract the secret image bits from the stego image
    for idx, (sx, sy) in enumerate(random_slots):
        secret_x = idx % secret_width
        secret_y = idx // secret_width

        # Get the stego pixel (R, G, B)
        r, g, b = stego_pixels[sx, sy]

        # Extract the 4 MSBs from the 4 LSBs
        secret_r_bin = int_to_bin(r)[-4:] + '0000'  # Extract 4 LSBs and pad with zeros
        secret_g_bin = int_to_bin(g)[-4:] + '0000'  # Extract 4 LSBs and pad with zeros
        secret_b_bin = int_to_bin(b)[-4:] + '0000'  # Extract 4 LSBs and pad with zeros

        # Convert binary to integer
        secret_r = bin_to_int(secret_r_bin)
        secret_g = bin_to_int(secret_g_bin)
        secret_b = bin_to_int(secret_b_bin)

        # Set the pixel value in the secret image
        secret_pixels[secret_x, secret_y] = (secret_r, secret_g, secret_b)

    # Save the extracted secret image
    secret_img.save(output_secret_img_path, 'PNG')
    print(f"Extracted secret image saved as {output_secret_img_path}")


# Example usage
extract_secret_image("F:/Jalil/stego_image.png", "F:/Jalil/extracted_secret_image.png", seed=42)