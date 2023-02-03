from PIL import Image

def image_to_ascii(image_path):
    # Open the image
    image = Image.open(image_path)

    # Resize the image to reduce the number of characters
    width, height = image.size
    new_width = int(width * 0.3)
    new_height = int(height * 0.3)
    image = image.resize((new_width, new_height))

    # Convert the image to grayscale
    image = image.convert("L")

    # Define a mapping from grayscale values to ASCII characters
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    chars = [ascii_chars[int(value / 255 * (len(ascii_chars) - 1))] for value in range(0, 256)]

    # Create the ASCII art by mapping each pixel to an ASCII character
    ascii_art = ""
    for y in range(new_height):
        for x in range(new_width):
            ascii_art += chars[image.getpixel((x, y))]
        ascii_art += "\n"

    # Return the ASCII art
    return ascii_art

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    ascii_art = image_to_ascii(image_path)
    print(ascii_art)
