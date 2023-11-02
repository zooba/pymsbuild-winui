import copy
import jinja2
import os
import sys

from pathlib import Path

FORCE = "-f" in sys.argv
ROOT = Path(__file__).absolute().parent
OUTPUT = ROOT.parent / "pymsbuild_winui" / "targets" / "_winui"
CONTROLDATA_OUTPUT = ROOT.parent / "pymsbuild_winui" / "_controldata.py"

# Number of types to define in the same .cpp file
# Smaller numbers means more build parallelisation
TYPE_CHUNK_SIZE = 100

RENDER_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ROOT),
    trim_blocks=True,
)

def _split_type(type):
    type = type.replace("::", ".")
    ns, _, type = type.rpartition(".")
    if not ns and type in {"bool", "int", "float", "double", "uint32_t"}:
        ns = "__"
    return ns, type

def _join_type(namespace, name):
    if namespace and namespace != "__":
        return f"{namespace}.{name}"
    return name

ALL_TYPES = []

def collect(ns, **members):
    for k, v in members.items():
        try:
            make_info = v.make_info
        except AttributeError:
            ALL_TYPES.append(TypeInfo(ns, k, v))
        else:
            ALL_TYPES.append(make_info(ns, k))


# The BaseInfo and TypeInfo classes are passed into the jinja
# environment when constructing the template. BaseInfo is typically
# subclassed and instatiated directly in the namespace dicts, while
# ControlInfos are specified as plain old dicts and converted later.

class BaseInfo:
    def __init__(self, namespace="", name=None, members=None):
        self.name = name
        self.namespace = namespace
        self.members = members if members is not None else {}

    def __repr__(self):
        return f"<{self.fullname}>"

    @property
    def fullname(self):
        return _join_type(self.namespace, self.name)

    @property
    def cppname(self):
        return self.fullname.replace(".", "::")

    def make_info(self, namespace, name):
        if not self.namespace:
            self.namespace = namespace
        self.name = name
        return self


class StructInfo(BaseInfo):
    kind = "struct"

    def __init__(self, namespace="", **members):
        super().__init__(namespace, None, members)


class CallbackInfo(BaseInfo):
    kind = "callback"

    @property
    def backing_name(self):
        return f"_Callback_{self.fullname}".replace(".", "_")


class TypeInfo(BaseInfo):
    kind = "runtimeclass"

    def __init__(self, namespace, name, members):
        super().__init__(namespace, name, members)
        try:
            self.namespace = members.pop("__namespace__")
        except KeyError:
            pass
        try:
            self.bases = list(members.pop("__bases__"))
        except KeyError:
            try:
                self.bases = [members.pop("__base__")]
            except KeyError:
                self.bases = []
        # pybind11 can't see all the conversions between classes in
        # the cppwinrt hierarchy, so we only allow casting down to
        # IInspectable, but then copy all the members everywhere.
        # The "__implements__" member list allows implicit casting
        # as part of our own function calls.
        self.basespec = ", Windows::Foundation::IInspectable"
        if self.bases:
            self.bases = [f"{namespace}.{b}" if "." not in b else b for b in self.bases]


class EnumInfo(BaseInfo):
    kind = "enum"
    def __init__(self, *names, namespace=""):
        super().__init__(namespace)
        self.members = names


class AsyncOpInfo(BaseInfo):
    kind = "asyncop"
    def __init__(self, type, namespace=""):
        ns, type = _split_type(type)
        super().__init__(namespace or ns)
        self.result = type

    def make_info(self, namespace, name):
        # Keep the name we were originally provided
        return super().make_info(namespace, self.result)


class CallbackInfo(BaseInfo):
    kind = "callback"
    def __init__(self, void=False, **kwargs):
        super().__init__()
        self.void = void
        self.namespace = None
        self._args = list(kwargs.items())

    @property
    def args(self):
        return [ARG.make(n, t, self.namespace) for n, t in self._args]


class CALL:
    kind = "call"
    def __init__(self, cvt="", void=False, **kwargs):
        self.cvt = cvt
        # We can infer the actual return value, but also inferring
        # void makes the compiler work too hard, so we do it manually.
        self.void = void
        self.namespace = None
        self._args = list(kwargs.items())

    @property
    def args(self):
        return [ARG.make(n, t, self.namespace) for n, t in self._args]


class ARG:
    kind = "arg"
    def __init__(self, type, *, name=None):
        self.namespace, self.type = _split_type(type)
        self.name = name

    @property
    def fulltype(self):
        return _join_type(self.namespace, self.type)

    @property
    def cpptype(self):
        return self.fulltype.replace('.', '::')

    @classmethod
    def make(cls, n, t, namespace):
        if not isinstance(t, cls):
            t = cls(t)
        t.name = n
        if not t.namespace:
            t.namespace = namespace
        return t


class GET:
    kind = "get"
    def __init__(self, type, cvt=""):
        self.namespace, self.type = _split_type(type)
        self.cvt = cvt

    @property
    def fullname(self):
        return _join_type(self.namespace, self.type)

    @property
    def cpptype(self):
        return self.fullname.replace(".", "::")


class GETSET(GET):
    kind = "getset"


class FIELD(GET):
    kind = "field"


class EVENT(CALL):
    kind = "event"


class XEVENT:
    kind = "xaml_event"
    def __init__(self, arg="Microsoft.UI.Xaml.RoutedEventArgs", sender=None):
        self.selftype = None
        self._arg = arg
        self._sender = sender

    @property
    def sender(self):
        return self._sender or self.selftype.fullname

    @property
    def eventargs(self):
        arg = self._arg or "Microsoft.UI.Xaml.RoutedEventArgs"
        if "." not in arg:
            arg = f"{self.selftype.namespace}.{arg}"
        return arg


ANY = "Windows.Foundation.IInspectable"
STR = "winrt::hstring"
LIST_OBJ = "Windows.Foundation.Collections.IVector<IInspectable>"


collect(
    "Microsoft.UI",
    Color=StructInfo(
        namespace="Windows.UI",
        A=FIELD("uint8_t"),
        R=FIELD("uint8_t"),
        G=FIELD("uint8_t"),
        B=FIELD("uint8_t"),
    ),
)

collect(
    "Microsoft.UI.Dispatching",
    DispatcherQueue={
        "HasThreadAccess": GET("bool"),
        "CreateTimer": CALL(),
        "TryEnqueue": CALL(priority="DispatcherQueuePriority", callback="DispatcherQueueHandler"),
    },
    DispatcherQueueHandler=CallbackInfo(void=True),
    DispatcherQueuePriority=EnumInfo("Normal", "High", "Low"),
    DispatcherQueueTimer={
        "Interval": GETSET("TimeSpan"),
        "IsRepeating": GETSET("bool"),
        "IsRunning": GET("bool"),
        "Start": CALL(void=True),
        "Stop": CALL(void=True),
        "Tick": EVENT(sender="DispatcherQueueTimer", args=ANY),
    },
)

