from guizero import App, ButtonGroup, PushButton
import dark_theme
from center_window import center_window


# Pop-up to define the window size
class SizeWindow(App):

    def __init__(self, resolutions):
        super().__init__()

        # The size the player picked. Deliberately not called width and height, because
        # those are properties of the window itself on guizero's App and setting them
        # would resize this dialog rather than record an answer
        self.chosen_width = None
        self.chosen_height = None

        # Kept per dialog rather than on the class, so that opening a second one starts
        # from an empty list instead of inheriting the widgets of the first
        self.interface_elements = []

        self.title = "Resolution"
        self.interface_elements.append(self)

        self.resolutionRadioButtons = ButtonGroup(self, options=resolutions, selected=resolutions[1])
        self.interface_elements.append(self.resolutionRadioButtons)
        self.interface_elements += self.resolutionRadioButtons.children

        self.selectButton = PushButton(self, text="Select", command=self.changeSize, align="bottom")
        self.interface_elements.append(self.selectButton)

        dark_theme.apply(self.interface_elements)

        # Sized by its contents, so the natural size has to be worked out before the
        # dialog can be placed in the middle of the screen
        self.tk.update_idletasks()
        center_window(self, self.tk.winfo_reqwidth(), self.tk.winfo_reqheight())

    def changeSize(self):
        self.chosen_width = int(self.resolutionRadioButtons.value.split(" x ")[0])
        self.chosen_height = int(self.resolutionRadioButtons.value.split(" x ")[1])
        self.destroy()
