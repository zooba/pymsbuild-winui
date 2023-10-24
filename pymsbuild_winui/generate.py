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
    "datetime": "winrt::Windows::Foundation::DateTime",
    "timedelta": "winrt::Windows::Foundation::TimeSpan",
    "str": "winrt::hstring",
    "float": "double",
    "UUID": "GUID",
}


PROPERTY_IDLTYPE_MAP = {
    "uint8_t": "UInt8",
    "uint16_t": "UInt16",
    "uint32_t": "UInt32",
    "uint64_t": "UInt64",
    "int16_t": "Int16",
    "int32_t": "Int32",
    "int64_t": "Int64",
    "wchar_t": "Char",
    "std::wstring": "String",
    "winrt::hstring": "String",
    "float": "Single",
    "double": "Double",
    "bool": "Boolean",
    "GUID": "Guid",
    "winrt::Windows::Foundation::DateTime": "Windows.Foundation.DateTime",
    "winrt::Windows::Foundation::TimeSpan": "Windows.Foundation.TimeSpan",
}


class ParsedProperty:
    def __init__(self):
        self.type = None
        self.idltype = None
        self.name = None
        self.hold = False


class ParsedEventHandler:
    def __init__(self):
        self.name = None
        self.eventarg = None


class ParsedViewModel:
    def __init__(self):
        self.name = None
        self.properties = []

    def _property(self, e):
        p = ParsedProperty()
        p.name = e.attrib["Name"]
        p.type = e.attrib["Type"]
        p.type = PROPERTY_TYPE_MAP.get(p.type, p.type)
        try:
            p.idltype = e.attrib["IdlType"]
        except KeyError:
            p.idltype = PROPERTY_IDLTYPE_MAP.get(p.type)
        self.properties.append(p)


class ParsedControl:
    def __init__(self):
        self.name = None
        self.idltype = None


class ParsedPage:
    def __init__(self, filename, version="0.0.0.0"):
        self.filename = filename
        self.basename = PurePath(filename).name
        self.version = version
        self.name = None
        self.properties = []
        self.handlers = []
        self.viewmodels = []
        self.controls = []
        self.types = set()

    def _property(self, e):
        p = ParsedProperty()
        p.name = e.attrib["Name"]
        p.type = e.attrib["Type"]
        p.type = PROPERTY_TYPE_MAP.get(p.type, p.type)
        try:
            p.idltype = e.attrib["IdlType"]
        except KeyError:
            p.idltype = PROPERTY_IDLTYPE_MAP.get(p.type)
        self.properties.append(p)

    def _handler(self, e):
        h = ParsedEventHandler()
        h.name = e.attrib["Name"]
        try:
            h.sender = e.attrib["Sender"]
        except KeyError:
            h.sender = "Control"
        try:
            h.eventarg = e.attrib["EventArg"]
        except KeyError:
            h.eventarg = "RoutedEventArgs"
        self.handlers.append(h)
        self.types.add(h.sender)
        self.types.add(h.eventarg)

    def _control(self, e):
        c = ParsedControl()
        c.name = e.attrib[QN(NS["x"], "Name")]
        c.idltype = e.tag.partition("}")[2]
        self.controls.append(c)
        self.types.add(c.name)

    def _viewmodel(self, e):
        m = ParsedViewModel()
        m.name = e.attrib["Name"]
        for p in e.findall("py:Property", NS):
            m._property(p)
        self.viewmodels.append(m)


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
        for e in root.findall("py:ViewModel", NS):
            page._viewmodel(e)
        for e in root.findall("**[@x:Name]", NS):
            page._control(e)

        return page

    def _open_files(self, force=False, **files):
        ignore = []
        if not force:
            for k, v in files.items():
                try:
                    with open(v, "r", encoding="utf-8-sig") as f:
                        for i, line in zip(range(8), f):
                            if "-autogen:true" in line.lower().replace(" ", ""):
                                break
                        else:
                            ignore.append(k)
                except IOError:
                    pass
        return {k: (open(v, "w", encoding="utf-8") if k not in ignore else None)
                for k, v in files.items()}

    def open_app_files(self, force=False):
        return self._open_files(
            force,
            cpp_file=f"{self.app.basename}.cpp",
            h_file=f"{self.app.basename}.h",
            idl_file=f"{self.app.basename.rpartition('.')[0]}.idl",
            manifest_file=f"app.manifest",
            pch_file=f"pch.h",
        )

    def open_page_files(self, page, force=False):
        return self._open_files(
            force,
            cpp_file=f"{page.basename}.cpp",
            h_file=f"{page.basename}.h",
            idl_file=f"{page.basename.rpartition('.')[0]}.idl",
        )

    def render_app(self, cpp_file, h_file, idl_file, manifest_file, pch_file):
        context = {
            "app": self.app,
            "page": self.pages[0],
            "pages": self.pages,
            "namespace": self.namespace,
        }
        for tmpl, file in [
            ("app.xaml.cpp.in", cpp_file),
            ("app.xaml.h.in", h_file),
            ("app.idl.in", idl_file),
            ("app.manifest.in", manifest_file),
            ("pch.h.in", pch_file),
        ]:
            if file:
                for s in RENDER_ENV.get_template(tmpl).generate(context):
                    file.write(s)
        
        
    def render_page(self, page, cpp_file, h_file, idl_file):
        if not isinstance(page, ParsedPage):
            page = [p for p in self.pages if p.basename == page][0]
        context = {
            "app": self.app,
            "page": page,
            "pages": self.pages,
            "namespace": self.namespace,
        }
        for tmpl, file in [
            ("page.xaml.cpp.in", cpp_file),
            ("page.xaml.h.in", h_file),
            ("page.idl.in", idl_file),
        ]:
            if file:
                for s in RENDER_ENV.get_template(tmpl).generate(context):
                    file.write(s)


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        args.remove("-f")
        force = True
    except ValueError:
        force = False

    p = Parser()
    app = None
    to_write = []
    for f in args:
        if f.startswith("--app:"):
            app = p.parse_app(f[6:])
        else:
            to_write.append(p.parse_page(f))

    if app:
        p.render_app(**p.open_app_files(force=force))
    for f in to_write:
        p.render_page(f, **p.open_page_files(f, force=force))

