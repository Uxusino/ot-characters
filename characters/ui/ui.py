from tkinter import Tk, ttk
from main_view import MainView
from story_view import StoryView
from services.story_service import story_service
from entities.story import Story

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

    def show_main_view(self):
        self._hide_current_view()

        self._current_view = MainView(
            root=self._root,
            stories = self.stories,
            handle_story = self._handle_story
        )
        self._current_view.pack()

    def show_story_view(self, story: Story):
        self._hide_current_view()

        self._current_view = StoryView(
            root=self._root,
            story=story,
            handle_main = self._handle_main,
            stories = self.stories
        )
        self._current_view.pack()

window = Tk()
window.title("OT-chara")

ui = UI(window)
ui.start()

window.mainloop()