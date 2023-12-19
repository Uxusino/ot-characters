"""Class for managing characters' profile picture files.

    Returns:
        Repostitory: Repository that is responsible for local file control.
"""

import os
import string
import random
from PIL import Image


class Repository:
    def __init__(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(current_dir, "../library/avatars/")

    def _generate_name(self) -> str:
        """Generates random name for new image.

        Returns:
            str: Randomized string.
        """
        chars = string.ascii_letters + string.digits
        name = ''.join(random.sample(chars, k=10))
        return name

    def save_image(self, image: Image) -> str:
        """Saves image to image folder and returns image's name.

        Args:
            image (Image): Image object to be saved.

        Returns:
            str: Image's new name.
        """

        new_name = self._generate_name()
        filedir = self._path + f"{new_name}.png"

        image.save(filedir, format="png")
        return new_name

    def delete_all_avatars(self) -> None:
        """Deletes all character images except for default picture.
        """
        img_list = os.listdir(self._path)
        img_paths = [os.path.join(self._path, img) for img in img_list]
        for path in img_paths:
            if "default.png" not in path:
                os.remove(path=path)

    def delete_avatars(self, avatars: list[str]) -> None:
        """Deletes avatars which name matches images in avatars list.

        Args:
            avatars (list[str]): List with image names to be deleted
        """

        for avatar in avatars:
            self.delete_avatar(avatar)

    def delete_avatar(self, name: str) -> None:
        """Deletes a certain character image.

        Args:
            name (str): Name of the picture to be deleted.
        """
        img_path = self._path + f"{name}.png"
        os.remove(path=img_path)

    def get_file_path(self, name: str) -> str:
        """Responsible for giving full path to a certain file.

        Args:
            name: Image name

        Returns:
            str: Full path to the file.  
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, name)
        return file_path


rep = Repository()
