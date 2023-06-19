import sys

import trio
from kivy.app import App
from kivy.resources import resource_add_path

import screens
import widgets
from translation import TranslatedApp

if getattr(sys, 'frozen', False):
    resource_add_path(sys._MEIPASS)


class Slap(
    TranslatedApp,
    App,
):
    async def async_run(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery
            await super().async_run('trio')
            nursery.cancel_scope.cancel()


if __name__ == '__main__':
    app = Slap()
    trio.run(app.async_run)
