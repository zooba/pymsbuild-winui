def color_repr(c):
    return "0x{:02X}{:02X}{:02X}{:02X}".format(
        c.A, c.B, c.G, c.R
    )

class MainWindow:
    def __init__(self, view):
        self.view = view

    def Color_ColorChanged(self, sender, e):
        self.view.MyProperty = f"Selected {color_repr(e.NewColor)}"

    def Calendar_DateChanged(self, sender, e):
        self.view.MyProperty = f"Selected {e.NewDate} (deselect {e.OldDate})"
