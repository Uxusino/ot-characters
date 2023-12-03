import tkinter as tk
import os
from tkinter import constants, ttk
from services.character_service import char_service, Character
from services.story_service import story_service, Story


class CharacterView:
    def __init__(self, root, character: Character, handle_story) -> None:
        self._root = root
        self._handle_story = handle_story
        self._frame = None

        self._character = character

        self._heading_font = ('Helvetica', '20')
        self._info_width = 50
        self._button_width = 15

        self._initialiaze()

    def pack(self):
        self._frame.pack()

    def destroy(self):
        self._frame.destroy()

    def _initialiaze(self):
        self._frame = ttk.Frame(master=self._root)
        self._initialize_left()
        self._initialize_right()

    def _initialize_left(self):
        left_frame = ttk.Frame(master=self._frame)
        left_frame.pack(side=tk.LEFT)

        labels = ["Appearance", "Personality",
                  "History", "Relations", "Trivia"]
        for l in labels:
            stat_frame = ttk.Frame(left_frame)
            stat_frame.pack(pady=15, padx=30)
            ttk.Label(stat_frame, text=l,
                      font=self._heading_font).pack(anchor="w")
            if l == "Relations":
                new_relation = ttk.Button(
                    master=stat_frame, text="Add Relation", command=self._add_relation, width=self._button_width)
                new_relation.pack(pady=5)
            info_frame = ttk.Frame(
                master=stat_frame, border=1, relief=tk.SOLID)
            info_frame.pack()
            if l != "Relations":
                info = ttk.Label(
                    master=info_frame,
                    text=self._character.stats[l.lower()],
                    width=self._info_width)
                info.pack(padx=5, pady=5)

    def _initialize_right(self):
        right_frame = ttk.Frame(master=self._frame)
        right_frame.pack(side=tk.RIGHT)

        name = self._character.name()
        name_label = ttk.Label(
            master=right_frame, text=name, font=self._heading_font)
        name_label.pack(pady=10)

        img_frame = ttk.Frame(master=right_frame, border=1,
                              relief=tk.SOLID, width=125, height=125)
        img_frame.pack()

        img_path = self._character.image()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pic_path = os.path.join(current_dir, img_path)
        img = tk.PhotoImage(file=pic_path)
        img_label = tk.Label(master=img_frame, image=img)
        img_label.image = img
        img_label.pack()

        story_name = story_service.get_name_by_id(
            story_id=self._character.get_story_id())
        story_name_label = ttk.Label(master=right_frame, text=story_name)
        story_name_label.pack()

        table_frame = ttk.Frame(right_frame)
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

        delete_character = ttk.Button(master=right_frame, text="Delete Character",
                                      command=self._delete_character, width=self._button_width)
        delete_character.pack(pady=50)

        go_back = ttk.Button(master=right_frame, text="Go Back", width=self._button_width, command=lambda: self._handle_story(
            story=story_service.get_story_by_id(self._character.get_story_id())))
        go_back.pack()

    def _add_relation(self):
        pass

    def _delete_character(self):
        pass
