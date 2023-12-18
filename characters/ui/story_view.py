import tkinter as tk
import os
import string
import random
from . import delete_dialog as dd
from tkinter import ttk, font, constants, filedialog
from PIL import Image, ImageTk
from entities.story import Story
from services.character_service import char_service, Character
from services.story_service import story_service


class CharacterCreationDialog:
    def __init__(self, parent, view: "StoryView") -> None:
        self.view = view

        self.dialog = tk.Toplevel(parent)
        self.dialog.title = "New Character"

        self._pic_frame = tk.Frame(self.dialog)
        self._pic_name = ttk.Label(master=self._pic_frame, text="")

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

        self._initialize()

        ok_button = ttk.Button(self.dialog, text="Ok", command=self.enter)
        ok_button.pack()

    def _initialize(self):
        """Initializes all elements of character creation.
        """

        tk.Label(
            master=self.dialog,
            text="""
                All numeric values such as dates, age, height and weight must be integers and only contain numbers.
            """,
            justify=tk.LEFT,
            anchor='w').pack()

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

    def enter(self) -> None:
        """Gets all the data from entry or text boxes.

        Saves tuple (name, gender, (day, month, year), height, weight, appearance, personality, history, picture, trivia) to temporary data.

        """

        name = self.name.get()
        if name != "" and len(name) > 30:
            return
        gender = self.gender
        day = self.day.get()
        if day not in ["", "Day"] and len(day) > 2:
            return
        month = self.month.get()
        if month not in ["", "Month"] and len(month) > 2:
            return
        year = self.year.get()
        age = self.age.get()
        height = self.height.get()
        weight = self.weight.get()
        appearance = self.appearance.get("1.0", tk.END).strip()
        personality = self.personality.get("1.0", tk.END).strip()
        history = self.history.get("1.0", tk.END).strip()
        picture = self.picture
        if picture:
            picture = self.save_image(picture)
        trivia = self.trivia.get("1.0", tk.END).strip()

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

    def generate_name(self) -> str:
        """Generates random name for new image.

        Returns:
            str: Randomized string.
        """
        chars = string.ascii_letters + string.digits
        name = ''.join(random.sample(chars, k=10))
        return name

    def save_image(self, image: Image) -> str:
        """Saves image to image folder and returns image's name.

        Args:
            image (Image): Image object to be saved.

        Returns:
            str: Image's new name.
        """

        dir = "../library/avatars/"
        new_name = self.generate_name()
        print(new_name)
        filedir = dir + f"{new_name}.png"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        pic_path = os.path.join(current_dir, filedir)

        image.save(pic_path, format="png")
        return new_name

    def initialize_name(self) -> None:
        askname = ttk.Label(self.dialog, text="Name:")
        askname.pack()

        self.name = tk.Entry(self.dialog)
        self.name.pack()

    def initialize_gender(self) -> None:
        """Initializes gender selection combobox.
        """

        askgender = ttk.Label(self.dialog, text="Gender:")
        askgender.pack()

        self.genderbox = ttk.Combobox(
            self.dialog, values=["Female", "Male", "Unknown"], state="readonly")
        self.genderbox.bind("<<ComboboxSelected>>", self.on_sex_change)
        self.genderbox.pack()

    def initialize_birthday(self) -> None:
        """Initializes entries for day, month and year of birthday.
        """
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
        askheight = ttk.Label(self.dialog, text="Height (cm):")
        askheight.pack()

        self.height = tk.Entry(master=self.dialog)
        self.height.pack()

    def initialize_weight(self) -> None:
        askweight = ttk.Label(self.dialog, text="Weight (kg):")
        askweight.pack()

        self.weight = tk.Entry(master=self.dialog)
        self.weight.pack()

    def initialize_appearance(self) -> None:
        askappearance = ttk.Label(self.dialog, text="Appearance:")
        askappearance.pack()

        self.appearance = tk.Text(
            self.dialog, wrap=tk.WORD, height=5, width=30)
        self.appearance.pack()

    def initialize_personality(self) -> None:
        askpersonality = ttk.Label(self.dialog, text="Personality:")
        askpersonality.pack()

        self.personality = tk.Text(
            self.dialog, wrap=tk.WORD, height=5, width=30)
        self.personality.pack()

    def initialize_history(self) -> None:
        askhistory = ttk.Label(self.dialog, text="History:")
        askhistory.pack()

        self.history = tk.Text(self.dialog, wrap=tk.WORD, height=5, width=30)
        self.history.pack()

    def initialize_picture(self) -> None:
        self._pic_frame.pack()
        askpicture = ttk.Label(
            self._pic_frame, text="Image:")
        warning = ttk.Label(
            self._pic_frame, text="For better compatibility the image is advised to have 1:1 aspect ratio.\nCurrently supported: .png, .jpg, .jpeg"
        )

        askpicture.pack()
        warning.pack()
        self._pic_name.pack()

        select_image_button = ttk.Button(
            self._pic_frame, text="Select image", command=self.select_image)
        select_image_button.pack()

    def select_image(self) -> None:
        """Lets user select an image from their computer.
        """

        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;")]
        )

        if file_path:
            image_path = file_path
            img_name = os.path.basename(file_path)
            img = Image.open(image_path)
            img = img.resize((125, 125))
            self.picture = img
            self._pic_name.config(text=img_name)

    def initialize_trivia(self) -> None:
        asktrivia = ttk.Label(self.dialog, text="Trivia:")
        asktrivia.pack()

        self.trivia = tk.Text(self.dialog, wrap=tk.WORD, height=5, width=30)
        self.trivia.pack()

    def on_date_click(self, entry: tk.Entry, event=None) -> None:
        """Deletes gray preview text from birthday entries.

        Args:
            entry (tk.Entry): Date entry to erase preview text.
        """

        if entry.get() == "Day" or entry.get() == "Month" or entry.get() == "Year":
            entry.delete(0, tk.END)
            entry.config(fg='black', font=('Arial', 10, 'normal'))

    def on_sex_change(self, event) -> None:
        self.gender = self.genderbox.get()

    def close(self) -> None:
        self.dialog.destroy()


