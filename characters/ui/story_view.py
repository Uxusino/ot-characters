from tkinter import ttk, constants
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

    def _initialize_heading(self):
        heading_frame = ttk.Frame(master=self._frame)
        heading_frame.pack()

        story_name = self.story.get_name()
        head = ttk.Label(
            master=heading_frame,
            text=story_name
        )
        head.pack()

        story_desc = self.story.get_desc()
        desc = ttk.Label(
            master=heading_frame,
            text=story_desc
        )
        desc.pack()

        character_button = ttk.Button(
            master=heading_frame,
            text="New Character",
            command=None
        )
        character_button.pack()

    def _initialize_characters(self):
        pass

    def _initialize_endpage(self):
        endpage_frame = ttk.Frame(master=self._frame)
        endpage_frame.pack(pady=10)

        button = ttk.Button(
            master=endpage_frame,
            text="Go back",
            command=lambda: self._handle_main()
        )
        button.pack()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_heading()
        self._initialize_characters()
        self._initialize_endpage()
