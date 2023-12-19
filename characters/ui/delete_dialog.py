import tkinter as tk
from tkinter import ttk
from services.story_service import story_service, Story
from services.character_service import char_service, Character


class DeleteDialog:
    def __init__(self, parent: tk.Tk, handle_func, _object: Story | list[Story] | Character, _type: str) -> None:
        """Deletion dialog that asks user if they're sure to delete something.

        Args:
            parent (tk.Tk): Root
            handle_func (function): Functon that redirects user to other view
            object (Story | list[Story] | Character): Object/objects to be deleted
            type (str): What is being deleted. Possible types: 'story', 'all_stories', 'character'
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title = "Delete?"
        self._handle_func = handle_func
        self._object = _object
        self._type = _type

        tk.Label(
            master=self.dialog,
            text=f"Are you sure?"
        ).pack()

        buttons_frame = tk.Frame(
            master=self.dialog
        )
        buttons_frame.pack()

        ttk.Button(
            master=buttons_frame,
            text="Yes",
            command=self._delete
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            master=buttons_frame,
            text="No",
            command=self._close
        ).grid(row=0, column=1, padx=5)

    def _close(self):
        self.dialog.destroy()

    def _delete(self):
        if self._type == 'story':
            story_service.delete_story(self._object.story_id)
            self._close()
            self._handle_func()
        elif self._type == 'all_stories':
            story_service.clear_stories()
            self._close()
        elif self._type == 'character':
            char_service.delete_character(self._object)
            self._handle_func()
            self._close()
        else:
            self._close()
