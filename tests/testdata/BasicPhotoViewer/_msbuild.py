import os
from pymsbuild import *
from pymsbuild_winui.pymsbuild import *

METADATA = {"Metadata-Version": "2.1", "Name": "BasicPhotoViewer", "Version": "1.0"}

PACKAGE = Package(
    'out',
    PyFile("PhotoViewer.py"),
    PyFile("image_info.py"),
    Package("Photos",
        File("Photos\\*.jpg"),
    ),
    WinUIExe(
        "PhotoViewer",  # must match app namespace
        XamlApp("app.xaml"),
        XamlPage("MainWindow.xaml"),
    ),
)

def init_PACKAGE(tag):
    # WinUIExe needs to be passed the wheel tag
    PACKAGE.find("PhotoViewer").init_PACKAGE(tag)