class StoryView:
    def __init__(self, root: tk.Tk, story: Story, handle_main, handle_character, stories: list[Story]) -> None:
        self._root = root
        self._handle_main = handle_main
        self._handle_character = handle_character
        self._frame = None
        self._characters_frame = None
        self.story = story
        self.stories = stories

        self._head = None
        self._desc = None

        self._bg_color = "#f0f0f0"
        self._row = 0
        self._column = 0

        self._frozen = False
        self._temp = None

        self._initialize()

    def pack(self):
        self._frame.pack(expand=True, fill="x")

    def destroy(self):
        self._frame.destroy()

    def _change_story_name(self, event) -> None:
        """Updates story name after user presses Enter, if name not empty and not too long.
        """

        new_name = self._head.get()
        if new_name == "" or len(new_name) > 100:
            return
        story_service.update_story_name(
            story_id=self.story.story_id, new_name=new_name)

    def _change_story_desc(self, event) -> None:
        """Updates story description after user presses Enter if new description is not too long.
        """

        new_desc = self._desc.get()
        if len(new_desc) > 100:
            return
        story_service.update_story_desc(
            story_id=self.story.story_id, new_desc=new_desc)

    def _initialize_heading(self):
        """Initializes heading of the view: story name, description and New Character button.
        """

        heading_frame = ttk.Frame(
            master=self._frame, borderwidth=1, relief='solid', padding=5)
        heading_frame.pack(expand=True, fill="x")

        story_name = self.story.name
        self._head = tk.Entry(
            master=heading_frame,
            font=('Helvetica', '24'),
            bg=self._bg_color,
            relief="flat",
            borderwidth=0,
            justify=tk.CENTER
        )
        self._head.insert(tk.END, story_name)
        self._head.pack(side=tk.TOP, anchor='center', fill='x')
        self._head.bind("<Return>", self._change_story_name)

        story_desc = self.story.desc
        self._desc = tk.Entry(
            master=heading_frame,
            font=('Helvetica', '14'),
            bg=self._bg_color,
            relief="flat",
            borderwidth=0,
            justify=tk.CENTER
        )
        if story_desc:
            self._desc.insert(tk.END, story_desc)
        else:
            self._desc.insert(tk.END, "No description")
        self._desc.pack(side=tk.TOP, pady=5, anchor='center', fill='x')
        self._desc.bind("<Return>", self._change_story_desc)

        character_button = ttk.Button(
            master=heading_frame,
            text="New Character",
            command=self._character_creation_dialog
        )
        character_button.pack(pady=5)

    def _initialize_characters(self) -> None:
        """Initializes characters frame for all characters of the story.
        """

        self._characters_frame = ttk.Frame(master=self._frame)
        self._characters_frame.pack(fill=tk.BOTH, expand=True)
        characters = char_service.get_characters_by_story_id(
            story_id=self.story.story_id)
        if not characters:
            return
        for character in characters:
            self._initialize_character(character=character)

    def _initialize_character(self, character: Character) -> None:
        """Initializes single character frame for selecter Character object.

        Args:
            character (Character): Character to be viewed.
        """

        char_frame = ttk.Frame(master=self._characters_frame)
        char_frame.grid(row=self._row, column=self._column)

        self._column += 1
        if self._column == 7:
            self._column = 0
            self._row += 1

        img_frame = ttk.Frame(master=char_frame, border=1,
                              relief=tk.SOLID, width=125, height=125)
        img_frame.pack(padx=5, pady=5)

        img_path = char_service.get_image_path(character=character)

        img = tk.PhotoImage(file=img_path)
        label = tk.Label(master=img_frame, image=img)
        label.image = img
        label.pack()
        label.bind(
            "<Button-1>", lambda event: self._handle_character(character=character))

        char_name = character.name()
        char_name_label = tk.Label(master=char_frame, text=char_name)
        char_name_label.pack()

    def _initialize_endpage(self) -> None:
        """Initializes endpage which contain story statistics and a button for going back to the story list.
        """

        endpage_frame = ttk.Frame(master=self._frame)
        endpage_frame.pack(pady=10)

        tk.Label(master=endpage_frame, text="Story Statistics").pack()

        mean_age = story_service.get_mean_age(story_id=self.story.story_id)
        mean_age_lbl = tk.Label(
            master=endpage_frame,
            text=f"Mean age: {mean_age}"
        )
        mean_age_lbl.pack()

        delete_story_button = ttk.Button(
            master=endpage_frame,
            text="Delete story",
            command=self._press_delete_button
        )
        delete_story_button.pack(pady=5)

        button = ttk.Button(
            master=endpage_frame,
            text="Go back",
            command=lambda: self._handle_main()
        )
        button.pack(pady=5)

    def _press_delete_button(self) -> None:
        if self._frozen:
            return
        self._frozen = True
        dialog = dd.DeleteDialog(
            self._root, self._handle_main, self.story, 'story')
        self._wait_for_input(dialog, self.unfreeze)

    def unfreeze(self):
        self._frozen = False

    def _initialize(self) -> None:
        """Initializes the main frame.
        """

        self._frame = ttk.Frame(master=self._root)
        self._root.configure(bg=self._bg_color)
        self._root.geometry('1000x600')

        self._initialize_heading()
        self._initialize_characters()
        self._initialize_endpage()

    def _character_creation_dialog(self) -> None:
        """Calls character creation dialog if none is already opened.
        """

        if not self._frozen:
            self._frozen = True
            self._input_character_details()

    def _input_character_details(self) -> None:
        """Calls character creation dialog and waits for user's input.
        """

        dialog = CharacterCreationDialog(self._root, self)
        self._wait_for_input(dialog, self._create_character)

    def _wait_for_input(self, dialog: "CharacterCreationDialog", callback) -> None:
        """Waits for user input before executing the rest of character creation function.

        Args:
            dialog (CharacterCreationDialog): Dialog that is awaited to be closed.
            callback (function): Function that is called when dialog is closed.
        """

        def wait():
            if dialog.dialog.winfo_exists():
                self._root.after(100, wait)
            else:
                callback()
        wait()

    def _create_character(self) -> None:
        """Clears temporary data, creates new character from input and initializes it; Unfreezes story view.
        """

        new_character = self._temp
        self._temp = None
        valid_character = char_service.create_character(
            new_character, self.story.story_id)
        if valid_character:
            self._initialize_character(character=valid_character)
        self._frozen = False
