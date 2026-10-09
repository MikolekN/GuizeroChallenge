DARK_THEME = (
    ("background", "#2d2d2d"),
    ("foreground", "white"),
    ("activebackground", "#2d2d2d"),
    ("activeforeground", "white"),
)


def dark_theme_element(elem):
    # Not every widget accepts every one of these, and the ones that do not are simply
    # left as they are. A frame having no activebackground is normal, not worth reporting
    for option, value in DARK_THEME:
        try:
            elem.tk.config(**{option: value})
        except Exception:
            pass


def apply(elems):
    for elem in elems:
        dark_theme_element(elem)
