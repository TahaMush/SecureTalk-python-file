import random
from PIL import Image


def int_to_bin(value, bits=8):
    """Convert an integer to a binary string of given length."""
    return format(value, f'0{bits}b')


def bin_to_int(binary):
    """Convert a binary string to an integer."""
    return int(binary, 2)


def embed_secret_image(cover_img_path, secret_img_path, output_img_path, seed=42):
    """
    Embed a secret RGB image into a cover RGB image using 4 LSBs and random slots.

    Args:
        cover_img_path (str): Path to the cover image.
        secret_img_path (str): Path to the secret image.
        output_img_path (str): Path to save the stego image.
        seed (int): Seed for random slot generation to ensure reproducibility.
    """
    # Open the cover and secret images
    cover_img = Image.open(cover_img_path).convert('RGB')
    secret_img = Image.open(secret_img_path).convert('RGB')  # Keep secret image in RGB

    cover_pixels = cover_img.load()
    secret_pixels = secret_img.load()
    cover_width, cover_height = cover_img.size
    secret_width, secret_height = secret_img.size

    if secret_width * secret_height > cover_width * cover_height - 2:
        raise ValueError("The cover image is too small to embed the secret image.")

    # Step 1: Store secret image dimensions in the first two pixels (R & G channels)
    cover_pixels[0, 0] = (
        secret_width // 256,  # High byte of width (R)
        secret_width % 256,  # Low byte of width (G)
        cover_pixels[0, 0][2]  # Keep original Blue (B)
    )
    cover_pixels[0, 1] = (
        secret_height // 256,  # High byte of height (R)
        secret_height % 256,  # Low byte of height (G)
        cover_pixels[0, 1][2]  # Keep original Blue (B)
    )

    # Step 2: Generate random slots for embedding
    random.seed(seed)
    available_slots = [(x, y) for y in range(cover_height) for x in range(cover_width) if y > 1]
    random_slots = random.sample(available_slots, secret_width * secret_height)

    # Step 3: Embed the secret image into the cover image
    for idx, (sx, sy) in enumerate(random_slots):
        secret_x = idx % secret_width
        secret_y = idx // secret_width

        # Get cover pixel (R, G, B)
        r, g, b = cover_pixels[sx, sy]

        # Get secret pixel (R, G, B)
        secret_r, secret_g, secret_b = secret_pixels[secret_x, secret_y]
        secret_r_bin, secret_g_bin, secret_b_bin = (
            int_to_bin(secret_r), int_to_bin(secret_g), int_to_bin(secret_b)
        )

        # Embed the first 4 bits of each channel of the secret image into the 4 LSBs of the cover image
        new_r = int_to_bin(r)[:-4] + secret_r_bin[:4]  # Embed 4 MSBs of secret R
        new_g = int_to_bin(g)[:-4] + secret_g_bin[:4]  # Embed 4 MSBs of secret G
        new_b = int_to_bin(b)[:-4] + secret_b_bin[:4]  # Embed 4 MSBs of secret B

        # Convert back to integers
        new_r = bin_to_int(new_r)
        new_g = bin_to_int(new_g)
        new_b = bin_to_int(new_b)

        # Update cover pixel with the modified values
        cover_pixels[sx, sy] = (new_r, new_g, new_b)

    # Save the resulting stego image
    cover_img.save(output_img_path, 'PNG')
    print(f"Stego image saved as {output_img_path}")


# Example usage
embed_secret_image("F:/Jalil/image2.png", "F:/Jalil/coin.jpg", "F:/Jalil/stego_image.png", seed=42)