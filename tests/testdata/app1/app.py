def color_repr(c):
    return "0x{:02X}{:02X}{:02X}{:02X}".format(
        c.A, c.B, c.G, c.R
    )

class MainWindow:
    def __init__(self, view, viewmodels):
        self.view = view
        self.viewmodels = viewmodels
        self.view.Obj = self.dc = self.viewmodels.DayColor()

    def Color_ColorChanged(self, sender, e):
        self.view.MyProperty = f"Selected {color_repr(e.NewColor)}"
        c = e.NewColor
        self.dc.Color = c.A << 24 | c.B << 16 | c.G << 8 | c.R

    def Calendar_DateChanged(self, sender, e):
        self.view.MyProperty = f"Selected {e.NewDate} (deselect {e.OldDate})"
        if e.NewDate:
            self.dc.Day = e.NewDate