collect(
    "Microsoft.UI.Composition",
    AmbientLight={},
    AnimationController={},
    AnimationControllerProgressBehavior=EnumInfo(),
    AnimationDelayBehavior=EnumInfo(),
    AnimationDirection=EnumInfo(),
    AnimationIterationBehavior=EnumInfo(),
    AnimationPropertyAccessMode=EnumInfo(),
    AnimationPropertyInfo={},
    AnimationStopBehavior=EnumInfo(),
    BackEasingFunction={},
    BooleanKeyFrameAnimation={},
    BounceEasingFunction={},
    BounceScalarNaturalMotionAnimation={},
    BounceVector2NaturalMotionAnimation={},
    BounceVector3NaturalMotionAnimation={},
    CircleEasingFunction={},
    ColorKeyFrameAnimation={},
    CompositionAnimation={
        "__base__": "CompositionObject",
        "__implements__": ["Microsoft::UI::Composition::ICompositionAnimationBase"],
        "InitialValueExpressions": GET("InitialValueExpressionCollection"),
        "Target": GETSET(STR),
    },
    CompositionAnimationGroup={},
    CompositionApiInformation=StructInfo(),
    CompositionBackdropBrush={},
    CompositionBackfaceVisibility=EnumInfo(),
    CompositionBatchCompletedEventArgs={},
    CompositionBatchTypes=EnumInfo(),
    CompositionBitmapInterpolationMode=EnumInfo(),
    CompositionBorderMode=EnumInfo(),
    CompositionBrush={},
    CompositionCapabilities={},
    CompositionClip={},
    CompositionColorBrush={},
    CompositionColorGradientStop={},
    CompositionColorGradientStopCollection={},
    CompositionColorSpace=EnumInfo(),
    CompositionCommitBatch={},
    CompositionCompositeMode=EnumInfo(),
    CompositionContainerShape={},
    CompositionDrawingSurface={},
    CompositionDropShadowSourcePolicy=EnumInfo(),
    CompositionEasingFunction={},
    CompositionEasingFunctionMode=EnumInfo(),
    CompositionEffectBrush={},
    CompositionEffectFactory={},
    CompositionEffectFactoryLoadStatus=EnumInfo(),
    CompositionEffectSourceParameter={},
    CompositionEllipseGeometry={},
    CompositionGeometricClip={},
    CompositionGeometry={},
    CompositionGetValueStatus=EnumInfo(),
    CompositionGradientBrush={},
    CompositionGradientExtendMode=EnumInfo(),
    CompositionGraphicsDevice={},
    CompositionLight={},
    CompositionLinearGradientBrush={},
    CompositionLineGeometry={},
    CompositionMappingMode=EnumInfo(),
    CompositionMaskBrush={},
    CompositionMipmapSurface={},
    CompositionNineGridBrush={},
    CompositionObject={},
    CompositionPath={},
    CompositionPathGeometry={},
    CompositionProjectedShadow={},
    CompositionProjectedShadowCaster={},
    CompositionProjectedShadowCasterCollection={},
    CompositionProjectedShadowReceiver={},
    CompositionProjectedShadowReceiverUnorderedCollection={},
    CompositionPropertySet={},
    CompositionRadialGradientBrush={},
    CompositionRectangleGeometry={},
    CompositionRoundedRectangleGeometry={},
    CompositionScopedBatch={},
    CompositionShadow={},
    CompositionShape={},
    CompositionShapeCollection={},
    CompositionSpriteShape={},
    CompositionStretch=EnumInfo(),
    CompositionStrokeCap=EnumInfo(),
    CompositionStrokeDashArray={},
    CompositionStrokeLineJoin=EnumInfo(),
    CompositionSurfaceBrush={},
    CompositionTransform={},
    CompositionViewBox={},
    CompositionVirtualDrawingSurface={},
    CompositionVisualSurface={},
    Compositor={
        "CreateSpringVector3Animation": CALL(),
    },
    ContainerVisual={},
    CubicBezierEasingFunction={},
    DistantLight={},
    DropShadow={},
    ElasticEasingFunction={},
    ExponentialEasingFunction={},
    ExpressionAnimation={
        "__base__": "CompositionAnimation",
    },
    ImplicitAnimationCollection={},
    InitialValueExpressionCollection={},
    InsetClip={},
    KeyFrameAnimation={
        "__base__": "CompositionAnimation",
    },
    LayerVisual={},
    LinearEasingFunction={},
    NaturalMotionAnimation={
        "__base__": "CompositionAnimation",
    },
    PathKeyFrameAnimation={},
    PointLight={},
    PowerEasingFunction={},
    QuaternionKeyFrameAnimation={},
    RectangleClip={},
    RedirectVisual={},
    RenderingDeviceReplacedEventArgs={},
    ScalarKeyFrameAnimation={},
    ScalarNaturalMotionAnimation={},
    ShapeVisual={},
    SineEasingFunction={},
    SpotLight={},
    SpringScalarNaturalMotionAnimation={},
    SpringVector2NaturalMotionAnimation={},
    SpringVector3NaturalMotionAnimation={
        "__base__": "Vector3NaturalMotionAnimation",
        "DampingRatio": GETSET("float"),
        "Period": GETSET("TimeSpan"),
    },
    SpriteVisual={},
    StepEasingFunction={},
    Vector2KeyFrameAnimation={},
    Vector2NaturalMotionAnimation={},
    Vector3KeyFrameAnimation={},
    Vector3NaturalMotionAnimation={
        "__base__": "NaturalMotionAnimation",
        "InitialValue": GETSET("Vector3", cvt="cvt_vector3_opt"),
        "FinalValue": GETSET("Vector3", cvt="cvt_vector3_opt"),
        "InitialVelocity": GETSET("Vector3", cvt="cvt_vector3"),
    },
    Vector4KeyFrameAnimation={},
    Visual={},
    VisualCollection={},
    VisualUnorderedCollection={},
)

collect(
    "Windows.ApplicationModel.DataTransfer",
    DataPackageOperation=EnumInfo("None", "Copy", "Move", "Link"),
    DataPackage={
        #"Properties"
        "RequestedOperation": GETSET("DataPackageOperation"),
        "SetApplicationLink": CALL(value="Windows.Foundation.Uri", void=True),
        #"SetBitmap": CALL(value=stream),
        "SetData": CALL(formatId=STR, value=ANY, void=True),
        #"SetDataProvider": CALL(formatId=STR, delayRenderer="DataProviderHandler", void=True),
        "SetHtmlFormat": CALL(value=STR, void=True),
        "SetRtf": CALL(value=STR, void=True),
        "SetText": CALL(value=STR, void=True),
        "SetWebLink": CALL(value="Windows.Foundation.Uri", void=True),
    },
)

collect(
    "Microsoft.UI.Xaml",
    Visibility=EnumInfo("Visible", "Collapsed"),
    BringIntoViewOptions={
        "__init__": CALL(),
        "HorizontalAlignmentRatio": GETSET("double"),
        "HorizontalOffset": GETSET("double"),
        "VerticalAlignmentRatio": GETSET("double"),
        "VerticalOffset": GETSET("double"),
    },
    BringIntoViewRequestedEventArgs={},
    DataContextChangedEventArgs={"Handled": GETSET("bool"), "NewValue": GET(ANY)},
    DependencyObject={},
    DependencyProperty={},
    DependencyPropertyChangedEventArgs={
        "NewValue": GET(ANY),
        "OldValue": GET(ANY),
        "Property": GET("DependencyProperty"),
    },
    DragEventArgs={},
    DragStartingEventArgs={},
    DropCompletedEventArgs={},
    EffectiveViewportChangedEventArgs={
        "BringIntoViewDistanceX": GET("double"),
        "BringIntoViewDistanceY": GET("double"),
        "EffectiveViewport": GET("Windows.Foundation.Rect"),
        "MaxViewport": GET("Windows.Foundation.Rect"),
    },
    ElementSoundMode=EnumInfo("Default", "FocusOnly", "Off"),
    ExceptionRoutedEventArgs={"__base__": "Microsoft.UI.Xaml.RoutedEventArgs", "ErrorMessage": GET(STR)},
    FrameworkElement={
        "__base__": "UIElement",
        "DataContext": GET(ANY),
        "ActualThemeChanged": XEVENT(ANY),
        "DataContextChanged": XEVENT("DataContextChangedEventArgs"),
        "EffectiveViewportChanged": XEVENT("EffectiveViewportChangedEventArgs"),
        "LayoutUpdated": XEVENT(ANY),
        "Loaded": XEVENT(),
        "Loading": XEVENT(ANY),
        "SizeChanged": XEVENT("SizeChangedEventHandler"),
        "Unloaded": XEVENT(),
    },
    RoutedEventArgs={"OriginalSource": GET(ANY)},
    UIElement={
        "__base__": "DependencyObject",
        "Visibility": GETSET("Visibility"),
        # Strictly should be ICompositionAnimationBase, but who's counting?
        "StartAnimation": CALL(animation="Microsoft.UI.Composition.CompositionAnimation", void=True),
        "StopAnimation": CALL(animation="Microsoft.UI.Composition.CompositionAnimation", void=True),
        "AccessKeyDisplayDismissed": XEVENT("Microsoft.UI.Xaml.Input.AccessKeyDisplayDismissedEventArgs"),
        "AccessKeyDisplayRequested": XEVENT("Microsoft.UI.Xaml.Input.AccessKeyDisplayRequestedEventArgs"),
        "AccessKeyInvoked": XEVENT("Microsoft.UI.Xaml.Input.AccessKeyInvokedEventArgs"),
        "BringIntoViewRequested": XEVENT("BringIntoViewRequestedEventArgs"),
        "CharacterReceived": XEVENT("Microsoft.UI.Xaml.Input.CharacterReceivedRoutedEventArgs"),
        "ContextCanceled": XEVENT(),
        "ContextRequested": XEVENT("Microsoft.UI.Xaml.Input.ContextRequestedEventArgs"),
        "DoubleTapped": XEVENT("Microsoft.UI.Xaml.Input.DoubleTappedRoutedEventArgs"),
        "DragEnter": XEVENT("DragEventArgs"),
        "DragLeave": XEVENT("DragEventArgs"),
        "DragOver": XEVENT("DragEventArgs"),
        "DragStarting": XEVENT("DragStartingEventArgs"),
        "Drop": XEVENT("DragEventArgs"),
        "DropCompleted": XEVENT("DropCompletedEventArgs"),
        "GettingFocus": XEVENT("Microsoft.UI.Xaml.Input.GettingFocusEventArgs"),
        "GotFocus": XEVENT(),
        "Holding": XEVENT("Microsoft.UI.Xaml.Input.HoldingEventArgs"),
        "KeyDown": XEVENT("Microsoft.UI.Xaml.Input.KeyRoutedEventArgs"),
        "KeyUp": XEVENT("Microsoft.UI.Xaml.Input.KeyRoutedEventArgs"),
        "LosingFocus": XEVENT("Microsoft.UI.Xaml.Input.LosingFocusEventArgs"),
        "LostFocus": XEVENT(),
        "ManipulationCompleted": XEVENT("Microsoft.UI.Xaml.Input.ManipulationCompletedRoutedEventArgs"),
        "ManipulationDelta": XEVENT("Microsoft.UI.Xaml.Input.ManipulationDeltaRoutedEventArgs"),
        "ManipulationInertiaStarting": XEVENT("Microsoft.UI.Xaml.Input.ManipulationInertiaStartingRoutedEventArgs"),
        "ManipulationStarted": XEVENT("Microsoft.UI.Xaml.Input.ManipulationStartedRoutedEventArgs"),
        "ManipulationStarting": XEVENT("Microsoft.UI.Xaml.Input.ManipulationStartingRoutedEventArgs"),
        "NoFocusCandidateFound": XEVENT("Microsoft.UI.Xaml.Input.NoFocusCandidateFoundEventArgs"),
        "PointerCanceled": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerCaptureLost": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerEntered": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerExited": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerMoved": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerPressed": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerReleased": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PointerWheelChanged": XEVENT("Microsoft.UI.Xaml.Input.PointerRoutedEventArgs"),
        "PreviewKeyDown": XEVENT("Microsoft.UI.Xaml.Input.KeyRoutedEventArgs"),
        "PreviewKeyUp": XEVENT("Microsoft.UI.Xaml.Input.KeyRoutedEventArgs"),
        "ProcessKeyboardAccelerators": XEVENT(),
        "RightTapped": XEVENT("Microsoft.UI.Xaml.Input.RightTappedRoutedEventArgs"),
        "Tapped": XEVENT("Microsoft.UI.Xaml.Input.TappedRoutedEventArgs"),
    },
    Window={
        "Activate": CALL(void=True),
        "Close": CALL(void=True),
        "SetTitleBar": CALL(titleBar="UIElement", void=True),
    },
    WindowEventArgs={"Handled": GETSET("bool")},
)

