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
                                         command=self.create_story)

        welcome_text.pack()
        if len(self.stories) == 0:
            no_stories = ttk.Label(master=self._frame, text="You don't have any stories yet. Why not create one?")
            no_stories.pack()

        create_story_button.pack()

        # Show all stories
        for s in self.stories:
            story = ttk.Button(master=self._frame,
                               text=s.name,
                               command=lambda: self._handle_story(story_id=s.id))
            story.pack()

    # It's a mess I have to change the ids the other way around
    def create_story(self):
        new_story_id = len(self.stories) + 1
        new_story = Story(id=new_story_id, name="Dummy Story", desc=None)
        new_story_button = ttk.Button(master=self._frame,
                               text=new_story.name,
                               command=lambda: self._handle_story(story_id=new_story_id))
        db.create_story(name=new_story.name, desc=new_story.desc)
        new_story_button.pack()