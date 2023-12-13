import tkinter as tk
from tkinter import ttk
from typing import Callable
from services.character_service import char_service, Character
from services.story_service import story_service
from services.formatter import formatter


class RelationDialog:
    def __init__(self, parent, character: Character) -> None:
        """Class for dialog window for setting characters' relationships.

        Args:
            parent (Tk): Parent root.
            character (Character): Character whose relationship is being added.
        """

        self.dialog = tk.Toplevel(parent)
        self.dialog.title = "Add Relation"

        self._character = character
        self._characters = None
        self._relations = None
        self._target_char = None
        self._charbox = None
        self._target_rel = None
        self._relbox = None

        self._former = tk.IntVar()

        self._initialize()

    def _initialize(self):
        """Initializes elements in the dialog window.
        """

        self._characters = char_service.get_characters_by_story_id(
            self._character.story_id)
        self._relations = char_service.get_relations()

        self._charbox = ttk.Combobox(
            master=self.dialog, values=[char.name() for char in self._characters], state="readonly"
        )
        self._charbox.bind("<<ComboboxSelected>>", self._on_character_choice)
        self._charbox.pack(padx=5, side=tk.LEFT)

        ttk.Label(master=self.dialog, text="is").pack(side=tk.LEFT)

        self._relbox = ttk.Combobox(
            master=self.dialog, values=self._relations, state="readonly"
        )
        self._relbox.bind("<<ComboboxSelected>>", self._on_relation_choice)
        self._relbox.pack(padx=5, side=tk.LEFT)

        ttk.Label(master=self.dialog, text="to me.").pack(side=tk.LEFT)

        former_check = tk.Checkbutton(
            master=self.dialog, text="Former", variable=self._former)
        self._former.set(0)
        former_check.pack(padx=5, side=tk.LEFT)

        ttk.Button(master=self.dialog, text="OK",
                   command=self._enter).pack(pady=10)

    def _on_character_choice(self, event):
        """Is called when user selects a character from character selection box.
        """

        self._target_char = self._characters[self._charbox.current()]

    def _on_relation_choice(self, event):
        """Is called when user selects a relation from relation selection box.
        """

        self._target_rel = self._relbox.get()

    def _enter(self):
        """Is called when user presses OK button.

        Doesn't close window if a character or relation are not selected.

        """

        if not self._target_char or not self._target_rel:
            return
        char_service.set_relations(char1=self._character, char2=self._target_char,
                                   relation=self._target_rel, former=self._former.get())
        self._close()

    def _close(self):
        """Closes the dialog.
        """
        self.dialog.destroy()


