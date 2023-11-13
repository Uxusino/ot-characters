import getpass

from tkinter import ttk, constants

class MainView:
    def __init__(self, root, stories, handle_story) -> None:
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
        if self.stories == 0:
            no_stories = ttk.Label(master=self._frame, text="You don't have any stories yet. Why not create one?")
            no_stories.pack()

        create_story_button.pack()

        # Show all dummy stories that are already there
        for x in range(1, self.stories+1):
            story = ttk.Button(master=self._frame,
                               text =f"Story {x}: Tadaa!",
                               command=lambda: self._handle_story(story_id=x, stories=self.stories))
            story.pack()

    def create_story(self):
        self.stories += 1
        new_story_id = self.stories
        new_story = ttk.Button(master=self._frame,
                               text=f"Story {new_story_id}: Tadaa!",
                               command=lambda: self._handle_story(story_id=new_story_id, stories=self.stories))
        new_story.pack()