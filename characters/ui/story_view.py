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
        label = ttk.Label(
            master=self._frame, text=f"This is a page for story number {self.story.get_id()} which name is {self.story.name}.")
        total_stories = ttk.Label(
            master=self._frame, text=f"You have {db.count_stories()} stories in total.")
        button = ttk.Button(
            master=self._frame,
            text="Go back",
            command=lambda: self._handle_main()
        )

        label.pack()
        total_stories.pack()
        button.pack()
