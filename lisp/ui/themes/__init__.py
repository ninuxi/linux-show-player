from os import path

from lisp.core.loading import load_classes


class Theme:
    """Base class for themes"""
    
    def apply(self, qt_app):
        """Apply the theme to the Qt application"""
        pass


_THEMES = {}


def load_themes():
    if not _THEMES:
        for name, theme in load_classes(__package__, path.dirname(__file__)):
            _THEMES[name] = theme()


def themes_names():
    load_themes()
    return list(_THEMES.keys())


def get_theme(theme_name):
    load_themes()
    return _THEMES[theme_name]
