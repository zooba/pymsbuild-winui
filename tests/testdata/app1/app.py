class MainWindow:
    def __init__(self, view):
        self.view = view

    def myButton_Click(self):
        #self.view.myButton.content = self.view.box(f"Clicked in Python ({self.MyProperty})!")
        self.view.MyProperty += 1
