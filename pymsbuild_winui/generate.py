from pathlib import Path, PurePath
import jinja2
import xml.etree.ElementTree as ET
import sys

QN = ET.QName

NS = {
    "xml": "http://www.w3.org/XML/1998/namespace",
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


TARGETS = Path(__file__).absolute().parent / "targets"
WINUI_MODULES = [f.stem for f in TARGETS.glob("_winui*.cpp")]

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
    "object": "winrt::Windows::Foundation::IInspectable",
    "list": "winrt::Windows::Foundation::Collections::IVector",
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
    "winrt::Windows::Foundation::IInspectable": "IInspectable",
    "winrt::Windows::Foundation::DateTime": "Windows.Foundation.DateTime",
    "winrt::Windows::Foundation::TimeSpan": "Windows.Foundation.TimeSpan",
    "winrt::Windows::Foundation::Collections::IVector": "Windows.Foundation.Collections.IVector",
}

PROPERTYTYPE_TREAT_ELEMENT_AS_OBJECT = {
    "winrt::Windows::Foundation::Collections::IVector",
}

IDLTYPE_TREAT_ELEMENT_AS_OBJECT = {
    "Windows.Foundation.Collections.IVector",
}

def _map_property_type(type):
    type, _, generic = type.strip().partition("[")
    if generic:
        generics = ','.join(_map_property_type(g) for g in generic.rstrip("]").split(","))
    else:
        generics = []
    try:
        type = PROPERTY_TYPE_MAP[type]
    except LookupError:
        type = type.replace(".", "::")
        if "::" in type and not type.startswith("winrt::"):
            type = f"winrt::{type}"
    if type in PROPERTYTYPE_TREAT_ELEMENT_AS_OBJECT and generics:
        generics = ",".join("winrt::Windows::Foundation::IInspectable" for _ in generics.split(","))
    return f"{type}<{generics}>" if generics else type

def _map_idl_type(property_type):
    type, _, generic = property_type.strip().partition("<")
    if generic:
        generics = ','.join(_map_idl_type(g) for g in generic.rstrip(">").split(","))
    else:
        generics = []
    try:
        type = PROPERTY_IDLTYPE_MAP[type]
    except LookupError:
        type = type.replace("::", ".").removeprefix("winrt.")
    if generics and type in IDLTYPE_TREAT_ELEMENT_AS_OBJECT:
        generics = ",".join("IInspectable" for _ in generics.split(","))
    return f"{type}<{generics}>" if generics else type


def _map_default_value(prop_type, value):
    if not value:
        return "nullptr"
    if prop_type == "winrt::hstring":
        if value.startswith(('"', "'")) and value.endswith(p[0]):
            value = value[1:-1]
        # TODO: Full escaping
        value = (value
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )
        return '"{}"'.format(value)
    return value


class ParsedProperty:
    def __init__(self, e=None):
        self.type = None
        self.idltype = None
        self.name = None
        if e is not None:
            self.name = e.attrib["Name"]
            self.type = _map_property_type(e.attrib["Type"])
            self.idltype = e.attrib.get("IdlType", _map_idl_type(self.type))
            try:
                default = e.attrib["Default"]
            except LookupError:
                default = e.find("py:Property.Default", NS)
                if default is not None:
                    if default.attrib.get(QN(NS["xml"], "space")) == "preserve":
                        default = default.text
                    else:
                        default = default.text.strip()
            self.default = _map_default_value(self.type, default)

    @property
    def elemtype(self):
        if not self.idltype.startswith("Windows.Foundation.Collections.IVector<"):
            return None
        return self.type.partition("<")[2].removesuffix(">")


class ParsedEventHandler:
    def __init__(self):
        self.name = None
        self.eventarg = None


class ParsedViewModel:
    def __init__(self):
        self.name = None
        self.properties = []

    def _property(self, e):
        p = ParsedProperty(e)
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

    @property
    def all_elemtypes(self):
        return {
            p.elemtype: p
            for vm in [self, *self.viewmodels]
            for p in vm.properties
            if p.elemtype
        }.values()

    def _property(self, e):
        p = ParsedProperty(e)
        self.properties.append(p)

    def _handler(self, e):
        h = ParsedEventHandler()
        h.name = e.attrib["Name"]
        h.sender = e.attrib.get("Sender", "IInspectable")
        h.eventarg = _map_property_type(e.attrib.get("EventArgs", "RoutedEventArgs"))
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
        )

    def open_page_files(self, page, force=False):
        return self._open_files(
            force,
            cpp_file=f"{page.basename}.cpp",
            h_file=f"{page.basename}.h",
            idl_file=f"{page.basename.rpartition('.')[0]}.idl",
        )

    def render_app(self, cpp_file, h_file, idl_file, manifest_file):
        context = {
            "winui_modules": WINUI_MODULES,
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