collect(
    "Microsoft.UI.Xaml.Controls",
    AnchorRequestedEventArgs={
        "Anchor": GET("UIElement"),
        "AnchorCandidates": GET("std::vector<UIElement>"),
    },
    #AnimatedIcon={},
    #AnimatedIconSource={},
    #AnimatedVisualPlayer={},
    AnnotatedScrollBar={
        "__base__": "Control",
    },
    AnnotatedScrollBarDetailLabelRequestedEventArgs={
        "Content": GETSET(ANY),
        "ScrollOffset": GET("double"),
    },
    AnnotatedScrollBarLabel={},
    AnnotatedScrollBarScrollingEventKind=EnumInfo("Click", "Drag", "IncrementButton", "DecrementButton"),
    AnnotatedScrollBarScrollingEventArgs={
        "Cancel": GETSET("bool"),
        "ScrollingEventKind": GET("AnnotatedScrollBarScrollingEventKind"),
        "ScrollOffset": GET("double"),
    },
    AppBar={
        "__base__": "ContentControl",
        "IsOpen": GETSET("bool"),
    },
    AppBarButton={
        "__base__": "Button",
        "Label": GETSET(STR),
    },
    #AppBarElementContainer={"__base__": "ContentControl"},
    #AppBarSeparator={"__base__": "Control"},
    AppBarToggleButton={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.ToggleButton"},
    AutoSuggestBox={
        "Text": GETSET(STR),
    },
    AutoSuggestBoxQuerySubmittedEventArgs={
        "ChosenSuggestion": GET(ANY),
        "QueryText": GET(STR),
    },
    AutoSuggestBoxSuggestionChosenEventArgs={
        "SelectedItem": GET(ANY),
    },
    AutoSuggestBoxTextChangedEventArgs={
        "CheckCurrent": CALL(),
        "Reason": GET("AutoSuggestionBoxTextChangeReason"),
    },
    AutoSuggestionBoxTextChangeReason=EnumInfo("UserInput", "ProgrammaticChange", "SuggestionChosen"),
    BitmapIcon={"ShowAsMonochrome": GETSET("bool")},
    BitmapIconSource={"ShowAsMonochrome": GETSET("bool")},
    Border={"__base__": "Microsoft.UI.Xaml.FrameworkElement"},
    BreadcrumbBar={
        "__base__": "Control",
    },
    BreadcrumbBarItem={"__base__": "ContentControl"},
    BreadcrumbBarItemClickedEventArgs={
        "Index": GET("int"),
        "Item": GET(ANY),
    },
    Button={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.ButtonBase"},
    CalendarDatePicker={
        "__base__": "Control",
        "Date": GETSET("IReference<Windows.Foundation.DateTime>"),
        "DateFormat": GETSET(STR),
        "DisplayMode": GETSET("CalendarViewDisplayMode"),
        "IsCalendarOpen": GETSET("bool"),
        "MaxDate": GETSET("Windows.Foundation.DateTime"),
        "MinDate": GETSET("Windows.Foundation.DateTime"),
        "SetDisplayDate": CALL(date="Windows.Foundation.DateTime", void=True),
    },
    CalendarDatePickerDateChangedEventArgs={
        "NewDate": GET("IReference<Windows.Foundation.DateTime>"),
        "OldDate": GET("IReference<Windows.Foundation.DateTime>"),
    },
    CalendarView={
        "__base__": "Control",
        "MaxDate": GETSET("Windows.Foundation.DateTime"),
        "MinDate": GETSET("Windows.Foundation.DateTime"),
        #"SelectedDates": GET("std::vector<DateTime>"),
        "SetDisplayDate": CALL(date="Windows.Foundation.DateTime", void=True),
    },
    #CalendarViewDayItem={"__base__": "Control"},
    #CalendarViewDayItemChangingEventArgs={},
    CalendarViewDisplayMode=EnumInfo("Month", "Year", "Decade"),
    #CalendarViewSelectedDatesChangedEventArgs={},
    #CandidateWindowBoundsChangedEventArgs={},
    Canvas={
        "GetLeft": CALL(element="Microsoft.UI.Xaml.UIElement"),
        "GetTop": CALL(element="Microsoft.UI.Xaml.UIElement"),
        "GetZIndex": CALL(element="Microsoft.UI.Xaml.UIElement"),
        "SetLeft": CALL(element="Microsoft.UI.Xaml.UIElement", length="double", void=True),
        "SetTop": CALL(element="Microsoft.UI.Xaml.UIElement", length="double", void=True),
        "SetZIndex": CALL(element="Microsoft.UI.Xaml.UIElement", value="int", void=True),
    },
    CharacterCasing=EnumInfo("Normal", "Lower", "Upper"),
    CheckBox={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.ToggleButton"},
    ChoosingGroupHeaderContainerEventArgs={
        "Group": GET(ANY),
        "GroupIndex": GET("int"),
    },
    ChoosingItemContainerEventArgs={
        "Item": GET(ANY),
        "ItemIndex": GET("int"),
    },
    CleanUpVirtualizedItemEventArgs={
        "Cancel": GETSET("bool"),
        "UIElement": GET("Microsoft.UI.Xaml.UIElement"),
        "Value": GET(ANY),
    },
    ClickMode=EnumInfo("Release", "Press", "Hover"),
    ColorChangedEventArgs={
        "NewColor": GET("Windows.Foundation.Color"),
        "OldColor": GET("Windows.Foundation.Color"),
    },
    ColorPicker={
        "__base__": "Control",
        "Color": GETSET("Windows.Foundation.Color"),
        "ColorSpectrumComponents": GETSET("ColorSpectrumComponents"),
        "ColorSpectrumShape": GETSET("ColorSpectrumShape"),
        "PreviousColor": GETSET("Windows.Foundation.Color"),
    },
    ColorSpectrumComponents=EnumInfo("HueValue", "ValueHue", "HueSaturation", "SaturationHue", "SaturationValue", "ValueSaturation"),
    ColorSpectrumShape=EnumInfo("Box", "Ring"),
    #ColumnDefinition={"ActualWidth": GET("double")},
    #ColumnDefinitionCollection={},
    ComboBox={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.Selector",
        "Text": GETSET(STR),
    },
    ComboBoxItem={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.SelectorItem"},
    ComboBoxTextSubmittedEventArgs={
        "Handled": GETSET("bool"),
        "Text": GET(STR),
    },
    CommandBar={},
    CommandBarFlyout={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.FlyoutBase"},
    #CommandBarOverflowPresenter={},
    ContainerContentChangingEventArgs={
        "Handled": GETSET("bool"),
        "InRecycleQueue": GET("bool"),
        "Item": GET(ANY),
        "ItemContainer": GET("Microsoft.UI.Xaml.UIElement"),
        "ItemIndex": GET("int"),
        "Phase": GET("uint32_t"),
    },
    ContentControl={
        "__base__": "Control",
        "Content": GETSET(ANY),
    },
    ContentDialog={
        "__base__": "ContentControl",
        "CloseButtonText": GETSET(STR),
        "DefaultButton": GETSET("ContentDialogButton"),
        "IsPrimaryButtonEnabled": GETSET("bool"),
        "IsSecondaryButtonEnabled": GETSET("bool"),
        "PrimaryButtonText": GETSET(STR),
        "SecondaryButtonText": GETSET(STR),
        "Title": GETSET(ANY),
        "Hide": CALL(void=True),
        "ShowAsync": CALL(),
    },
    ContentDialogButton=EnumInfo("None", "Primary", "Secondary", "Close"),
    ContentDialogButtonClickDeferral={"Complete": CALL(void=True)},
    ContentDialogButtonClickEventArgs={"Cancel": GETSET("bool"), "GetDeferral": CALL()},
    ContentDialogClosedEventArgs={"Result": GET("ContentDialogResult")},
    ContentDialogClosingDeferral={"Complete": CALL(void=True)},
    ContentDialogClosingEventArgs={
        "Cancel": GETSET("bool"),
        "Result": GET("ContentDialogResult"),
        "GetDeferral": CALL(),
    },
    ContentDialogOpenedEventArgs={},
    ContentDialogResult=EnumInfo("None", "Primary", "Secondary"),
    ContentDialogResult_Op=AsyncOpInfo("ContentDialogResult"),
    ContentPresenter={"__base__": "Microsoft.UI.Xaml.FrameworkElement", "Content": GETSET(ANY)},
    ContextMenuEventArgs={"CursorLeft": GET("double"), "CursorTop": GET("double"), "Handled": GETSET("bool")},
    Control={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
        "IsEnabled": GETSET("bool"),
        "FocusDisengaged": XEVENT("FocusDisengagedEventArgs"),
        "FocusEngaged": XEVENT("FocusEngagedEventArgs"),
        "IsEnabledChanged": XEVENT("Microsoft.UI.Xaml.DependencyPropertyChangedEventArgs"),
    },
    #ControlTemplate={},
    #CoreWebView2InitializedEventArgs={},
    #DataTemplateSelector={},
    DatePickedEventArgs={
        "NewDate": GET("Windows.Foundation.DateTime"),
        "OldDate": GET("Windows.Foundation.DateTime"),
    },
    DatePicker={
        "__base__": "Control",
        "Date": GETSET("Windows.Foundation.DateTime"),
        "MaxYear": GETSET("Windows.Foundation.DateTime"),
        "MinYear": GETSET("Windows.Foundation.DateTime"),
    },
    DatePickerFlyout={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.PickerFlyoutBase"},
    #DatePickerFlyoutItem={},
    #DatePickerFlyoutPresenter={"__base__": "Control"},
    DatePickerSelectedValueChangedEventArgs={
        "NewDate": GET("Windows.Foundation.DateTime"),
        "OldDate": GET("Windows.Foundation.DateTime"),
    },
    DatePickerValueChangedEventArgs={
        "NewDate": GET("Windows.Foundation.DateTime"),
        "OldDate": GET("Windows.Foundation.DateTime"),
    },
    DragItemsCompletedEventArgs={
        "DropResult": GET("Windows.ApplicationModel.DataTransfer.DataPackageOperation"),
        "Items": GET("Windows.Foundation.Collections.IVector<IInspectable>"),
    },
    DragItemsStartingEventArgs={
        "Cancel": GETSET("bool"),
        "Data": GET("Windows.ApplicationModel.DataTransfer.DataPackage"),
    },
    DropDownButton={"__base__": "Button"},
    DynamicOverflowItemsChangingEventArgs={},
    Expander={"__base__": "ContentControl", "IsExpanded": GETSET("bool")},
    ExpanderCollapsedEventArgs={},
    ExpanderExpandingEventArgs={},
    #ExpanderTemplateSettings={},
    FlipView={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.Selector"},
    FlipViewItem={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.SelectorItem"},
    Flyout={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.FlyoutBase"},
    FlyoutPresenter={"__base__": "ContentControl"},
    FocusDisengagedEventArgs={},
    FocusEngagedEventArgs={},
    FontIcon={"__base__": "IconElement", "Glyph": GETSET(STR)},
    FontIconSource={"__base__": "IconSource", "Glyph": GETSET(STR)},
    Frame={
        "__base__": "ContentControl",
        "CanGoBack": GET("bool"),
        "CanGoForward": GET("bool"),
        "GetNavigationState": CALL(),
        "GoBack": CALL(void="unchecked"),
        "GoForward": CALL(void=True),
        "Navigate": CALL(sourcePageType="Windows.UI.Xaml.Interop.TypeName", parameter=ANY),
        "SetNavigationState": CALL(navigationState=STR, suppressNavigate="bool", void="unchecked"),
    },
    Grid={"__base__": "Panel"},
    GridView={"__base__": "ListViewBase"},
    GridViewHeaderItem={"__base__": "ListViewBaseHeaderItem"},
    GridViewItem={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.SelectorItem"},
    GroupItem={"__base__": "ContentControl"},
    #GroupStyle={},
    #GroupStyleSelector={},
    HasValidationErrorsChangedEventArgs={"NewValue": GET("bool")},
    Hub={
        "__base__": "Control",
        "ScrollToSection": CALL(section="HubSection", void=True),
    },
    HubSection={"__base__": "Control"},
    #HubSectionCollection={},
    HubSectionHeaderClickEventArgs={"Section": GET("HubSection")},
    HyperlinkButton={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.ButtonBase",
        "NavigateUri": GETSET("Windows.Foundation.Uri"),
    },
    IconElement={"__base__": "Microsoft.UI.Xaml.FrameworkElement"},
    IconSource={"__base__": "Microsoft.UI.Xaml.DependencyObject"},
    IconSourceElement={"__base__": "IconElement"},
    Image={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
        "GetAsCastingSource": CALL(),
        "ImageFailed": XEVENT("Microsoft.UI.Xaml.ExceptionRoutedEventArgs"),
        "ImageOpened": XEVENT(),
    },
    ImageIcon={"__base__": "IconElement"},
    ImageIconSource={"__base__": "IconSource"},
    InfoBadge={
        "__base__": "Control",
        "Value": GETSET("int"),
    },
    #InfoBadgeTemplateSettings={},
    InfoBar={
        "__base__": "Control",
        "Content": GETSET(ANY),
        "Message": GETSET(STR),
        "IsOpen": GETSET("bool"),
        "Severity": GETSET("InfoBarSeverity"),
        "Title": GETSET(STR),
        "CloseButtonClick": XEVENT(ANY),
        "Closed": XEVENT("InfoBarClosedEventArgs"),
        "Closing": XEVENT("InfoBarClosingEventArgs"),
    },
    InfoBarClosedEventArgs={"Reason": GET("InfoBarCloseReason")},
    InfoBarCloseReason=EnumInfo("CloseButton", "Programmatic"),
    InfoBarClosingEventArgs={"Cancel": GETSET("bool"), "Reason": GET("InfoBarCloseReason")},
    InfoBarSeverity=EnumInfo("Informational", "Success", "Warning", "Error"),
    #InfoBarTemplateSettings={},
    IsTextTrimmedChangedEventArgs={},
    ItemClickEventArgs={"ClickedItem": GET(ANY)},
    ItemCollection={},
    #ItemCollectionTransition={},
    #ItemCollectionTransitionCompletedEventArgs={},
    #ItemCollectionTransitionProgress={},
    #ItemCollectionTransitionProvider={},
    ItemContainer={
        "__base__": "Control",
        "Child": GETSET("Microsoft.UI.Xaml.UIElement"),
        "IsSelected": GETSET("bool"),
    },
    #ItemContainerGenerator={},
    ItemsControl={
        "__base__": "Control",
        "ContainerFromIndex": CALL(index="int"),
        "ContainerFromItem": CALL(item=ANY),
        "IndexFromContainer": CALL(container="Microsoft.UI.Xaml.DependencyObject"),
        "ItemFromContainer": CALL(container="Microsoft.UI.Xaml.DependencyObject"),
    },
    #ItemsPanelTemplate={},
    ItemsPickedEventArgs={
        "AddedItems": GET(LIST_OBJ),
        "RemovedItems": GET(LIST_OBJ),
    },
    #ItemsPresenter={},
    #ItemsRepeater={},
    #ItemsRepeaterElementClearingEventArgs={},
    #ItemsRepeaterElementIndexChangedEventArgs={},
    #ItemsRepeaterElementPreparedEventArgs={},
    #ItemsRepeaterScrollHost={},
    ItemsSourceView={},
    ItemsStackPanel={"__base__": "Panel"},
    ItemsView={
        "__base__": "Control",
        "CurrentItemIndex": GET("int"),
        "SelectedItem": GET(ANY),
        "SelectedItems": GET(LIST_OBJ),
        "Deselect": CALL(itemIndex="int", void=True),
        "DeselectAll": CALL(void=True),
        "InvertSelection": CALL(void=True),
        "IsSelected": CALL(itemIndex="int"),
        "Select": CALL(itemIndex="int", void=True),
        "SelectAll": CALL(void=True),
        "StartBringItemIntoView": CALL(itemIndex="int", options="Microsoft.UI.Xaml.BringIntoViewOptions", void=True),
        "ItemInvoked": XEVENT("ItemsViewItemInvokedEventArgs"),
        "SelectionChanged": XEVENT("ItemsViewSelectionChangedEventArgs"),
    },
    ItemsViewItemInvokedEventArgs={"InvokedItem": GET(ANY)},
    ItemsViewSelectionChangedEventArgs={},
    ItemsWrapGrid={"__base__": "Panel"},
    #Layout={"__base__": "Windows.UI.Xaml.DependencyObject"},
    #LayoutContext={},
    #LinedFlowLayout={},
    #LinedFlowLayoutItemCollectionTransitionProvider={},
    #LinedFlowLayoutItemsInfoRequestedEventArgs={},
    ListBox={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.Selector",
        "SelectedItems": GET(LIST_OBJ),
        "ScrollIntoView": CALL(item=ANY, void=True),
        "SelectAll": CALL(void=True),
    },
    ListBoxItem={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.SelectorItem"},
    ListPickerFlyout={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.PickerFlyoutBase"},
    #ListPickerFlyoutPresenter={"__base__": "Control"},
    ItemIndexRange={
        "__namespace__": "Microsoft.UI.Xaml.Data",
        "__init__": CALL(firstIndex="int", length="uint32_t"),
        "FirstIndex": GET("int"),
        "LastIndex": GET("int"),
        "Length": GET("uint32_t"),
    },
    ListView={"__base__": "ListViewBase"},
    ListViewBase={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.Selector",
        "SelectedItems": LIST_OBJ,
        "SelectedRanges": "Windows.Foundation.Collections.IVector<Microsoft.UI.Xaml.Data.ItemIndexRange>",
        "DeselectRange": CALL(itemIndexRange="Microsoft.UI.Xaml.Data.ItemIndexRange", void=True),
        "SelectAll": CALL(void=True),
        "SelectRange": CALL(itemIndexRange="Microsoft.UI.Xaml.Data.ItemIndexRange", void=True),
        "DragItemsCompleted": XEVENT("DragItemsCompletedEventArgs"),
        "DragItemsStarting": XEVENT("DragItemsStartingEventArgs"),
        "ItemClick": XEVENT("ItemClickEventArgs"),
    },
    ListViewBaseHeaderItem={"__base__": "ContentControl"},
    ListViewHeaderItem={"__base__": "ListViewBaseHeaderItem"},
    ListViewItem={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.SelectorItem"},
    ListViewPersistenceHelper={},
    MediaPlaybackState=EnumInfo("None", "Opening", "Buffering", "Playing", "Paused", namespace="Windows.Media.Playback"),
    MediaPlaybackSession={
        "__namespace__": "Windows.Media.Playback",
        "NaturalDuration": GET("TimeSpan"),
        "PlaybackState": GET("Windows.Media.Playback.MediaPlaybackState"),
        "Position": GET("TimeSpan"),  # technically GETSET but cannot cast yet
    },
    MediaPlayer={
        "__namespace__": "Windows.Media.Playback",
        "PlaybackSession": GET("MediaPlaybackSession"),
        "Pause": CALL(void=True),
        "Play": CALL(void=True),
        "StepBackwardOneFrame": CALL(void=True),
        "StepForwardOneFrame": CALL(void=True),
    },
    MediaPlayerElement={
        "__base__": "Control",
        "IsFullWindow": GETSET("bool"),
        "MediaPlayer": GET("MediaPlayer"),
    },
    MediaPlayerPresenter={
        "IsFullWindow": GETSET("bool"),
        "MediaPlayer": GET("MediaPlayer"),
    },
    MediaTransportControls={
        "__base__": "Control",
        "Hide": CALL(void=True),
        "Show": CALL(void=True),
        "ThumbnailRequested": XEVENT("Microsoft.UI.Xaml.Media.MediaTransportControlsThumbnailRequestedEventArgs"),
    },
    MediaTransportControlsThumbnailRequestedEventArgs={
        "__namespace__": "Microsoft.UI.Xaml.Media",
        "GetDeferral": CALL(),
        #"SetThumbnailImage": CALL(source="Windows.Storage.Streams.IInputStream"),
    },
    MediaTransportControlsHelper={},
    MenuBar={
        "__base__": "Control",
    },
    MenuBarItem={
        "__base__": "Control",
        "Title": GETSET(STR),
    },
    #MenuBarItemFlyout={},
    MenuFlyout={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.FlyoutBase",
        "ShowAt": CALL(
            targetElement="Microsoft.UI.Xaml.UIElement",
            point="Windows.Foundation.Point",
            void="unchecked",
        ),
    },
    MenuFlyoutItem={
        "__base__": "MenuFlyoutItemBase",
        "Text": GETSET(STR),
        "Click": XEVENT(),
    },
    MenuFlyoutItemBase={"__base__": "Control"},
    #MenuFlyoutPresenter={},
    #MenuFlyoutSeparator={},
    MenuFlyoutSubItem={
        "__base__": "MenuFlyoutItemBase",
        "Text": GETSET(STR),
    },
    NavigationView={
        "__base__": "ContentControl",
        "SelectedItem": GETSET(ANY),
        "Collapse": CALL(item="NavigationViewItem", void=True),
        "Expand": CALL(item="NavigationViewItem", void=True),
        "BackRequested": XEVENT("NavigationViewBackRequestedEventArgs"),
        "Collapsed": XEVENT("NavigationViewItemCollapsedEventArgs"),
        "DisplayModeChanged": XEVENT("NavigationViewDisplayModeChangedEventArgs"),
        "Expanding": XEVENT("NavigationViewItemExpandingEventArgs"),
        "ItemInvoked": XEVENT("NavigationViewItemInvokedEventArgs"),
        "PaneClosed": XEVENT(ANY),
        "PaneClosing": XEVENT("NavigationViewPaneClosingEventArgs"),
        "PaneOpened": XEVENT(ANY),
        "PaneOpening": XEVENT(ANY),
        "SelectionChanged": XEVENT("NavigationViewSelectionChangedEventArgs"),
    },
    NavigationViewBackRequestedEventArgs={},
    NavigationViewDisplayMode=EnumInfo("Minimal", "Compact", "Expanded"),
    NavigationViewDisplayModeChangedEventArgs={"DisplayMode": GET("NavigationViewDisplayMode")},
    NavigationViewItem={
        "__base__": "NavigationViewItemBase",
        "IsExpanded": GETSET("bool"),
    },
    NavigationViewItemBase={"__base__": "ContentControl"},
    NavigationViewItemCollapsedEventArgs={
        "CollapsedItem": GET(ANY),
        "CollapsedItemContainer": GET(ANY),
    },
    NavigationViewItemExpandingEventArgs={
        "ExpandingItem": GET(ANY),
        "ExpandingItemContainer": GET(ANY),
    },
    NavigationViewItemHeader={},
    NavigationViewItemInvokedEventArgs={
        "InvokedItem": GET(ANY),
        "InvokedItemContainer": GET(ANY),
        "IsSettingsInvoked": GET("bool"),
    },
    #NavigationViewItemSeparator={},
    NavigationViewPaneClosingEventArgs={"Cancel": GETSET("bool")},
    NavigationViewSelectionChangedEventArgs={
        "IsSettingsSelected": GET("bool"),
        "SelectedItem": GET(ANY),
        "SelectedItemContainer": GET(ANY),
    },
    #NavigationViewTemplateSettings={},
    #NonVirtualizingLayout={},
    #NonVirtualizingLayoutContext={},
    NumberBox={
        "__base__": "Control",
        "Text": GETSET(STR),
        "Value": GETSET("double"),
        "ValueChanged": XEVENT("NumberBoxValueChangedEventArgs"),
    },
    NumberBoxValueChangedEventArgs={"OldValue": GET("double"), "NewValue": GET("double")},
    Page={"__base__": "Control"},
    Panel={"__base__": "Microsoft.UI.Xaml.FrameworkElement"},
    ParallaxView={"__base__": "Microsoft.UI.Xaml.FrameworkElement"},
    PasswordBox={
        "__base__": "Control",
        "Password": GETSET(STR),
        "PasteFromClipboard": CALL(void=True),
        "SelectAll": CALL(void=True),
        "PasswordChanged": XEVENT(),
        "PasswordChanging": XEVENT("PasswordBoxPasswordChangingEventArgs"),
        "Paste": XEVENT("TextControlPasteEventArgs"),
    },
    PasswordBoxPasswordChangingEventArgs={"IsContentChanging": GET("bool")},
    PathIcon={"__base__": "IconElement"},
    PathIconSource={"__base__": "IconSource"},
    PersonPicture={
        "__base__": "Control",
        "BadgeText": GETSET(STR),
        #"Contact": GETSET("Windows.ApplicationModel.Contacts.Contact"),
        "Initials": GETSET(STR),
    },
    #PersonPictureTemplateSettings={},
    PickerConfirmedEventArgs={},
    PipsPager={
        "__base__": "Control",
        "SelectedPageIndex": GETSET("int"),
    },
    PipsPagerSelectedIndexChangedEventArgs={},
    #PipsPagerTemplateSettings={},
    Pivot={
        "__base__": "ItemsControl",
        "SelectedIndex": GETSET("int"),
        "SelectedItem": GETSET(ANY),
        "PivotItemLoaded": XEVENT("PivotItemEventArgs"),
        "PivotItemLoading": XEVENT("PivotItemEventArgs"),
        "PivotItemUnloaded": XEVENT("PivotItemEventArgs"),
        "PivotItemUnloading": XEVENT("PivotItemEventArgs"),
        "SelectionChanged": XEVENT("SelectionChangedEventArgs"),
    },
    PivotItem={"__base__": "ContentControl"},
    PivotItemEventArgs={"Item": GETSET(ANY)},
    ProgressBar={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.RangeBase",
        "IsIndeterminate": GETSET("bool"),
        "ShowError": GETSET("bool"),
        "ShowPaused": GETSET("bool"),
    },
    #ProgressBarTemplateSettings={},
    ProgressRing={
        "__base__": "Control",
        "IsActive": GETSET("bool"),
        "IsIndeterminate": GETSET("bool"),
        "Maximum": GETSET("double"),
        "Minimum": GETSET("double"),
        "Value": GETSET("double"),
    },
    #ProgressRingTemplateSettings={},
    RadioButton={
        "__base__": "Microsoft.UI.Xaml.Controls.Primitives.ToggleButton",
        "GroupName": GETSET(STR),
    },
    RadioButtons={
        "__base__": "Control",
        "SelectedIndex": GETSET("int"),
        "SelectedItem": GETSET(ANY),
        "ContainerFromIndex": CALL(index="int"),
        "SelectionChanged": XEVENT("SelectionChangedEventArgs"),
    },
    RadioMenuFlyoutItem={
        "__base__": "MenuFlyoutItem",
        "IsChecked": GETSET("bool"),
    },
    RatingControl={
        "__base__": "Control",
        "MaxRating": GETSET("double"),
        "Value": GETSET("double"),
        "ValueChanged": XEVENT(ANY),
    },
    #RatingItemFontInfo={},
    #RatingItemImageInfo={},
    #RatingItemInfo={},
    RefreshContainer={"__base__": "ContentControl"},
    RefreshInteractionRatioChangedEventArgs={},
    RefreshRequestedEventArgs={"GetDeferral": CALL()},
    RefreshStateChangedEventArgs={
        "NewState": GET("RefreshVisualizerState"),
        "OldState": GET("RefreshVisualizerState"),
    },
    RefreshVisualizer={
        "__base__": "Control",
    },
    RefreshVisualizerState=EnumInfo("Idle", "Peeking", "Interacting", "Pending", "Refreshing"),
    RelativePanel={"__base__": "Panel"},
    #RevealListViewItemPresenter={},
    RichEditBox={
        "__base__": "Control",
        # TODO: Implement TextDocument
        "TextDocument": GET("Microsoft.UI.Text.RichEditTextDocument"),

    },
    RichEditBoxSelectionChangingEventArgs={
        "Cancel": GETSET("bool"),
        "SelectionLength": GET("int"),
        "SelectionStart": GET("int"),
    },
    RichEditBoxTextChangingEventArgs={"IsContentChanging": GET("bool")},
    RichTextBlock={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
        "CopySelectionToClipboard": CALL(void=True),
        # TODO: Implement TextPointer
        "Select": CALL(start="Microsoft.UI.Xaml.Documents.TextPointer", end="Microsoft.UI.Xaml.Documents.TextPointer", void=True),
        "SelectAll": CALL(void=True),
    },
    RichTextBlockOverflow={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
    },
    #RowDefinition={},
    #RowDefinitionCollection={},
    #ScrollContentPresenter={},
    #ScrollingAnchorRequestedEventArgs={},
    #ScrollingBringingIntoViewEventArgs={},
    #ScrollingScrollAnimationStartingEventArgs={},
    #ScrollingScrollCompletedEventArgs={},
    #ScrollingScrollOptions={},
    #ScrollingZoomAnimationStartingEventArgs={},
    #ScrollingZoomCompletedEventArgs={},
    #ScrollingZoomOptions={},
    #ScrollView={"__base__": "Control"},
    #ScrollViewer={"__base__": "ContentControl"},
    #ScrollViewerView={},
    #ScrollViewerViewChangedEventArgs={},
    #ScrollViewerViewChangingEventArgs={},
    #SectionsInViewChangedEventArgs={},
    SelectionChangedEventArgs={
        "AddedItems": GET(LIST_OBJ),
        "RemovedItems": GET(LIST_OBJ),
    },
    #SemanticZoom={"__base__": "Control"},
    #SemanticZoomLocation={},
    #SemanticZoomViewChangedEventArgs={},
    Slider={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.RangeBase"},
    SplitButton={"__base__": "ContentControl"},
    SplitButtonClickEventArgs={},
    SplitView={
        "__base__": "Control",
        "IsPaneOpen": GETSET("bool"),
    },
    SplitViewPaneClosingEventArgs={},
    #StackLayout={},
    StackPanel={"__base__": "Panel"},
    #StyleSelector={},
    SwapChainPanel={"__base__": "Grid"},
    SwipeControl={"__base__": "ContentControl", "Close": CALL(void=True)},
    SwipeItem={"__base__": "Windows.UI.Xaml.DependencyObject", "Text": GETSET(STR)},
    SwipeItemInvokedEventArgs={"SwipeControl": GET("SwipeControl")},
    SwipeItems={"__base__": "Windows.UI.Xaml.DependencyObject"},
    SymbolIcon={"__base__": "IconElement"},
    SymbolIconSource={"__base__": "IconSource"},
    TabView={
        "__base__": "Control",
        "SelectedIndex": GETSET("int"),
        "SelectedItem": GETSET(ANY),
        "ContainerFromIndex": CALL(index="int"),
        "ContainerFromItem": CALL(item=ANY),
    },
    TabViewItem={"__base__": "ListViewItem", "IsClosable": GETSET("bool")},
    #TabViewItemTemplateSettings={},
    TabViewTabCloseRequestedEventArgs={"Item": GET(ANY), "Tab": GET("TabViewItem")},
    TabViewTabDragCompletedEventArgs={
        "DropResult": "Windows.ApplicationModel.DataTransfer.DataPackageOperation",
        "Item": GET(ANY),
        "Tab": GET("TabViewItem"),
    },
    TabViewTabDragStartingEventArgs={
        "Cancel": GETSET("bool"),
        "DropResult": "Windows.ApplicationModel.DataTransfer.DataPackageOperation",
        "Item": GET(ANY),
        "Tab": GET("TabViewItem"),
    },
    TabViewTabDroppedOutsideEventArgs={
        "Item": GET(ANY),
        "Tab": GET("TabViewItem"),
    },
    TeachingTip={
        "__base__": "ContentControl",
        "IsOpen": GETSET("bool"),
    },
    TeachingTipClosedEventArgs={"Reason": GET("TeachingTipCloseReason")},
    TeachingTipCloseReason=EnumInfo("CloseButton", "LightDismiss", "Programmatic"),
    TeachingTipClosingEventArgs={
        "Cancel": GETSET("bool"),
        "Reason": GET("TeachingTipCloseReason"),
        "GetDeferral": CALL(),
    },
    #TeachingTipTemplateSettings={},
    TextBlock={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
        "Text": GETSET(STR),
        "CopySelectionToClipboard": CALL(void=True),
        #"Select": CALL(start="TextPointer", end="TextPointer", void=True),
        "SelectAll": CALL(void=True),
    },
    TextBox={
        "__base__": "Control",
        "SelectionLength": GETSET("int"),
        "SelectionStart": GETSET("int"),
        "Text": GETSET(STR),
        "ClearUndoRedoHistory": CALL(void=True),
        "CopySelectionToClipboard": CALL(void=True),
        "CutSelectionToClipboard": CALL(void=True),
        "PasteFromClipboard": CALL(void=True),
        "Redo": CALL(void=True),
        "Select": CALL(start="int", length="int", void=True),
        "SelectAll": CALL(void=True),
        "Undo": CALL(void=True),
    },
    TextBoxBeforeTextChangingEventArgs={"Cancel": GETSET("bool"), "NewText": GET(STR)},
    TextBoxSelectionChangingEventArgs={
        "Cancel": GETSET("bool"),
        "SelectionLength": GET("int"),
        "SelectionStart": GET("int"),
    },
    TextBoxTextChangingEventArgs={"IsContentChanging": GET("bool")},
    TextChangedEventArgs={},
    #TextCommandBarFlyout={},
    TextCompositionChangedEventArgs={"Length": GET("int"), "StartIndex": GET("int")},
    TextCompositionEndedEventArgs={"Length": GET("int"), "StartIndex": GET("int")},
    TextCompositionStartedEventArgs={"Length": GET("int"), "StartIndex": GET("int")},
    TextControlCopyingToClipboardEventArgs={"Handled": GETSET("bool")},
    TextControlCuttingToClipboardEventArgs={"Handled": GETSET("bool")},
    TextControlPasteEventArgs={"Handled": GETSET("bool")},
    TimePickedEventArgs={"NewTime": GET("TimeSpan"), "OldTime": GET("TimeSpan")},
    TimePicker={
        "__base__": "Control",
        "SelectedTime": GETSET("TimeSpan"),
        "Time": GETSET("TimeSpan"),
    },
    TimePickerFlyout={"__base__": "Microsoft.UI.Xaml.Controls.Primitives.PickerFlyoutBase"},
    #TimePickerFlyoutPresenter={"__base__": "Control"},
    TimePickerSelectedValueChangedEventArgs={"NewTime": GET("TimeSpan"), "OldTime": GET("TimeSpan")},
    TimePickerValueChangedEventArgs={"NewTime": GET("TimeSpan"), "OldTime": GET("TimeSpan")},
    #ToggleMenuFlyoutItem={},
    ToggleSplitButton={"__base__": "SplitButton", "IsChecked": GETSET("bool")},
    ToggleSplitButtonIsCheckedChangedEventArgs={},
    ToggleSwitch={"__base__": "Control", "IsOn": GETSET("bool")},
    ToolTip={"__base__": "ContentControl", "IsOpen": GETSET("bool")},
    ToolTipService={
        "GetToolTip": CALL(element="Microsoft.UI.Xaml.DependencyObject"),
        "SetToolTip": CALL(element="Microsoft.UI.Xaml.DependencyObject", value=ANY, void=True),
    },
    TreeView={
        "__base__": "Control",
        "SelectedItem": GETSET(ANY),
        "SelectedItems": GET(LIST_OBJ),
        "SelectedNode": GETSET("TreeViewNode"),
        "SelectedNodes": GET("Windows.Foundation.Collections.IVector<Microsoft.UI.Xaml.Controls.TreeViewNode>"),
        "Collapse": CALL(value="TreeViewNode", void=True),
        "ContainerFromItem": CALL(item=ANY),
        "ContainerFromNode": CALL(node="TreeViewNode"),
        "Expand": CALL(value="TreeViewNode", void=True),
        "ItemFromContainer": CALL(container="Microsoft.UI.Xaml.DependencyObject"),
        "NodeFromContainer": CALL(container="Microsoft.UI.Xaml.DependencyObject"),
        "SelectAll": CALL(void=True),
    },
    TreeViewCollapsedEventArgs={"Item": GET(ANY), "Node": GET("TreeViewNode")},
    TreeViewDragItemsCompletedEventArgs={},
    TreeViewDragItemsStartingEventArgs={},
    TreeViewExpandingEventArgs={"Item": GET(ANY), "Node": GET("TreeViewNode")},
    TreeViewItem={"__base__": "ListViewItem", "IsExpanded": GETSET("bool")},
    TreeViewItemInvokedEventArgs={"Handled": GETSET("bool"), "InvokedItem": GET(ANY)},
    #TreeViewItemTemplateSettings={},
    TreeViewList={"__base__": "ListView"},
    TreeViewNode={
        "Depth": GET("int"),
        "HasChildren": GET("bool"),
        "IsExpanded": GETSET("bool"),
    },
    TreeViewSelectionChangedEventArgs={
        "AddedItems": GET(LIST_OBJ),
        "RemovedItems": GET(LIST_OBJ),
    },
    TwoPaneView={"__base__": "Control"},
    #UIElementCollection={},
    #UniformGridLayout={},
    VariableSizedWrapGrid={"__base__": "Panel"},
    Viewbox={"__base__": "Microsoft.UI.Xaml.FrameworkElement"},
    #VirtualizingLayout={},
    #VirtualizingLayoutContext={},
    VirtualizingPanel={"__base__": "Panel"},
    VirtualizingStackPanel={},
    WebView2={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
        "CanGoBack": GET("bool"),
        "CanGoForward": GET("bool"),
        "Source": GETSET("Windows.Foundation.Uri"),
        "ExecuteScriptAsync": CALL(javascriptCode=STR),
        "GoBack": CALL(void=True),
        "GoForward": CALL(void=True),
        "NavigateToString": CALL(htmlContent=STR, void=True),
        "Reload": CALL(void=True),
    },
    WrapGrid={"__base__": "VirtualizingPanel"},
    #XamlControlsResources={},
)

collect(
    "Microsoft.UI.Xaml.Controls.Primitives",
    ButtonBase={
        "__base__": "Microsoft.UI.Xaml.Controls.ContentControl",
        "IsPointerOver": GET("bool"),
        "IsPressed": GET("bool"),
        "Click": XEVENT(),
    },
    DragCompletedEventArgs={
        "Canceled": GET("bool"),
        "HorizontalChange": GET("double"),
        "VerticalChange": GET("double"),
    },
    DragDeltaEventArgs={
        "HorizontalChange": GET("double"),
        "VerticalChange": GET("double"),
    },
    DragStartedEventArgs={
        "HorizontalOffset": GET("double"),
        "VerticalOffset": GET("double"),
    },
    FlyoutBase={
        "__base__": "Microsoft.UI.Xaml.DependencyObject",
        "ElementSoundMode": GETSET("Microsoft.UI.Xaml.ElementSoundMode"),
        "IsOpen": GET("bool"),
        "ShowMode": GETSET("FlyoutShowMode"),
        "Hide": CALL(void=True),
        "ShowAt": CALL(placementTarget="Microsoft.UI.Xaml.DependencyObject", showOptions="Microsoft.UI.Xaml.Controls.Primitives.FlyoutShowOptions", void="unchecked"),
        "Closed": XEVENT(ANY),
        "Closing": XEVENT("FlyoutBaseClosingEventArgs"),
        "Opened": XEVENT(ANY),
        "Opening": XEVENT(ANY),
    },
    FlyoutBaseClosingEventArgs={"Cancel": GETSET("bool")},
    FlyoutPlacementMode=EnumInfo("Auto", "Bottom", "BottomEdgeAlignedLeft", "BottomEdgeAlignedRight", "Full", "Left", "LeftEdgeAlignedBottom", "LeftEdgeAlignedTop", "Right", "RightEdgeAlignedBottom", "RightEdgeAlignedTop", "Top", "TopEdgeAlignedLeft", "TopEdgeAlignedRight"),
    FlyoutShowMode=EnumInfo("Auto", "Standard", "Transient", "TransientWithDismissOnPointerMoveAway"),
    FlyoutShowOptions={
        "__init__": CALL(),
        "Placement": GETSET("FlyoutPlacementMode"),
        "Position": GETSET("IReference<Windows.Foundation.Point>"),
        "ShowMode": GETSET("FlyoutShowMode"),
    },
    LoopingSelector={
        "__base__": "Microsoft.UI.Xaml.Controls.Control",
        "ItemHeight": GETSET("int"),
        "ItemWidth": GETSET("int"),
        "SelectedIndex": GETSET("int"),
        "SelectedItem": GETSET(ANY),
        "ShouldLoop": GETSET("bool"),
        "SelectionChanged": XEVENT("Microsoft.UI.Xaml.Controls.SelectionChangedEventArgs"),
    },
    RangeBase={
        "__base__": "Microsoft.UI.Xaml.Controls.Control",
        "LargeChange": GETSET("double"),
        "Minimum": GETSET("double"),
        "Maximum": GETSET("double"),
        "SmallChange": GETSET("double"),
        "Value": GETSET("double"),
        "ValueChanged": XEVENT("RangeBaseValueChangedEventArgs"),
    },
    ScrollBar={
        "__base__": "RangeBase",
        "Scroll": XEVENT("ScrollEventArgs"),
    },
    ScrollEventArgs={
        "NewValue": GET("double"),
        "ScrollEventType": GET("ScrollEventType"),
    },
    ScrollEventType=EnumInfo("EndScroll", "First", "LargeDecrement", "LargeIncrement", "Last", "SmallDecrement", "SmallIncrement", "ThumbPosition", "ThumbTrack"),
    Selector={
        "__base__": "Microsoft.UI.Xaml.Controls.ItemsControl",
        "SelectedIndex": GETSET("int"),
        "SelectedItem": GETSET(ANY),
        "SelectedValue": GETSET(ANY),
        "SelectionChanged": XEVENT("Microsoft.UI.Xaml.Controls.SelectionChangedEventArgs"),
    },
    SelectorItem={
        "__base__": "Microsoft.UI.Xaml.Controls.ContentControl",
        "IsSelected": GETSET("bool"),
    },
    Thumb={
        "__base__": "Microsoft.UI.Xaml.Controls.Control",
        "IsDragging": GET("bool"),
        "CancelDrag": CALL(void=True),
        "DragCompleted": XEVENT("DragCompletedEventArgs"),
        "DragDelta": XEVENT("DragDeltaEventArgs"),
        "DragStarted": XEVENT("DragStartedEventArgs"),
    },
    ToggleButton={
        "__base__": "ButtonBase",
        "IsChecked": GETSET("Windows.IReference<bool>"),
        "IsThreeState": GETSET("bool"),
        "Checked": XEVENT(),
        "Indeterminate": XEVENT(),
        "Unchecked": XEVENT(),
    },
)

collect(
    "Microsoft.UI.Xaml.Input",
    PointerDeviceType=EnumInfo("Touch", "Pen", "Mouse", "Touchpad", namespace="Microsoft.UI.Input"),
    PointerPoint={
        "__namespace__": "Microsoft.UI.Input",
        "FrameId": GET("uint32_t"),
        "IsInContact": GET("bool"),
        "PointerDeviceType": GET("PointerDeviceType"),
        "PointerId": GET("uint32_t"),
        "Position": GET("Windows.Foundation.Point"),
        "Properties": GET("PointerPointProperties"),
        "Timestamp": GET("uint64_t"),
    },
    PointerPointProperties={"__namespace__": "Microsoft.UI.Input"},
    VirtualKeyModifiers=EnumInfo("None", "Control", "Menu", "Shift", "Windows", namespace="Windows.System"),

    DoubleTappedRoutedEventArgs={
        "__base__": "Microsoft.UI.Xaml.RoutedEventArgs",
        "Handled": GETSET("bool"),
        "PointerDeviceType": GET("Microsoft.UI.Input.PointerDeviceType"),
        "GetPosition": CALL(relativeTo="Microsoft.UI.Xaml.UIElement"),
    },
    Pointer={
        "IsInContact": GET("bool"),
        "IsInRange": GET("bool"),
        "PointerDeviceType": GET("Microsoft.UI.PointerDeviceType"),
        "PointerId": GET("uint32_t"),
    },
    PointerRoutedEventArgs={
        "__base__": "Microsoft.UI.Xaml.RoutedEventArgs",
        "Handled": GETSET("bool"),
        "IsGenerated": GET("bool"),
        "KeyModifiers": GET("Windows.System.VirtualKeyModifiers"),
        "Pointer": GET("Pointer"),
        "GetCurrentPoint": CALL(relativeTo="Microsoft.UI.Xaml.UIElement"),
    },
    RightTappedRoutedEventArgs={
        "__base__": "Microsoft.UI.Xaml.RoutedEventArgs",
        "Handled": GETSET("bool"),
        "PointerDeviceType": GET("Microsoft.UI.Input.PointerDeviceType"),
        "GetPosition": CALL(relativeTo="Microsoft.UI.Xaml.UIElement"),
    },
    TappedRoutedEventArgs={
        "__base__": "Microsoft.UI.Xaml.RoutedEventArgs",
        "Handled": GETSET("bool"),
        "PointerDeviceType": GET("Microsoft.UI.Input.PointerDeviceType"),
        "GetPosition": CALL(relativeTo="Microsoft.UI.Xaml.UIElement"),
    },
)

collect(
    "Windows.UI.Xaml.Interop",
    TypeName=StructInfo(),
)


def resolve_bases(all_types):
    derived = {}
    todo = []
    for c in all_types:
        if c.kind == "runtimeclass":
            for b in c.bases:
                derived.setdefault(b, set()).add(c)
                todo.append(c)

    while todo:
        b = todo.pop(0)
        try:
            subs = derived[b.fullname]
        except KeyError:
            continue
        new = {c2 for c in subs for c2 in derived.get(c.fullname, ())}
        if new - subs:
            subs.update(new)
            todo.append(b)

    for c in all_types:
        for sub in derived.get(c.fullname, ()):
            sub.members.update(c.members)


def update_members(all_types):
    for c in all_types:
        if not isinstance(c.members, dict):
            continue
        c.members = copy.deepcopy(c.members)
        for m in c.members.values():
            if hasattr(m, "selftype"):
                m.selftype = c
            if not getattr(m, "namespace", ...):
                m.namespace = c.namespace


def maybe_write_template(template, context, dest, force=False):
    read_f = write_f = None
    if not force:
        try:
            read_f = open(dest, "rb")
        except FileNotFoundError:
            pass
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
        print("Updated", dest)



resolve_bases(ALL_TYPES)
update_members(ALL_TYPES)

MODULES = {}
for c in ALL_TYPES:
    MODULES.setdefault(c.namespace, []).append(c)


maybe_write_template(
    RENDER_ENV.get_template("winui_converters.h.in"),
    dict(all_types=ALL_TYPES),
    OUTPUT / "_winui_converters.h",
    FORCE,
)

maybe_write_template(
    RENDER_ENV.get_template("controldata.py.in"),
    dict(all_types=ALL_TYPES),
    CONTROLDATA_OUTPUT,
    FORCE,
)

for m, types in MODULES.items():
    safe_name = f"_winui_{m.replace('.', '_')}"
    CONTEXT = dict(
        namespace=m,
        module=safe_name,
        all_types=ALL_TYPES,
        module_types=types,
    )

    DEST = OUTPUT / (safe_name + ".cpp")
    maybe_write_template(
        RENDER_ENV.get_template("winui_module.cpp.in"),
        CONTEXT,
        DEST,
        FORCE,
    )

    to_write = list(types)
    next_i = 0
    while to_write:
        DEST = OUTPUT / f"{safe_name}.{next_i}.cpp"
        maybe_write_template(
            RENDER_ENV.get_template("winui_module_impl.cpp.in"),
            {**CONTEXT, "module_types": to_write[:TYPE_CHUNK_SIZE]},
            DEST,
            FORCE,
        )
        to_write[:TYPE_CHUNK_SIZE] = []
        next_i += 1
