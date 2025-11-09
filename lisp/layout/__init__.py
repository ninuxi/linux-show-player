__LAYOUTS__ = {}


def get_layouts():
    return list(__LAYOUTS__.values())


def get_layout(class_name):
    return __LAYOUTS__[class_name]


def register_layout(layout):
    __LAYOUTS__[layout.__name__] = layout


def unregister_layout(layout):
    """Unregister a layout"""
    if layout.__name__ in __LAYOUTS__:
        del __LAYOUTS__[layout.__name__]


def layout_names():
    """Get list of layout names"""
    return list(__LAYOUTS__.keys())
