import os
from pymsbuild import *
from pymsbuild_winui.pymsbuild import *

METADATA = {"Metadata-Version": "2.1", "Name": "TestApp", "Version": "1.0"}

PACKAGE = Package(
    'TestApp',
    PyFile("app.py"),
    WinUIExe(
        "app",
        XamlApp("app.xaml"),
        XamlPage("MainWindow.xaml"),
    ),
)