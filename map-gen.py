from PIL import Image

frames = []


def bmp_to_matrix_array(path):
    """
    Converts a bitmap image to a matrix array.

    Args:
        image_path (str): The path to the bitmap image file.

    Returns:
        list: A matrix array representing the image, where each element
        is a string of 'b' (black) or '.' (white) pixels.
    """
    img = Image.open(path)
    img = img.convert("1")  # Convert to black and white

    width, height = img.size
    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            sub_img = img.crop((x, y, x+1, y+1))
            row.append(
                ''.join(['.' if pixel == 255 else 'b' for pixel in sub_img.getdata()]))
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


def save_matrix_array(the_frames):
    """
    Saves the matrix array in a specific format to a text file.

    Args:
        the_frames (list): The matrix array to be saved.

    Returns:
        None
    """
    with open('map.js', 'w', encoding='utf-8') as f:
        f.write("const b=\"b\";setLegend([\"b\",bitmap`\n")
        for _ in range(15):
            f.write("0000000000000000\n")
        f.write("0000000000000000`]);let level=0;let framerate=" +
                str((1000 / (25 / frame_rate)))+"\n")

        f.write("const max_level = " + str(len(the_frames) - 1) + "\n")
        f.write("const levels = [\n")
        for p, matrix in enumerate(the_frames):
            if p != 0:
                for n, row in enumerate(matrix):
                    if n == 0:
                        f.write(f'  map`{"".join(row)}\n')
                    if n < len(matrix) - 1:
                        f.write(f'     {"".join(row)}\n')
                    else:
                        f.write(f'     {"".join(row)}`,\n')
        f.write("]\n")
        f.write(
            "setMap(levels[level]);var tick=setInterval(()=>{level<max_level&&(setMap(levels[level]),level++)},framerate);")
        f.close()


images = int(input("enter the number of the frames you want to see: "))
frame_rate = int(input("enter the frame rate you want to see: "))

for i in range(1,  (images * frame_rate), frame_rate):
    image_path = f"frames/resized-mdm/output_{i:04d}.bmp"
    frames.append(bmp_to_matrix_array(image_path))

# print_matrix_array(frames)

input("Press Enter to save the map to a text file...")
save_matrix_array(frames)
print("Done!")
