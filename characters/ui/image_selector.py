import os
from tkinter import filedialog
from PIL import Image


def select_image() -> tuple | None:
    """Opens image selection window.

    If nothing is selected, returns None.

    Returns:
        tuple: Contains Image object and its name.
    """

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Images", "*.png;*.jpg;*.jpeg;")]
    )

    if file_path:
        image_path = file_path
        img_name = os.path.basename(file_path)
        img = Image.open(image_path)
        img = img.resize((125, 125))
        return (img, img_name)
    return None
