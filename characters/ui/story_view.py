from tkinter import ttk, constants, Toplevel, Entry, LEFT, RIGHT, END, font, Text, CURRENT, WORD
from entities.story import Story

class CharacterCreationDialog:
    def __init__(self, parent, view: "StoryView") -> None:
        self.view = view

        self.dialog = Toplevel(parent)
        self.dialog.title = "New Character"
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)

        self.name = None
        self.gender = None
        self.day = None
        self.month = None
        self.year = None
        self.height = None
        self.weight = None
        self.appearance = None
        self.personality = None
        self.history = None
        self.picture = None

        self.initialize_name()
        self.initialize_gender()
        self.initialize_birthday()
        self.initialize_height()
        self.initialize_weight()
        self.initialize_appearance()
        self.initialize_history()
        self.initialize_picture()
        self.initialize_trivia()

        self.ok_button = ttk.Button(self.dialog, text="Ok", command=None)

    def initialize_name(self) -> None:
        askname = ttk.Label(self.dialog, text="Name:")
        askname.pack()

        self.name = Entry(self.dialog)
        self.name.pack()

    def initialize_gender(self) -> None:
        askgender = ttk.Label(self.dialog, text="Gender:")
        askgender.pack()

        self.genderbox = ttk.Combobox(self.dialog, values=["Female", "Male", "Unknown"])
        self.genderbox.bind("<<ComboboxSelected>>", self.on_sex_change)
        self.genderbox.pack()

    def initialize_birthday(self) -> None:
        askbirthday = ttk.Label(self.dialog, text="Birthday:")
        askbirthday.pack()

        birthday_frame = ttk.Frame(self.dialog)
        birthday_frame.pack()

        empty_entry_font = font.Font(size=10, slant='italic')
        self.day = Entry(master=birthday_frame, fg='gray', font=empty_entry_font)
        self.month = Entry(master=birthday_frame, fg='gray', font=empty_entry_font)
        self.year = Entry(master=birthday_frame, fg='gray', font=empty_entry_font)

        self.day.insert(0, "Day")
        self.month.insert(0, "Month")
        self.year.insert(0, "Year")

        self.day.bind("<FocusIn>", lambda event=None, entry=self.day: self.on_date_click(entry=entry))
        self.month.bind("<FocusIn>", lambda event=None, entry=self.month: self.on_date_click(entry=entry))
        self.year.bind("<FocusIn>", lambda event=None, entry=self.year: self.on_date_click(entry=entry))

        self.day.pack(side=LEFT, padx=5)
        self.month.pack(side=LEFT, padx=5)
        self.year.pack(side=LEFT, padx=5)

    def initialize_height(self) -> None:
        askheight = ttk.Label(self.dialog, text="Height:")
        askheight.pack()

        self.height = Entry(master=self.dialog)
        self.height.pack()

    def initialize_weight(self) -> None:
        askweight = ttk.Label(self.dialog, text="Weight:")
        askweight.pack()

        self.weight = Entry(master=self.dialog)
        self.weight.pack()

    def initialize_appearance(self) -> None:
        askappearance = ttk.Label(self.dialog, text="Appearance:")
        askappearance.pack()

        self.appearance = Text(self.dialog, wrap=WORD, height=5, width=30)
        self.appearance.pack()
        self.appearance.bind("<KeyRelease>", lambda: self.move_line(text=self.appearance, event=None))

    def initialize_personality(self) -> None:
        askpersonality = ttk.Label(self.dialog, text="Personality:")
        askpersonality.pack()

        self.personality = Text(self.dialog, wrap=WORD, height=5, width=30)
        self.personality.pack()
        self.personality.bind("<KeyRelease>", lambda: self.move_line(text=self.personality, event=None))

    def initialize_history(self) -> None:
        askhistory = ttk.Label(self.dialog, text="History:")
        askhistory.pack()

        self.history = Text(self.dialog, wrap=WORD, height=5, width=30)
        self.history.pack()
        self.history.bind("<KeyRelease>", lambda: self.move_line(text=self.history, event=None))

    def initialize_picture(self) -> None:
        askpicture = ttk.Label(self.dialog, text="Select picture (not available yet!):")
        askpicture.pack()
        # Here goes code for selecting picture from PC

    def initialize_trivia(self) -> None:
        asktrivia = ttk.Label(self.dialog, text="Trivia:")
        asktrivia.pack()

        self.trivia = Text(self.dialog, wrap=WORD, height=5, width=30)
        self.trivia.pack()
        self.trivia.bind("<KeyRelease>", lambda: self.move_line(text=self.trivia, event=None))

    def move_line(self, text: Text, event=None) -> None:
        text.yview(CURRENT)
        text.config(height=text.count('1.0', END, 'lines'))

    def on_date_click(self, entry: Entry, event=None) -> None:
        if entry.get() == "Day" or entry.get() == "Month" or entry.get() == "Year":
            entry.delete(0, END)
            entry.config(fg='black', font=('Arial', 10, 'normal'))

    def on_sex_change(self, event) -> None:
        self.gender = self.genderbox.get()

    def close(self) -> None:
        self.dialog.destroy()

class StoryView:
    def __init__(self, root, story: Story, handle_main, stories: list[Story]) -> None:
        self._root = root
        self._handle_main = handle_main
        self._frame = None
        self.story = story
        self.stories = stories

        self._freeze = False
        self._temp = None

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
            command=self._character_creation_dialog
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

    def _character_creation_dialog(self) -> None:
        if not self._frozen():
            self.freeze()
            self._input_character_details()

    def _input_character_details(self):
        dialog = CharacterCreationDialog(self._root, self)
        self._wait_for_input(dialog, self._create_character)

    # Waits for user input before executing the rest of create story function
    def _wait_for_input(self, dialog: "CharacterCreationDialog", callback):
        def wait():
            if dialog.dialog.winfo_exists():
                self._root.after(100, wait)
            else:
                callback()
        wait()

    def _create_character(self) -> None:
        self.unfreeze()

    def freeze(self):
        self._freeze = True

    def unfreeze(self):
        self._freeze = False

    def _frozen(self) -> bool:
        return self._freeze
