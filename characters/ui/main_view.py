import getpass
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir)
sys.path.append(root_dir)

from entities.story import Story
from repositories.db_management import db
from tkinter import ttk, constants

class MainView:
    def __init__(self, root, stories: list[Story], handle_story) -> None:
        self._root = root
        self._frame = None
        self._handle_story = handle_story
        self.stories = stories

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        name = getpass.getuser()
        welcome_text = ttk.Label(master=self._frame, text=f"Welcome, {name}!")
        create_story_button = ttk.Button(master=self._frame,
                                         text="New Story",
                                         command=self._create_story)

        welcome_text.pack()
        if len(self.stories) == 0:
            no_stories = ttk.Label(master=self._frame, text="You don't have any stories yet. Why not create one?")
            no_stories.pack()

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
        stories = db.get_stories()
        for story in stories:
            self._initialize_story(story=story)
        self.pack()

    def _create_story(self):
        new_story_id = db.create_story(name="Dummy Story3", desc=None)
        new_story = Story(id=new_story_id, name="Dummy Story3", desc=None)
        self._initialize_story(story=new_story)