import os


class Repository:
    def __init__(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(current_dir, "../library/avatars/")

    def delete_all_avatars(self) -> None:
        img_list = os.listdir(self._path)
        img_paths = [os.path.join(self._path, img) for img in img_list]
        for path in img_paths:
            if "default.png" not in path:
                os.remove(path=path)

    def delete_avatar(self, name: str) -> None:
        img_path = self._path + f"{name}.png"
        os.remove(path=img_path)

    def get_image_path(self, name: str) -> str:
        """Responsible for giving full path to image.

        Args:
            name: Image name

        Returns:
            string with full path    
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, name)
        return img_path


rep = Repository()
