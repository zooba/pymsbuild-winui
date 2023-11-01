import pathlib
import sys

ROOT = pathlib.Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT))
TESTDATA = ROOT / "tests" / "testdata" / "generate"

from io import StringIO
from pymsbuild_winui.generate import Parser


def test_basic_parse():
    p = Parser()
    page = p.parse_page(TESTDATA / "MainWindow.xaml")
    assert page.basename == "MainWindow.xaml"
    assert p.namespace == "app"
    assert [vars(p) for p in page.properties] == [
        {"name": "MyProperty", "type": "int32_t", "idltype": "Int32", "default": "nullptr"},
        {"name": "MyProperty2", "type": "winrt::hstring", "idltype": "String", "default": '"Hello"'},
        {"name": "MyProperty3", "type": "winrt::hstring", "idltype": "String", "default": '"Default value"'},
        {"name": "MyProperty4", "type": "winrt::hstring", "idltype": "String", "default": '" With spaces "'},
    ]
    assert [vars(h) for h in page.handlers] == [
        {"name": "myButton_Click", "eventarg": "RoutedEventArgs", "sender": "IInspectable"},
        {"name": "myButton2_Click", "eventarg": "MadeUpEventArgs", "sender": "Button"},
    ]
    assert [vars(c) for c in page.controls] == [
        {"name": "myButton", "idltype": "Button"},
    ]


def test_basic_app_parse():
    p = Parser()
    app = p.parse_app(TESTDATA / "App.xaml")
    assert app is p.app
    assert app.basename == "App.xaml"
    assert app.name == "App"
    assert p.namespace == "app"


def render_one(parser, filename):
    for tmpl, ctxt, name in parser.get_templates():
        if pathlib.Path(name).match(filename):
            return tmpl.render({**parser.get_context(), **ctxt})


def test_basic_generate():
    p = Parser()
    p.parse_page(TESTDATA / "MainWindow.xaml")
    cpp = render_one(p, "MainWindow.xaml.cpp")
    h = render_one(p, "MainWindow.xaml.h")
    print(cpp)
    print(h)
    #assert 0


def test_basic_app_generate():
    p = Parser()
    p.parse_app(TESTDATA / "App.xaml")
    p.parse_page(TESTDATA / "MainWindow.xaml")
    cpp = render_one(p, "app.xaml.cpp")
    h = render_one(p, "app.xaml.h")
    print(cpp)
    print(h)
