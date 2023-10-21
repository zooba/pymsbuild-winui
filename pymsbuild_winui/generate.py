from pathlib import Path, PurePath
import jinja2
import xml.etree.ElementTree as ET
import sys

QN = ET.QName

NS = {
    "": "http://schemas.microsoft.com/winfx/2006/xaml/presentation",
    "x": "http://schemas.microsoft.com/winfx/2006/xaml",
    "d": "http://schemas.microsoft.com/expression/blend/2008",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "py": "http://schemas.stevedower.id.au/pymsbuild/winui",
    "local": "local",
}

NS_T = {
    **{v: k for k, v in NS.items()},
}


RENDER_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader("pymsbuild_winui"),
    trim_blocks=True,
)


def short_name(text):
    if text.startswith("{"):
        ns, _, tag = text.partition("}")
        if ns and tag:
            ns = NS_T.get(ns[1:])
            if ns:
                return f"{ns}:{tag}"
            return tag
    return text


PROPERTY_TYPE_MAP = {
    "str": "std::wstring",
}


class ParsedProperty:
    def __init__(self):
        self.type = None
        self.name = None

class ParsedEventHandler:
    def __init__(self):
        self.name = None
        self.eventarg = None

class ParsedControl:
    def __init__(self):
        self.name = None

class ParsedPage:
    def __init__(self, filename):
        self.filename = filename
        self.basename = PurePath(filename).name
        self.name = None
        self.properties = []
        self.handlers = []
        self.controls = []

    def _property(self, e):
        p = ParsedProperty()
        p.name = e.attrib["Name"]
        p.type = e.attrib["Type"]
        p.type = PROPERTY_TYPE_MAP.get(p.type, p.type)
        self.properties.append(p)

    def _handler(self, e):
        h = ParsedEventHandler()
        h.name = e.attrib["Name"]
        try:
            h.eventarg = e.attrib["EventArg"]
        except KeyError:
            h.eventarg = "RoutedEventArgs"
        self.handlers.append(h)

    def _control(self, e):
        c = ParsedControl()
        c.name = e.attrib[QN(NS["x"], "Name")]
        self.controls.append(c)


class Parser:
    def __init__(self):
        self.pymsbuild_winui_version = "0.1"
        self.app = None
        self.pages = []
        self.namespace = None

    def parse_app(self, filename, file=None, root=None):
        if self.app is not None:
            raise ValueError(f"Already parsed app '{self.app.filename}'")
        self.app = self._parse_page(filename, file, root)
        return self.app

    def parse_page(self, filename, file=None, root=None):
        page = self._parse_page(filename, file, root)
        self.pages.append(page)
        return page

    def _parse_page(self, filename, file=None, root=None):
        if root is None:
            if file is None:
                with open(filename, "r", encoding="utf-8") as f:
                    return self._parse_page(filename, f, None)
            root = ET.parse(file).getroot()

        page = ParsedPage(filename)
        name = root.attrib[QN(NS["x"], "Class")]
        namespace, _, page.name = name.partition(".")
        if not namespace or not page.name or "." in page.name:
            raise ValueError(f"Unsupported class name '{name}'")
        if self.namespace is None:
            self.namespace = namespace
        elif self.namespace != namespace:
            raise ValueError(f"All pages must be in namespace '{self.namespace}'")

        for e in root.findall("py:Property", NS):
            page._property(e)
        for e in root.findall("py:EventHandler", NS):
            page._handler(e)
        for e in root.findall("**[@x:Name]", NS):
            page._control(e)

        return page

    def render_app(self, cpp_file, h_file):
        t_cpp = RENDER_ENV.get_template("app.xaml.cpp.in")
        t_h = RENDER_ENV.get_template("app.xaml.h.in")
        context = {
            "app": self.app,
            "page": self.pages[0],
            "pages": self.pages,
            "namespace": self.namespace,
        }
        for s in t_cpp.generate(context):
            cpp_file.write(s)
        for s in t_h.generate(context):
            h_file.write(s)
        
    def render_page(self, basename, cpp_file, h_file):
        t_cpp = RENDER_ENV.get_template("page.xaml.cpp.in")
        t_h = RENDER_ENV.get_template("page.xaml.h.in")
        context = {
            "app": self.app,
            "page": [p for p in self.pages if p.basename == basename][0],
            "pages": self.pages,
            "namespace": self.namespace,
        }
        for s in t_cpp.generate(context):
            cpp_file.write(s)
        for s in t_h.generate(context):
            h_file.write(s)

