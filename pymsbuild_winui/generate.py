import jinja2
import os
import sys
import xml.etree.ElementTree as ET

from pathlib import Path, PurePath

from ._controldata import *

QN = ET.QName

NS = {
    "xml": "http://www.w3.org/XML/1998/namespace",
    "": "http://schemas.microsoft.com/winfx/2006/xaml/presentation",
    "_": "http://schemas.microsoft.com/winfx/2006/xaml/presentation",
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
        h.eventarg = _map_property_type(e.attrib.get("EventArgs", "Microsoft.UI.Xaml.RoutedEventArgs"))
        self.handlers.append(h)
        self.types.add(h.sender)
        self.types.add(h.eventarg)

    def _control_handler(self, e, n):
        if any(h.name == e.attrib[n] for h in self.handlers):
            return
        try:
            sender, eventarg = KNOWN_EVENTS[short_name(e.tag), n]
        except LookupError:
            return
        h = ParsedEventHandler()
        h.name = e.attrib[n]
        if "." not in sender:
            sender = f"Microsoft.UI.Xaml.Controls.{sender}"
        if not eventarg:
            eventarg = "Microsoft.UI.Xaml.RoutedEventArgs"
        elif "." not in eventarg:
            eventarg = f"Microsoft.UI.Xaml.Controls.{eventarg}"
        h.sender = _map_property_type(sender)
        h.eventarg = _map_property_type(eventarg)
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
        for n in KNOWN_EVENT_NAMES:
            for e in root.findall(f"*//_:*[@{n}]", NS):
                page._control_handler(e, n)
        for e in root.findall("py:ViewModel", NS):
            page._viewmodel(e)
        for e in root.findall("**[@x:Name]", NS):
            page._control(e)

        return page

    def get_context(self):
        return {
            "winui_modules": WINUI_MODULES,
            "app": self.app,
            "mainpage": self.pages[0],
            "pages": self.pages,
            "namespace": self.namespace,
        }

    def get_templates(self):
        """Returns a sequence of (template, additional_context_dict, output_filename)"""
        app_ctxt = {"page": self.pages[0]}
        g = RENDER_ENV.get_template
        if self.app:
            yield g("app.xaml.cpp.in"), app_ctxt, f"{self.app.basename}.cpp"
            yield g("app.xaml.h.in"), app_ctxt, f"{self.app.basename}.h"
            yield g("app.idl.in"), app_ctxt, f"{self.app.basename.rpartition('.')[0]}.idl"
            yield g("app.manifest.in"), app_ctxt, "app.manifest"
        for p in self.pages:
            page_ctxt = {"page": p}
            yield g("page.xaml.cpp.in"), page_ctxt, f"{p.basename}.cpp"
            yield g("page.xaml.h.in"), page_ctxt, f"{p.basename}.h"
            yield g("page.idl.in"), page_ctxt, f"{p.basename.rpartition('.')[0]}.idl"


def should_regen(buffer):
    if b'autoregen' not in buffer:
        return False
    if b'-autoregen:true' in buffer.lower().replace(b' ', b''):
        return True
    return False


def maybe_write_template(template, context, dest, force=False):
    read_f = write_f = None
    if not force:
        try:
            read_f = open(dest, "rb")
        except FileNotFoundError:
            pass
        else:
            check_buf = read_f.read(1024)
            read_f.seek(0)
            if not should_regen(check_buf):
                read_f.close()
                return False
    if not read_f:
        write_f = open(dest, "wb")

    chunks = []
    for s in template.generate(context):
        s = s.encode("ascii").replace(b"\n", b"\r\n")
        if read_f:
            if read_f.read(len(s)) == s:
                chunks.append(s)
            else:
                read_f.close()
                read_f = None
                write_f = open(dest, "wb")
                for c in chunks:
                    write_f.write(c)
                chunks = None
        if write_f:
            write_f.write(s)
    if write_f:
        tell = write_f.tell()
        write_f.close()
        os.truncate(dest, tell)
        return True
    return False



if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        args.remove("-f")
        force = True
    except ValueError:
        force = False

    try:
        args.remove("-q")
        quiet = True
    except ValueError:
        quiet = False

    OUT = Path.cwd()
    p = Parser()
    for f in args:
        if f.startswith("-o:"):
            OUT = Path(f[3:])
        elif f.startswith("--app:"):
            p.parse_app(f[6:])
        else:
            p.parse_page(f)

    base_ctxt = p.get_context()
    for tmpl, ctxt, dest in p.get_templates():
        if maybe_write_template(
            tmpl,
            {**base_ctxt, **ctxt},
            OUT / dest,
            force=force,
        ):
            if not quiet:
                print("[pymsbuild-winui] Updating", dest)
        else:
            if not quiet:
                print("[pymsbuild-winui] No updates to", dest)
