from tkinter import ttk, constants
from repositories.db_management import db
from entities.story import Story

class StoryView:
    def __init__(self, root, story: Story, handle_main, stories: list[Story]) -> None:
        self._root = root
        self._handle_main = handle_main
        self._frame = None
        self.story = story
        self.stories = stories

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        # As these were created for testing purposes, right now it kind of works,
        # but bugs out when switching between main view and story view and only
        # shows the id of a last story. In future this will be based on database
        # and not variables, so I won't be fixing this issue at the time...
        label = ttk.Label(master=self._frame, text=f"This is a page for story number {self.story.id} which name is {self.story.name}.")
        total_stories = ttk.Label(master=self._frame, text=f"You have {db.count_stories()} stories in total.")
        button = ttk.Button(
            master=self._frame,
            text="Go back",
            command=lambda: self._handle_main()
        )
        
        label.pack()
        total_stories.pack()
        button.pack()