class CharacterView:
    def __init__(self, root, character: Character, handle_story: Callable) -> None:
        """View that contains information about certain character.

        Args:
            root (Tk): Parent root.
            character (Character): Character whose information is being displayed.
            handle_story (Callable): Function to return back to story view.
        """

        self._root = root
        self._handle_story = handle_story
        self._frame = None
        self._relations_frame = None

        self._frozen = False

        self._character = character

        self._heading_font = ('Helvetica', '20')
        self._info_width = 50
        self._button_width = 15

        self._initialiaze()

    def pack(self):
        """Packs the main frame of the view.
        """

        self._frame.pack()

    def destroy(self):
        """Destroys the main frame of the view.
        """

        self._frame.destroy()

    def _initialiaze(self):
        """Initializes the whole view.
        """

        self._frame = ttk.Frame(master=self._root)
        self._initialize_left()
        self._initialize_right()

    def _initialize_left(self):
        """Initializes left side of the view.
        """

        left_frame = ttk.Frame(master=self._frame)
        left_frame.pack(side=tk.LEFT)

        labels = ["Appearance", "Personality",
                  "History", "Trivia"]
        for l in labels:
            stat_frame = ttk.Frame(left_frame)
            stat_frame.pack(pady=15, padx=30)
            ttk.Label(stat_frame, text=l,
                      font=self._heading_font).pack(anchor="w")
            info_frame = ttk.Frame(
                master=stat_frame, border=1, relief=tk.SOLID)
            info_frame.pack()
            info = ttk.Label(
                master=info_frame,
                text=formatter.split_text(
                    self._character.stats[l.lower()], 50),
                width=self._info_width)
            info.pack(padx=5, pady=5)

        rel_frame = ttk.Frame(left_frame)
        rel_frame.pack(pady=15, padx=30)
        ttk.Label(rel_frame, text="Relationships",
                  font=self._heading_font).pack(anchor="w")

        info_frame = ttk.Frame(
            master=rel_frame, border=1, relief=tk.SOLID)
        info_frame.pack()
        ttk.Button(master=info_frame, text="Add Relation",
                   command=self._add_relation, width=self._button_width).pack(pady=5)
        self._relations_frame = ttk.Frame(
            master=info_frame, width=self._info_width)
        self._relations_frame.pack()
        self._initialize_relations()

    def _initialize_right(self):
        """Initializes the right side of the character view.
        """

        right_frame = ttk.Frame(master=self._frame)
        right_frame.pack(side=tk.RIGHT)

        name = self._character.name()
        name_label = ttk.Label(
            master=right_frame, text=name, font=self._heading_font)
        name_label.pack(pady=10)

        img_frame = ttk.Frame(master=right_frame, border=1,
                              relief=tk.SOLID, width=125, height=125)
        img_frame.pack()

        img_path = char_service.get_image_path(self._character)

        img = tk.PhotoImage(file=img_path)
        img_label = tk.Label(master=img_frame, image=img)
        img_label.image = img
        img_label.pack()

        story_name = story_service.get_name_by_id(
            story_id=self._character.story_id)
        story_name_label = ttk.Label(master=right_frame, text=story_name)
        story_name_label.pack()

        self._initialize_table(parent=right_frame)

    def _initialize_table(self, parent: ttk.Frame):
        """Initializes table with character info.

        Args:
            parent (ttk.Frame): Parent frame.
        """

        table_frame = ttk.Frame(parent)
        table_frame.pack()

        data = [
            ("Gender", self._character.gender()),
            ("Birthday", self._character.birthday()),
            ("Age", self._character.age()),
            ("Height", self._character.height()),
            ("Weight", self._character.weight())
        ]

        y = 0
        for record in data:
            ttk.Label(master=table_frame, text=record[0]).grid(row=y, column=0)
            entry = ttk.Entry(master=table_frame)
            entry.grid(row=y, column=1)
            entry.insert(0, record[1])
            y += 1

        delete_character = ttk.Button(master=parent, text="Delete Character",
                                      command=self._delete_character, width=self._button_width)
        delete_character.pack(pady=50)

        go_back = ttk.Button(master=parent, text="Go Back", width=self._button_width, command=lambda: self._handle_story(
            story=story_service.get_story_by_id(self._character.story_id)))
        go_back.pack()

    def _add_relation(self):
        """Calls new dialog window for adding relationships, freezes other buttons and waits for input.
        """

        if not self._frozen:
            dialog = RelationDialog(self._root, self._character)
            self._frozen = True
            self._wait_for_input(dialog, self._initialize_relations)

    def _wait_for_input(self, dialog: "RelationDialog", callback) -> None:
        """Doesn't execute the rest of the code in a function when called if an open dialog exists.

        Args:
            dialog (RelationDialog): Function checks if this dialog exists.
            callback (function): Calls this function when the dialog cease from existence.
        """

        def wait():
            if dialog.dialog.winfo_exists():
                self._root.after(100, wait)
            else:
                callback()
        wait()

    def _initialize_relations(self) -> None:
        """Destroys and initializes all relations from scratch.
        """

        for widget in self._relations_frame.winfo_children():
            widget.destroy()
        relations = char_service.get_character_relations(self._character)
        if not relations:
            ttk.Label(master=self._relations_frame, text="",
                      width=self._info_width).pack()
            return
        for relation in relations:
            ttk.Label(
                master=self._relations_frame,
                text=formatter.relation_str(relation),
                width=self._info_width
            ).pack()
        self._frozen = False

    def _delete_character(self):
        """Deletes current character from the database.

        WIP

        """

        pass
