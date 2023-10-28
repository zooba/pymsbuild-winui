# pymsbuild-winui

This is a highly experimental and early stage extension to
[pymsbuild](https://pypi.org/project/pymsbuild). It uses the Microsoft
Windows App SDK to build GUI apps based on XAML.

The sample projects in [testdata/app1](https://github.com/zooba/pymsbuild-winui/tree/master/tests/testdata/app1)
and [testdata/BasicPhotoViewer](https://github.com/zooba/pymsbuild-winui/tree/master/tests/testdata/BasicPhotoViewer)
are currently the best starting point.

Good luck!

(Expressions of interest are welcome right now, but not contributions.)

# Quick Start

In your `_msbuild.py`, import `WinUIExe`, `XamlApp` and `XamlPage` from
`pymsbuild_winui` (using `import *` is okay).

The `WinUIExe` element will take the `XamlApp` and one or more
`XamlPage`s and generate an executable file along with _a lot_ of
support files. The package this element goes into should contain the
Python sources and any other content, but only XAML items should be in
the `WinUIExe` itself.

The name of the `WinUIExe` must match the namespaces used in the XAML
files `x:Class` attributes, and must also be an importable Python
module that will contain the implementation of each page.

```python
from pymsbuild import *
from pymsbuild_winui import *

METADATA = {...}

PACKAGE = Package(
    'PhotoViewerApp',
    PyFile("PhotoViewer.py"),
    PyFile("image_info.py"),
    WinUIExe(
        "PhotoViewer",
        XamlApp("app.xaml"),
        XamlPage("MainWindow.xaml"),
    ),
)

def init_PACKAGE(tag):
    # WinUIExe needs to be passed the wheel tag to complete setup
    PACKAGE.find("PhotoViewer").init_PACKAGE(tag)
```

In the main Python module (`PhotoViewer.py` in the above example), each
XAML page must have a class with matching name and the initializer
shown below.

```python
class MainWindow:
    def __init__(self, view, viewmodels):
        ...
```

The `view` argument is a reference to the XAML instance. You should
keep this around as `self.view` to use it later.

The `viewmodels` argument has each defined viewmodel as an attribute.
You should now update the `view.models` dict to map your model types to
their viewmodels. This will enable `view.wrap()` and `view.unwrap()` to
work.

```python
    self.view.models[image_info.ImageInfo] = viewmodels.ImageInfo
    self.view.models[image_info.ImagesRepository] = viewmodels.ImageRepository
```

The `view` object also contains any properties that were defined in the
XAML. Properties and viewmodels use a private XML namespace that is
processed at build time.

```xml
    ...
    xmlns:py="http://schemas.stevedower.id.au/pymsbuild/winui"
    ...
    <py:ViewModel Name="ImageInfo">
        <py:Property Name="Name" Type="str" />
        <py:Property Name="Path" Type="str" />
    </py:ViewModel>
    <py:ViewModel Name="ImageRepository">
        <py:Property Name="Images" Type="list[object]" />
    </py:ViewModel>
    <py:Property Name="ImagesRepository" Type="PhotoViewer.ImageRepository" />
```

Property types are _very_ limited, try to stick to primitives or
other viewmodels. Notice that the viewmodel type must include the
namespace, which is implicitly added to the name specified when
defining it.

Event handlers must also be defined (for now), and also defined on your
Python class. They are hooked up using normal XAML specifications.

```xml
    <py:EventHandler Name="ImageClick" />
    <py:EventHandler Name="OnElementPointerEntered" EventArgs="Microsoft.UI.Xaml.Input.PointerRoutedEventArgs" />
```

Arguments are passed through with exactly the type they are defined as,
which often means `sender` will need to be down-cast in order to access
its members. The `.as_()` function takes a fully qualified name as a
string, and will raise if the conversion fails. The `e` argument will
already be usable as the type specified in the `EventArgs` attribute.

```python
    def ImageClick(self, sender, e):
        sender = sender.as_("Microsoft.UI.Xaml.Controls.Control")
        ...

    def OnElementPointerEntered(self, sender, e):
        ...
```

Finally, the `view` object contains any controls that were named with
`x:Name` in the XAML. In general, it is best to avoid working with
controls directly, and instead try to use XAML bindings (`{x:bind}`) to
properties and viewmodels. All properties and viewmodels provide update
notifications, and so `Text="{x:bind Message,Mode=OneWay}"` is more efficient
than writing `self.view.StatusControl.Text = Message`.
