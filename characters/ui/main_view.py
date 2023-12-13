import tkinter as tk
from tkinter import ttk, constants, Toplevel, Entry
from services.story_service import story_service, Story
import getpass
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir)
sys.path.append(root_dir)


class StoryDialog:
    """A class to manage user input of story name and description.
    """

    def __init__(self, parent: tk.Tk, view: "MainView") -> None:
        self.view = view
        self._parent = parent

        self.dialog = Toplevel(parent)
        self.dialog.title("New story")

        self.askname = ttk.Label(self.dialog, text="Name:")
        self.askname.pack()

        self.name = Entry(self.dialog)
        self.name.pack()

        self.askdesc = ttk.Label(self.dialog, text="Description (optional):")
        self.askdesc.pack()

        self.desc = tk.Text(
            self.dialog, wrap=tk.WORD, height=5, width=30)
        self.desc.pack()

        self.ok_button = ttk.Button(self.dialog, text="Ok", command=self.enter)
        self.ok_button.pack()

    def enter(self):
        """Saves temporary data from user input and closes dialog window.

        Name is obligatory.

        """

        name = self.name.get()
        desc = self.desc.get("1.0", tk.END).strip()

        if name == '' or len(name) > 100 or len(desc) > 100:
            return
        if desc == '':
            desc = None

        self.view._temp = (name, desc)

        self.close()

    def close(self):
        """Closes dialog window.
        """

        self.dialog.destroy()


class MainView:
    def __init__(self, root, stories: list[Story], handle_story) -> None:
        self._root = root

        self._frame = None
        self._stories_frame = None

        self._handle_story = handle_story
        self.stories = stories

        # Can't click anything while dialog window is open
        self._frozen = False

        # Stores last input from dialog
        self._temp = None

        self._initialize()

    def pack(self):
        """Packs the whole view.
        """

        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys all widgets in current view.
        """

        self._frame.destroy()

    def _initialize_welcome_frame(self):
        """Initializes frame that contains user's name (from their computer) and New Story button.
        """

        welcome_frame = ttk.Frame(master=self._frame)
        welcome_frame.pack()

        name = getpass.getuser()
        welcome_text = ttk.Label(master=welcome_frame,
                                 text=f"Welcome, {name}!")
        welcome_text.pack()

        if len(self.stories) == 0:
            no_stories = ttk.Label(
                master=welcome_frame, text="You don't have any stories yet. Why not create one?")
            no_stories.pack()

        create_story_button = ttk.Button(
            master=welcome_frame,
            text="New Story",
            command=self._story_creation_dialog
        )
        create_story_button.pack(pady=10)

    def _initialize_endpage(self):
        """Initializes story count and button for deleting all stories.
        """

        endpage_frame = ttk.Frame(master=self._frame)
        endpage_frame.pack(pady=10)

        count = ttk.Label(
            master=endpage_frame,
            text=f"You have {story_service.count_stories()} stories."
        )
        count.pack()

        clear_stories_button = ttk.Button(
            master=endpage_frame,
            text="Delete all stories",
            command=self._clear_stories
        )

        clear_stories_button.pack()

    def _initialize(self):
        """Initializes main elements of the view.
        """

        self._frame = ttk.Frame(master=self._root)

        self._initialize_welcome_frame()
        self._initialize_stories_list()
        self._initialize_endpage()

    def _initialize_story(self, story: Story):
        """Initializes single story frame from Story object.

        Args:
            story (Story): Story to be viewed.
        """

        story_frame = ttk.Frame(master=self._stories_frame)
        story_button = ttk.Button(
            master=story_frame,
            text=story.name,
            command=lambda: self._handle_story(story=story)
        )
        story_button.pack()
        story_frame.pack(fill=constants.X)

    def _initialize_stories_list(self):
        """Initializes frame containing all stories.
        """

        if not self._stories_frame:
            self._stories_frame = ttk.Frame(master=self._frame)
        self._stories_frame.pack()
        stories = story_service.get_stories()
        for story in stories:
            self._initialize_story(story=story)
        self.pack()

    def _story_creation_dialog(self):
        """Checks if the window is frozen, if not, initializes story creation dialog.
        """

        if not self._frozen:
            self._frozen = True
            self._input_story_details()

    def _create_story(self):
        """Creates story from temporary data that was saved by story creation dialog.
        """

        self._frozen = False
        if not self._temp or not self._temp[0]:
            return
        new_story = story_service.create_story(
            name=self._temp[0], desc=self._temp[1])
        self._temp = None
        if new_story:
            self._initialize_story(story=new_story)
            self._reload()

    def _clear_stories(self):
        """Deletes all stories and reloads the view.
        """

        if not self._frozen:
            story_service.clear_stories()
            self._reload()

    def _reload(self):
        """Completely reloads the view.
        """

        self._stories_frame = None
        self.destroy()
        self._initialize()

    def _input_story_details(self):
        """Calls dialog window and waits for input.
        """

        dialog = StoryDialog(self._root, self)
        self._wait_for_input(dialog, self._create_story)

    def _wait_for_input(self, dialog: "StoryDialog", callback):
        """Waits for user input before executing the rest of story creation function.

        Args:
            dialog (StoryDialog): Story dialog that the function is waiting to be closed.
            callback (function): Calls this function when the dialog is closed.
        """

        def wait():
            if dialog.dialog.winfo_exists():
                self._root.after(100, wait)
            else:
                callback()
        wait()
