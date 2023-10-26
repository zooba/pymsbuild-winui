import jinja2
import sys

from pathlib import Path

ROOT = Path(__file__).absolute().parent
OUTPUT = ROOT.parent / "pymsbuild_winui" / "targets" / "xaml_controls.cpp"

RENDER_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ROOT),
    trim_blocks=True,
)

# The BaseInfo and ControlInfo classes are passed into the jinja
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
        return f"{self.namespace}.{self.name}" if self.namespace else self.name

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
        

class ControlInfo(BaseInfo):
    kind = "control"

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
        self.basespec = ", ::winrt::Windows::Foundation::IInspectable"
        if self.bases:
            self.bases = [f"{namespace}.{b}" if "." not in b else b for b in self.bases]
        #    self.basespec = "".join(f", {b.replace('.', '::')}" for b in self.bases)


class EnumInfo(BaseInfo):
    kind = "enum"
    def __init__(self, *names, namespace=""):
        super().__init__(namespace)
        self.members = names


class AsyncOpInfo(BaseInfo):
    kind = "asyncop"
    def __init__(self, type, namespace=""):
        super().__init__(namespace)
        self.result = type

    def make_info(self, namespace, name):
        # Keep the name we were originally provided
        return super().make_info(namespace, self.result)


class CALL:
    kind = "call"
    def __init__(self, cvt="", **kwargs):
        self.cvt = cvt
        self.args = list(kwargs.items())
        self.prototype = "".join(f", {v} {k}" for k, v in self.args)
        self.argspec = ", ".join(f"{k}" for k, v in self.args)

class GET:
    kind = "get"
    def __init__(self, type, cvt=""):
        self.type = type
        self.cvt = cvt

class GETSET(GET):
    kind = "getset"

class FIELD(GET):
    kind = "field"


ANY = "IInspectable"
STR = "std::wstring"


MICROSOFT_UI = dict(
    Color=StructInfo(
        namespace="Windows.UI",
        A=FIELD("uint8_t"),
        R=FIELD("uint8_t"),
        G=FIELD("uint8_t"),
        B=FIELD("uint8_t"),
    ),
)

