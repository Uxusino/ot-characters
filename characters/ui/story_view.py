import tkinter as tk
import os
from tkinter import ttk, font, constants
from entities.story import Story
from services.character_service import char_service, Character


class CharacterCreationDialog:
    def __init__(self, parent, view: "StoryView") -> None:
        self.view = view

        self.dialog = tk.Toplevel(parent)
        self.dialog.title = "New Character"
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)

        self.name = None
        self.gender = None
        self.day = None
        self.month = None
        self.year = None
        self.age = None
        self.height = None
        self.weight = None
        self.appearance = None
        self.personality = None
        self.history = None
        self.picture = None
        self.trivia = None

        self.initialize_name()
        self.initialize_gender()
        self.initialize_birthday()
        self.initialize_age()
        self.initialize_height()
        self.initialize_weight()
        self.initialize_appearance()
        self.initialize_personality()
        self.initialize_history()
        self.initialize_picture()
        self.initialize_trivia()

        ok_button = ttk.Button(self.dialog, text="Ok", command=self.enter)
        ok_button.pack()

    # Saves tuple (name, gender, (day, month, year), height, weight, appearance, personality, history, picture, trivia)
    def enter(self) -> None:
        name = self.name.get()
        gender = self.gender
        day = self.day.get()
        month = self.month.get()
        year = self.year.get()
        age = self.age.get()
        height = self.height.get()
        weight = self.weight.get()
        appearance = self.appearance.get("1.0", tk.END)
        personality = self.personality.get("1.0", tk.END)
        history = self.history.get("1.0", tk.END)
        picture = None
        trivia = self.trivia.get("1.0", tk.END)

        res_tuple = (
            name,
            gender,
            (day, month, year),
            age,
            height,
            weight,
            appearance,
            personality,
            history,
            picture,
            trivia
        )

        self.view._temp = res_tuple

        self.close()

    def initialize_name(self) -> None:
        askname = ttk.Label(self.dialog, text="Name:")
        askname.pack()

        self.name = tk.Entry(self.dialog)
        self.name.pack()

    def initialize_gender(self) -> None:
        askgender = ttk.Label(self.dialog, text="Gender:")
        askgender.pack()

        self.genderbox = ttk.Combobox(
            self.dialog, values=["Female", "Male", "Unknown"])
        self.genderbox.bind("<<ComboboxSelected>>", self.on_sex_change)
        self.genderbox.pack()

    def initialize_birthday(self) -> None:
        askbirthday = ttk.Label(self.dialog, text="Birthday:")
        askbirthday.pack()

        birthday_frame = ttk.Frame(self.dialog)
        birthday_frame.pack()

        empty_entry_font = font.Font(size=10, slant='italic')
        self.day = tk.Entry(master=birthday_frame,
                         fg='gray', font=empty_entry_font)
        self.month = tk.Entry(master=birthday_frame,
                           fg='gray', font=empty_entry_font)
        self.year = tk.Entry(master=birthday_frame,
                          fg='gray', font=empty_entry_font)

        self.day.insert(0, "Day")
        self.month.insert(0, "Month")
        self.year.insert(0, "Year")

        self.day.bind("<FocusIn>", lambda event=None,
                      entry=self.day: self.on_date_click(entry=entry))
        self.month.bind("<FocusIn>", lambda event=None,
                        entry=self.month: self.on_date_click(entry=entry))
        self.year.bind("<FocusIn>", lambda event=None,
                       entry=self.year: self.on_date_click(entry=entry))

        self.day.pack(side=tk.LEFT, padx=5)
        self.month.pack(side=tk.LEFT, padx=5)
        self.year.pack(side=tk.LEFT, padx=5)

    def initialize_age(self) -> None:
        askage = ttk.Label(self.dialog, text="Age:")
        askage.pack()

        self.age = tk.Entry(self.dialog)
        self.age.pack()

    def initialize_height(self) -> None:
        askheight = ttk.Label(self.dialog, text="Height:")
        askheight.pack()

        self.height = tk.Entry(master=self.dialog)
        self.height.pack()

    def initialize_weight(self) -> None:
        askweight = ttk.Label(self.dialog, text="Weight:")
        askweight.pack()

        self.weight = tk.Entry(master=self.dialog)
        self.weight.pack()

    def initialize_appearance(self) -> None:
        askappearance = ttk.Label(self.dialog, text="Appearance:")
        askappearance.pack()

        self.appearance = tk.Text(self.dialog, wrap=tk.WORD, height=5, width=30)
        self.appearance.pack()

    def initialize_personality(self) -> None:
        askpersonality = ttk.Label(self.dialog, text="Personality:")
        askpersonality.pack()

        self.personality = tk.Text(self.dialog, wrap=tk.WORD, height=5, width=30)
        self.personality.pack()

    def initialize_history(self) -> None:
        askhistory = ttk.Label(self.dialog, text="History:")
        askhistory.pack()

        self.history = tk.Text(self.dialog, wrap=tk.WORD, height=5, width=30)
        self.history.pack()

    def initialize_picture(self) -> None:
        askpicture = ttk.Label(
            self.dialog, text="Select picture (not available yet!):")
        askpicture.pack()
        # Here goes code for selecting picture from PC

    def initialize_trivia(self) -> None:
        asktrivia = ttk.Label(self.dialog, text="Trivia:")
        asktrivia.pack()

        self.trivia = tk.Text(self.dialog, wrap=tk.WORD, height=5, width=30)
        self.trivia.pack()

    def on_date_click(self, entry: tk.Entry, event=None) -> None:
        if entry.get() == "Day" or entry.get() == "Month" or entry.get() == "Year":
            entry.delete(0, tk.END)
            entry.config(fg='black', font=('Arial', 10, 'normal'))

    def on_sex_change(self, event) -> None:
        self.gender = self.genderbox.get()

    def close(self) -> None:
        self.dialog.destroy()


