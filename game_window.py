from size import SizeWindow


class GameWindowInterface:
    width = None
    height = None

    def __init__(self, resolutions=None):
        resolutions = resolutions if resolutions is not None else \
            ["600 x 300",
             "900 x 450",
             "1200 x 600",
             "1800 x 750"]
        size_window = SizeWindow(resolutions)
        size_window.display()
        self.width = size_window.width
        self.height = size_window.height