MICROSOFT_UI_COMPOSITION = dict(
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

MICROSOFT_UI_XAML = dict(
    Visibility=EnumInfo("Visible", "Collapsed"),
    DependencyObject={},
    FrameworkElement={
        "__base__": "UIElement",
        "DataContext": GET(ANY),
    },
    RoutedEventArgs={"OriginalSource": GET(ANY)},
    UIElement={
        "__base__": "DependencyObject",
        "Visibility": GETSET("Visibility"),
        # Strictly should be ICompositionAnimationBase, but who's counting?
        "StartAnimation": CALL(animation="::winrt::Microsoft::UI::Composition::CompositionAnimation"),
        "StopAnimation": CALL(animation="::winrt::Microsoft::UI::Composition::CompositionAnimation"),
    },
    Window={
        "Activate": CALL(),
        "Close": CALL(),
        "SetTitleBar": CALL(titleBar="UIElement"),
    },
)

MICROSOFT_UI_XAML_CONTROLS = dict(
    AnchorRequestedEventArgs={
        "Anchor": GET("UIElement"),
        "AnchorCandidates": GET("std::vector<UIElement>"),
    },
    AnimatedIcon={},
    AnimatedIconSource={},
    AnimatedVisualPlayer={},
    AnnotatedScrollBar={
        "__base__": "Control",
    },
    AnnotatedScrollBarDetailLabelRequestedEventArgs={
        "Content": GETSET(ANY),
        "ScrollOffset": GET("double"),
    },
    AnnotatedScrollBarLabel={},
    AnnotatedScrollBarScrollingEventArgs={},
    AppBar={"__base__": "ContentControl"},
    AppBarButton={},
    AppBarElementContainer={"__base__": "ContentControl"},
    AppBarSeparator={"__base__": "Control"},
    AppBarToggleButton={"__base__": "ContentControl"},
    AutoSuggestBox={},
    AutoSuggestBoxQuerySubmittedEventArgs={
        "ChosenSuggestion": GET(ANY),
        "QueryText": GET(STR),
    },
    AutoSuggestBoxSuggestionChosenEventArgs={
        "SelectedItem": GET(ANY),
    },
    AutoSuggestBoxTextChangedEventArgs={
        "CheckCurrent": CALL(),
        "Reason": GET("int"),
    },
    BitmapIcon={},
    BitmapIconSource={},
    Border={"__base__": "Microsoft.UI.Xaml.FrameworkElement"},
    BreadcrumbBar={
        "__base__": "Control",
    },
    BreadcrumbBarItem={"__base__": "ContentControl"},
    BreadcrumbBarItemClickedEventArgs={
        "Index": GET("int"),
        "Item": GET(ANY),
    },
    Button={"__base__": "ContentControl"},
    CalendarDatePicker={
        "__base__": "Control",
        "Date": GETSET("DateTime", cvt="cvt_DateTime_opt"),
        "MaxDate": GETSET("DateTime"),
        "MinDate": GETSET("DateTime"),
        "SetDisplayDate": CALL(date="DateTime"),
    },
    CalendarDatePickerDateChangedEventArgs={
        "NewDate": GET("DateTime", cvt="cvt_DateTime_opt"),
        "OldDate": GET("DateTime", cvt="cvt_DateTime_opt"),
    },
    CalendarView={
        "__base__": "Control",
        #"SelectedDates": GET("std::vector<DateTime>"),
        #"SetDisplayDate": CALL(date="DateTime"),
    },
    CalendarViewDayItem={"__base__": "Control"},
    CalendarViewDayItemChangingEventArgs={},
    CalendarViewSelectedDatesChangedEventArgs={},
    CandidateWindowBoundsChangedEventArgs={},
    Canvas={},
    CheckBox={"__base__": "ContentControl"},
    ChoosingGroupHeaderContainerEventArgs={},
    ChoosingItemContainerEventArgs={},
    CleanUpVirtualizedItemEventArgs={},
    ColorChangedEventArgs={
        "NewColor": GET("Color"),
        "OldColor": GET("Color"),
    },
    ColorPicker={
        "__base__": "Control",
        "Color": GETSET("Color"),
    },
    ColumnDefinition={},
    ColumnDefinitionCollection={},
    ComboBox={},
    ComboBoxItem={"__base__": "ContentControl"},
    ComboBoxTextSubmittedEventArgs={},
    CommandBar={},
    CommandBarFlyout={},
    CommandBarOverflowPresenter={},
    ContainerContentChangingEventArgs={},
    ContentControl={
        "__base__": "Control",
        "Content": GETSET(ANY),
    },
    ContentDialog={
        "__base__": "ContentControl",
        "CloseButtonText": GETSET(STR),
        "PrimaryButtonText": GETSET(STR),
        "SecondaryButtonText": GETSET(STR),
        "Title": GETSET(ANY),
        "ShowAsync": CALL(),
    },
    ContentDialogButtonClickDeferral={},
    ContentDialogButtonClickEventArgs={},
    ContentDialogClosedEventArgs={},
    ContentDialogClosingDeferral={},
    ContentDialogClosingEventArgs={},
    ContentDialogOpenedEventArgs={},
    ContentDialogResult=EnumInfo("None", "Primary", "Secondary"),
    ContentDialogResult_Op=AsyncOpInfo("ContentDialogResult"),
    ContentPresenter={},
    ContextMenuEventArgs={},
    Control={
        "__base__": "Microsoft.UI.Xaml.FrameworkElement",
    },
    ControlTemplate={},
    CoreWebView2InitializedEventArgs={},
    DataTemplateSelector={},
    DatePickedEventArgs={},
    DatePicker={
        "__base__": "Control",
    },
    DatePickerFlyout={},
    DatePickerFlyoutItem={},
    DatePickerFlyoutPresenter={
        "__base__": "Control",
    },
    DatePickerSelectedValueChangedEventArgs={},
    DatePickerValueChangedEventArgs={},
    DragItemsCompletedEventArgs={},
    DragItemsStartingEventArgs={},
    DropDownButton={},
    DynamicOverflowItemsChangingEventArgs={},
    Expander={"__base__": "ContentControl"},
    ExpanderCollapsedEventArgs={},
    ExpanderExpandingEventArgs={},
    ExpanderTemplateSettings={},
    FlipView={},
    FlipViewItem={"__base__": "ContentControl"},
    Flyout={},
    FlyoutPresenter={"__base__": "ContentControl"},
    FocusDisengagedEventArgs={},
    FocusEngagedEventArgs={},
    FontIcon={},
    FontIconSource={},
    Frame={"__base__": "ContentControl"},
    Grid={},
    GridView={},
    GridViewHeaderItem={},
    GridViewItem={"__base__": "ContentControl"},
    GroupItem={"__base__": "ContentControl"},
    GroupStyle={},
    GroupStyleSelector={},
    HasValidationErrorsChangedEventArgs={},
    Hub={
        "__base__": "Control",
    },
    HubSection={"__base__": "Control"},
    HubSectionCollection={},
    HubSectionHeaderClickEventArgs={},
    HyperlinkButton={"__base__": "ContentControl"},
    IconElement={},
    IconSource={},
    IconSourceElement={},
    Image={},
    ImageIcon={},
    ImageIconSource={},
    InfoBadge={
        "__base__": "Control",
    },
    InfoBadgeTemplateSettings={},
    InfoBar={
        "__base__": "Control",
        "Message": GETSET(STR),
        "IsOpen": GETSET("bool"),
    },
    InfoBarClosedEventArgs={},
    InfoBarClosingEventArgs={},
    InfoBarTemplateSettings={},
    IsTextTrimmedChangedEventArgs={},
    ItemClickEventArgs={},
    ItemCollection={},
    ItemCollectionTransition={},
    ItemCollectionTransitionCompletedEventArgs={},
    ItemCollectionTransitionProgress={},
    ItemCollectionTransitionProvider={},
    ItemContainer={
        "__base__": "Control",
    },
    ItemContainerGenerator={},
    ItemsControl={
        "__base__": "Control",
    },
    ItemsPanelTemplate={},
    ItemsPickedEventArgs={},
    ItemsPresenter={},
    ItemsRepeater={},
    ItemsRepeaterElementClearingEventArgs={},
    ItemsRepeaterElementIndexChangedEventArgs={},
    ItemsRepeaterElementPreparedEventArgs={},
    ItemsRepeaterScrollHost={},
    ItemsSourceView={},
    ItemsStackPanel={},
    ItemsView={
        "__base__": "Control",
    },
    ItemsViewItemInvokedEventArgs={},
    ItemsViewSelectionChangedEventArgs={},
    ItemsWrapGrid={},
    Layout={},
    LayoutContext={},
    LinedFlowLayout={},
    LinedFlowLayoutItemCollectionTransitionProvider={},
    LinedFlowLayoutItemsInfoRequestedEventArgs={},
    ListBox={},
    ListBoxItem={"__base__": "ContentControl"},
    ListPickerFlyout={},
    ListPickerFlyoutPresenter={"__base__": "Control"},
    ListView={},
    ListViewBase={},
    ListViewBaseHeaderItem={"__base__": "ContentControl"},
    ListViewHeaderItem={},
    ListViewItem={"__base__": "ContentControl"},
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
        "Pause": CALL(),
        "Play": CALL(),
        "StepBackwardOneFrame": CALL(),
        "StepForwardOneFrame": CALL(),
    },
    MediaPlayerElement={
        "__base__": "Control",
        "MediaPlayer": GET("MediaPlayer"),
    },
    MediaPlayerPresenter={},
    MediaTransportControls={
        "__base__": "Control",
    },
    MediaTransportControlsHelper={},
    MenuBar={
        "__base__": "Control",
    },
    MenuBarItem={
        "__base__": "Control",
    },
    MenuBarItemFlyout={},
    MenuFlyout={},
    MenuFlyoutItem={},
    MenuFlyoutItemBase={
        "__base__": "Control",
    },
    MenuFlyoutPresenter={},
    MenuFlyoutSeparator={},
    MenuFlyoutSubItem={},
    NavigationView={"__base__": "ContentControl"},
    NavigationViewBackRequestedEventArgs={},
    NavigationViewDisplayModeChangedEventArgs={},
    NavigationViewItem={},
    NavigationViewItemBase={"__base__": "ContentControl"},
    NavigationViewItemCollapsedEventArgs={},
    NavigationViewItemExpandingEventArgs={},
    NavigationViewItemHeader={},
    NavigationViewItemInvokedEventArgs={},
    NavigationViewItemSeparator={},
    NavigationViewPaneClosingEventArgs={},
    NavigationViewSelectionChangedEventArgs={},
    NavigationViewTemplateSettings={},
    NonVirtualizingLayout={},
    NonVirtualizingLayoutContext={},
    NumberBox={
        "__base__": "Control",
    },
    NumberBoxValueChangedEventArgs={},
    Page={},
    Panel={},
    ParallaxView={},
    PasswordBox={
        "__base__": "Control",
    },
    PasswordBoxPasswordChangingEventArgs={},
    PathIcon={},
    PathIconSource={},
    PersonPicture={
        "__base__": "Control",
    },
    PersonPictureTemplateSettings={},
    PickerConfirmedEventArgs={},
    PickerFlyout={},
    PickerFlyoutPresenter={"__base__": "ContentControl"},
    PipsPager={
        "__base__": "Control",
    },
    PipsPagerSelectedIndexChangedEventArgs={},
    PipsPagerTemplateSettings={},
    Pivot={},
    PivotItem={"__base__": "ContentControl"},
    PivotItemEventArgs={},
    PointerRoutedEventArgs={"__namespace__":"Microsoft.UI.Xaml.Input"},
    ProgressBar={},
    ProgressBarTemplateSettings={},
    ProgressRing={
        "__base__": "Control",
    },
    ProgressRingTemplateSettings={},
    RadioButton={"__base__": "ContentControl"},
    RadioButtons={
        "__base__": "Control",
    },
    RadioMenuFlyoutItem={},
    RatingControl={
        "__base__": "Control",
    },
    RatingItemFontInfo={},
    RatingItemImageInfo={},
    RatingItemInfo={},
    RefreshContainer={"__base__": "ContentControl"},
    RefreshInteractionRatioChangedEventArgs={},
    RefreshRequestedEventArgs={},
    RefreshStateChangedEventArgs={},
    RefreshVisualizer={
        "__base__": "Control",
    },
    RelativePanel={},
    RevealListViewItemPresenter={},
    RichEditBox={
        "__base__": "Control",
    },
    RichEditBoxSelectionChangingEventArgs={},
    RichEditBoxTextChangingEventArgs={},
    RichTextBlock={},
    RichTextBlockOverflow={},
    RowDefinition={},
    RowDefinitionCollection={},
    ScrollContentPresenter={},
    ScrollingAnchorRequestedEventArgs={},
    ScrollingBringingIntoViewEventArgs={},
    ScrollingScrollAnimationStartingEventArgs={},
    ScrollingScrollCompletedEventArgs={},
    ScrollingScrollOptions={},
    ScrollingZoomAnimationStartingEventArgs={},
    ScrollingZoomCompletedEventArgs={},
    ScrollingZoomOptions={},
    ScrollView={
        "__base__": "Control",
    },
    ScrollViewer={
        "__base__": "ContentControl"
    },
    ScrollViewerView={},
    ScrollViewerViewChangedEventArgs={},
    ScrollViewerViewChangingEventArgs={},
    SectionsInViewChangedEventArgs={},
    SelectionChangedEventArgs={},
    SemanticZoom={
        "__base__": "Control",
    },
    SemanticZoomLocation={},
    SemanticZoomViewChangedEventArgs={},
    Slider={},
    SplitButton={"__base__": "ContentControl"},
    SplitButtonClickEventArgs={},
    SplitView={
        "__base__": "Control",
    },
    SplitViewPaneClosingEventArgs={},
    StackLayout={},
    StackPanel={},
    StyleSelector={},
    SwapChainPanel={},
    SwipeControl={"__base__": "ContentControl"},
    SwipeItem={},
    SwipeItemInvokedEventArgs={},
    SwipeItems={},
    SymbolIcon={},
    SymbolIconSource={},
    TabView={
        "__base__": "Control",
    },
    TabViewItem={},
    TabViewItemTemplateSettings={},
    TabViewTabCloseRequestedEventArgs={},
    TabViewTabDragCompletedEventArgs={},
    TabViewTabDragStartingEventArgs={},
    TabViewTabDroppedOutsideEventArgs={},
    TeachingTip={"__base__": "ContentControl"},
    TeachingTipClosedEventArgs={},
    TeachingTipClosingEventArgs={},
    TeachingTipTemplateSettings={},
    TextBlock={},
    TextBox={
        "__base__": "Control",
        "Text": GETSET(STR),
    },
    TextBoxBeforeTextChangingEventArgs={},
    TextBoxSelectionChangingEventArgs={},
    TextBoxTextChangingEventArgs={},
    TextChangedEventArgs={},
    TextCommandBarFlyout={},
    TextCompositionChangedEventArgs={},
    TextCompositionEndedEventArgs={},
    TextCompositionStartedEventArgs={},
    TextControlCopyingToClipboardEventArgs={},
    TextControlCuttingToClipboardEventArgs={},
    TextControlPasteEventArgs={},
    TimePickedEventArgs={},
    TimePicker={
        "__base__": "Control",
    },
    TimePickerFlyout={},
    TimePickerFlyoutPresenter={"__base__": "Control"},
    TimePickerSelectedValueChangedEventArgs={},
    TimePickerValueChangedEventArgs={},
    ToggleMenuFlyoutItem={},
    ToggleSplitButton={},
    ToggleSplitButtonIsCheckedChangedEventArgs={},
    ToggleSwitch={
        "__base__": "Control",
    },
    ToolTip={"__base__": "ContentControl"},
    ToolTipService={},
    TreeView={
        "__base__": "Control",
    },
    TreeViewCollapsedEventArgs={},
    TreeViewDragItemsCompletedEventArgs={},
    TreeViewDragItemsStartingEventArgs={},
    TreeViewExpandingEventArgs={},
    TreeViewItem={},
    TreeViewItemInvokedEventArgs={},
    TreeViewItemTemplateSettings={},
    TreeViewList={},
    TreeViewNode={},
    TreeViewSelectionChangedEventArgs={},
    TwoPaneView={
        "__base__": "Control",
    },
    UIElementCollection={},
    UniformGridLayout={},
    VariableSizedWrapGrid={},
    Viewbox={},
    VirtualizingLayout={},
    VirtualizingLayoutContext={},
    VirtualizingPanel={},
    VirtualizingStackPanel={},
    WebView2={},
    WrapGrid={},
    XamlControlsResources={},
)

def info(ns, name, members):
    try:
        make_info = members.make_info
    except AttributeError:
        return ControlInfo(ns, name, members)
    else:
        return make_info(ns, name)


CONTROLS = [
    *(info("Microsoft.UI", k, v) for k, v in MICROSOFT_UI.items()),
    *(info("Microsoft.UI.Composition", k, v) for k, v in MICROSOFT_UI_COMPOSITION.items()),
    *(info("Microsoft.UI.Xaml", k, v) for k, v in MICROSOFT_UI_XAML.items()),
    *(info("Microsoft.UI.Xaml.Controls", k, v) for k, v in MICROSOFT_UI_XAML_CONTROLS.items()),
]

def resolve_bases(controls):
    derived = {}
    todo = []
    for c in controls:
        if c.kind == "control":
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

    for c in controls:
        for sub in derived.get(c.fullname, ()):
            sub.members.update(c.members)
resolve_bases(CONTROLS)

CONTEXT = dict(
    all_controls=CONTROLS,
)

with open(OUTPUT, "w", encoding="ascii") as f:
    for s in RENDER_ENV.get_template("controls.cpp.in").generate(CONTEXT):
        f.write(s)
