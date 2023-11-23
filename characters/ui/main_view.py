from tkinter import ttk, constants, Toplevel, Entry
from services.story_service import story_service, Story
import getpass
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir)
sys.path.append(root_dir)


# A class to manage user input of story name and description.

class StoryDialog:
    def __init__(self, parent, view: "MainView") -> None:
        self.view = view

        self.dialog = Toplevel(parent)
        self.dialog.title("New story")
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)

        self.askname = ttk.Label(self.dialog, text="Name:")
        self.askname.pack()

        self.name = Entry(self.dialog)
        self.name.pack()

        self.askdesc = ttk.Label(self.dialog, text="Description (optional):")
        self.askdesc.pack()

        self.desc = Entry(self.dialog)
        self.desc.pack()

        self.ok_button = ttk.Button(self.dialog, text="Ok", command=self.enter)
        self.ok_button.pack()

    def enter(self):
        name = self.name.get()
        desc = self.desc.get()

        if name == '':
            return
        if desc == '':
            desc = None

        self.view._temp = (name, desc)

        self.dialog.destroy()
        return (name, desc)

    def close(self):
        self.dialog.destroy()


class MainView:
    def __init__(self, root, stories: list[Story], handle_story) -> None:
        self._root = root
        self._frame = None
        self._handle_story = handle_story
        self.stories = stories

        # Stores last input from dialog
        self._temp = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        name = getpass.getuser()
        welcome_text = ttk.Label(master=self._frame, text=f"Welcome, {name}!")
        clear_stories_button = ttk.Button(master=self._frame,
                                          text="Delete all stories",
                                          command=self._clear_stories)
        create_story_button = ttk.Button(master=self._frame,
                                         text="New Story",
                                         command=self._story_creation_dialog)

        welcome_text.pack()
        if len(self.stories) == 0:
            no_stories = ttk.Label(
                master=self._frame, text="You don't have any stories yet. Why not create one?")
            no_stories.pack()

        clear_stories_button.pack()
        create_story_button.pack()

        self._initialize_stories_list()

    def _initialize_story(self, story: Story):
        story_frame = ttk.Frame(master=self._frame)
        story_button = ttk.Button(
            master=story_frame,
            text=story.name,
            command=lambda: self._handle_story(story=story)
        )
        story_button.pack()
        story_frame.pack(fill=constants.X)

    def _initialize_stories_list(self):
        stories = story_service.get_stories()
        for story in stories:
            self._initialize_story(story=story)
        self.pack()

    # No error message yet on errors
    # NEXT TIME Add so user can't click buttons when in dialog
    def _story_creation_dialog(self):
        self._input_story_details()

    def _create_story(self):
        if not self._temp or not self._temp[0]:
            print(self._temp)
            print("Something's wrong while creating story")
            return
        new_story = story_service.create_story(
            name=self._temp[0], desc=self._temp[1])
        # Clears _temp
        self._temp = None
        if new_story:
            self._initialize_story(story=new_story)

    # Reloads the page completely. May be a better solution
    # I'll find out later.
    def _clear_stories(self):
        story_service.clear_stories()
        self.destroy()
        self._initialize()

    # Calls dialog window and waits for input
    def _input_story_details(self):
        dialog = StoryDialog(self._root, self)
        self._wait_for_input(dialog, self._create_story)

    # Waits for user input before executing the rest of create story function
    def _wait_for_input(self, dialog: "StoryDialog", callback):
        def wait():
            if dialog.dialog.winfo_exists():
                self._root.after(100, wait)
            else:
                callback()
        wait()
