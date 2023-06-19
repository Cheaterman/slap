import gettext
import glob
import os

from babel.messages import mofile, pofile
from kivy.event import EventDispatcher
from kivy.lang import global_idmap
from kivy.logger import Logger
from kivy.properties import ConfigParserProperty, StringProperty


class Translator(EventDispatcher):
    language = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.observers = []
        self.gettext = lambda message: message

    def _(self, message):
        return self.gettext(message)

    translate = _

    def fbind(self, name, func, *args, **kwargs):
        if name == '_':
            self.observers.append((func, args, kwargs))
        else:
            super().fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, *args, **kwargs):
        if name == '_':
            args = (func, args, kwargs)
            if args in self.observers:
                self.observers.remove(args)
        else:
            return super().funbind(name, func, *args, **kwargs)

    def on_language(self, _, language):
        language = language.split('-')[0]
        self.gettext = gettext.translation(
            'messages',
            'translations',
            languages=[language],
            fallback=True if language == 'en' else False,
        ).gettext

        for func, args, _ in self.observers:
            try:
                func(*args, None, None)
            except ReferenceError:
                continue

    def compile_languages(self, remove_po_files=False):
        for filename in glob.glob('translations/*/LC_MESSAGES/messages.po'):
            language = filename[
                len('translations/'):-len('/LC_MESSAGES/messages.po')
            ]

            Logger.info('Translator: Compiling language %s...', language)

            with open(filename, 'rb') as po_file:
                catalog = pofile.read_po(po_file, locale=language)

            mo_filename = filename.replace('.po', '.mo')

            with open(mo_filename, 'wb') as mo_file:
                mofile.write_mo(mo_file, catalog)

            if remove_po_files:
                os.remove(filename)


class TranslatedApp:
    language = ConfigParserProperty('', 'app', 'language', 'app')

    def build_config(self, config):
        config.setdefaults('app', {
            'language': 'en',
        })
        super().build_config(config)

    def load_kv(self, filename):
        self.translator = translator = Translator()
        translator.compile_languages()
        translator.language = self.language
        self.bind(language=translator.setter('language'))
        global_idmap['_'] = translator
        return super().load_kv(filename)