class StoryView:
    def __init__(self, root, story: Story, handle_main, stories: list[Story]) -> None:
        self._root = root
        self._handle_main = handle_main
        # Handle character page (yet to be added)
        self._handle_character = None
        self._frame = None
        self._characters_frame = None
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

    def _initialize_characters(self) -> None:
        self._characters_frame = ttk.Frame(master=self._frame)
        self._characters_frame.pack()
        characters = char_service.get_characters_by_story_id(story_id=self.story.get_id())
        if not characters:
            return
        for character in characters:
            self._initialize_character(character=character)

    def _on_character_click(self):
        pass

    def _initialize_character(self, character: Character) -> None:
        char_frame = ttk.Frame(master=self._characters_frame)
        char_frame.pack(padx=5, pady=5)

        img_frame = ttk.Frame(master=char_frame, border=1, relief=tk.SOLID)
        img_frame.pack(padx=5, pady=5)

        img_path = character.get_image_path()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        pic_path = os.path.join(current_dir, img_path)

        img = tk.PhotoImage(file=pic_path)
        label = tk.Label(master=img_frame, image=img)
        label.image = img
        label.pack()
        label.bind("<Button-1>", lambda event: self._on_character_click())

        char_name = character.get_name()
        char_name_label = tk.Label(master=char_frame, text=char_name)
        char_name_label.pack()

    def _initialize_endpage(self) -> None:
        endpage_frame = ttk.Frame(master=self._frame)
        endpage_frame.pack(pady=10)

        button = ttk.Button(
            master=endpage_frame,
            text="Go back",
            command=lambda: self._handle_main()
        )
        button.pack()

    def _initialize(self) -> None:
        self._frame = ttk.Frame(master=self._root)

        self._initialize_heading()
        self._initialize_characters()
        self._initialize_endpage()

    def _character_creation_dialog(self) -> None:
        if not self._frozen():
            self.freeze()
            self._input_character_details()

    def _input_character_details(self) -> None:
        dialog = CharacterCreationDialog(self._root, self)
        self._wait_for_input(dialog, self._create_character)

    # Waits for user input before executing the rest of create story function
    def _wait_for_input(self, dialog: "CharacterCreationDialog", callback) -> None:
        def wait():
            if dialog.dialog.winfo_exists():
                self._root.after(100, wait)
            else:
                callback()
        wait()

    def _create_character(self) -> None:
        new_character = self._temp
        self._temp = None
        valid_character = char_service.create_character(
            stats=new_character, story_id=self.story.get_id())
        if valid_character:
            self._initialize_character(character=valid_character)
        self.unfreeze()

    def freeze(self):
        self._freeze = True

    def unfreeze(self):
        self._freeze = False

    def _frozen(self) -> bool:
        return self._freeze
