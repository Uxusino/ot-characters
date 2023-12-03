from services.story_service import story_service, Story
from services.character_service import Character
from . import story_view as sv
from . import main_view as mv
from . import character_view as cv
import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir)
sys.path.append(root_dir)


class UI:
    def __init__(self, root) -> None:
        self._root = root
        self._current_view = None
        self.stories = story_service.get_stories()

    def start(self):
        self.show_main_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _handle_main(self):
        self.stories = story_service.get_stories()
        self.show_main_view()

    def _handle_story(self, story: Story):
        self.stories = story_service.get_stories()
        self.show_story_view(story=story)

    def _handle_character(self, character: Character) -> None:
        self.show_character_view(character=character)

    def show_main_view(self):
        self._hide_current_view()

        self._current_view = mv.MainView(
            root=self._root,
            stories=self.stories,
            handle_story=self._handle_story
        )
        self._current_view.pack()

    def show_story_view(self, story: Story):
        self._hide_current_view()

        self._current_view = sv.StoryView(
            root=self._root,
            story=story,
            handle_main=self._handle_main,
            handle_character=self._handle_character,
            stories=self.stories
        )
        self._current_view.pack()

    def show_character_view(self, character: Character) -> None:
        self._hide_current_view()

        self._current_view = cv.CharacterView(
            root=self._root,
            character=character,
            handle_story=self._handle_story
        )
        self._current_view.pack()
