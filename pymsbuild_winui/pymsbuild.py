import os
import sys

from pathlib import Path
from pymsbuild import CSourceFile, File, IncludeFile, Midl, Property, PydFile


__all__ = [
    'WinUIExe',
    'XamlApp',
    'XamlPage',
]


TARGETS = Path(__file__).absolute().parent / "targets"


class XamlPage(File):
    _ITEMNAME = "Page"
    options = {
        "IncludeInSdist": True,
        "IncludeInLayout": False,
        "IncludeInWheel": False,
    }


class XamlApp(XamlPage):
    _ITEMNAME = "ApplicationDefinition"


class WinUIExe(PydFile):
    class WinUIProps:
        members = ()
        name = "$WinUIExe.WinUIProps"
        def write_member(self, f, g):
            import pybind11
            g.switch_to("PropertyGroup")
            f.add_property("_WinUITargetsPath", TARGETS)
            f.add_property("_PyBind11IncludePath", pybind11.get_include()),
            g.switch_to(None)
            f.add_import(f"$(_WinUITargetsPath){os.path.sep}winui.props")

    class WinUITargets:
        members = ()
        name = "$WinUIExe.WinUITargets"
        def write_member(self, f, g):
            g.switch_to(None)
            f.add_import(f"$(_WinUITargetsPath){os.path.sep}winui.targets")

    def __init__(self, name, *members, project_file=None, **kwargs):
        kwargs.setdefault("ConfigurationType", "Application")
        kwargs["TargetExt"] = ".exe"
        super().__init__(name, *members, project_file=project_file, **kwargs)
        self._embed_tag = Property("PythonRuntimeTag", "")
        self.insert(PydFile.GlobalProperties.name,
                    [self.WinUIProps(), self._embed_tag],
                    offset=1, range=True)
        self.members.append(self.WinUITargets())

    def init_PACKAGE(self, tag):
        if not tag:
            return
        # Restore our build packages before build begins
        import subprocess
        dest = os.getenv("PYMSBUILD_WINUIPACKAGES") or TARGETS
        subprocess.check_call([sys.executable, TARGETS / "restore.py", "-o", dest])

        # Provide wheel tag so we embed the correct CPython build
        self._embed_tag.value = tag
