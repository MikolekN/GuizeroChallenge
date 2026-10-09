from size import SizeWindow


class ResolutionNotChosen(Exception):
    """Raised when the player closes the resolution dialog instead of picking a size."""


class GameWindowInterface:

    def __init__(self, resolutions=None):
        resolutions = resolutions if resolutions is not None else \
            ["600 x 300",
             "900 x 450",
             "1200 x 600",
             "1800 x 750"]
        size_window = SizeWindow(resolutions)
        size_window.display()

        # The dialog was closed rather than answered, so there is no game to set up. This
        # is checked here so that no game has to remember to check it for itself
        if size_window.chosen_width is None or size_window.chosen_height is None:
            raise ResolutionNotChosen()

        self.width = size_window.chosen_width
        self.height = size_window.chosen_height
