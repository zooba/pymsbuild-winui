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
    assert [vars(p) for p in page.properties] == [{"name": "MyProperty", "type": "int32_t", "idltype": "Int32"}]
    assert [vars(h) for h in page.handlers] == [{"name": "myButton_Click", "eventarg": "RoutedEventArgs", "sender": "IInspectable"}]
    assert [vars(c) for c in page.controls] == [{"name": "myButton", "idltype": "Button"}]


def test_basic_app_parse():
    p = Parser()
    app = p.parse_app(TESTDATA / "App.xaml")
    assert app is p.app
    assert app.basename == "App.xaml"
    assert app.name == "App"
    assert p.namespace == "app"


def test_basic_generate():
    p = Parser()
    p.parse_page(TESTDATA / "MainWindow.xaml")
    cpp = StringIO()
    h = StringIO()
    p.render_page("MainWindow.xaml", cpp, h, None)
    cpp, h = cpp.getvalue(), h.getvalue()
    print(cpp)
    print(h)
    #assert 0


def test_basic_app_generate():
    p = Parser()
    p.parse_app(TESTDATA / "App.xaml")
    p.parse_page(TESTDATA / "MainWindow.xaml")
    cpp = StringIO()
    h = StringIO()
    p.render_app(cpp, h, None, None)
    cpp, h = cpp.getvalue(), h.getvalue()
    print(cpp)
    print(h)
