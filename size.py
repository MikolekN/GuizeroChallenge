import guizero

from guizero import App, ButtonGroup, PushButton
import dark_theme


# Pop-up to define the window size
class SizeWindow(App):
    width = None
    height = None

    interface_elements = []
    resolutionRadioButtons = None
    selectButton = None

    def __init__(self, resolutions):
        super().__init__()

        self.title = "Resolution"
        self.interface_elements.append(self)

        self.resolutionRadioButtons = ButtonGroup(self, options=resolutions, selected=resolutions[1])
        self.interface_elements.append(self.resolutionRadioButtons)
        self.interface_elements += self.resolutionRadioButtons.children

        self.selectButton = PushButton(self, text="Select", command=self.changeSize, align="bottom")
        self.interface_elements.append(self.selectButton)

        # dark_theme.apply(interface_elements)

    def changeSize(self):
        self.width = int(self.resolutionRadioButtons.value.split(" x ")[0])
        self.height = int(self.resolutionRadioButtons.value.split(" x ")[1])
        self.destroy()
