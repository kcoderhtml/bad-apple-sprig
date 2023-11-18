from PIL import Image

image_start = 2
images = 500
frames = []

def bmp_to_matrix_array(path):
    """
    Converts a bitmap image to a matrix array.

    Args:
        image_path (str): The path to the bitmap image file.

    Returns:
        list: A matrix array representing the image, where each element is a string of 'b' (black) or '.' (white) pixels.
    """
    img = Image.open(path)
    img = img.convert("1")  # Convert to black and white

    width, height = img.size
    matrix = []

    for y in range(height):  # Assuming each matrix is 18x24 pixels
        row = []
        for x in range(width):
            sub_img = img.crop((x, y, x+1, y+1))
            row.append(''.join(['.' if pixel == 255 else 'b' for pixel in sub_img.getdata()]))
        matrix.append(row)

    return matrix

def print_matrix_array(the_frames):
    """
    Prints the matrix array in a specific format.

    Args:
        the_frames (list): The matrix array to be printed.

    Returns:
        None
    """
    print("const max_level = " + str(len(the_frames) - 1))
    print("const levels = [")
    for p, matrix in enumerate(the_frames):
        if p != 0:
            for n, row in enumerate(matrix):
                if n == 0:
                    print(f'  map`{"".join(row)}')
                if n < len(matrix) - 1:
                    print(f'     {"".join(row)}')
                else:
                    print(f'     {"".join(row)}`,')
    print("]")


for i in range(image_start, image_start + (images * 2), 2):
    image_path = f"frames/resized/output_{i:04d}.bmp"
    frames.append(bmp_to_matrix_array(image_path))

print_matrix_array(frames)