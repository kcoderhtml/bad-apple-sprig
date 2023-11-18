from PIL import Image

image_path = "frames/resized/output_0140.bmp"
image_start = 140
image_end = 149

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

def print_matrix_array(matrix):
    """
    Prints the matrix as a JavaScript array of strings.

    Args:
        matrix (list): The matrix to be printed.

    Returns:
        None
    """
    print("const levels = [")
    for i, row in enumerate(matrix):
        if i == 0:
            print(f'  map`{"".join(row)}')
        if i < len(matrix) - 1:
            print(f'     {"".join(row)}')
        else:
            print(f'     {"".join(row)}`,')
    print("]")

matrix_array = bmp_to_matrix_array(image_path)
print_matrix_array(matrix_array)