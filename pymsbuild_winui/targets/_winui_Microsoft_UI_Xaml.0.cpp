// ****************************************************** //
// Generated by scripts\controls.py
// ****************************************************** //
#include "pch.h"
#include "_winui.h"

void add_enum_Microsoft_UI_Xaml_Visibility(const py::module_ &m) {
    py::enum_<Microsoft::UI::Xaml::Visibility>(m, "Microsoft.UI.Xaml.Visibility")
        .value("Visible", Microsoft::UI::Xaml::Visibility::Visible)
        .value("Collapsed", Microsoft::UI::Xaml::Visibility::Collapsed)
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_BringIntoViewOptions(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::BringIntoViewOptions, ::pywinui::holder<Microsoft::UI::Xaml::BringIntoViewOptions>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.BringIntoViewOptions")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::BringIntoViewOptions>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::cself_t _self) { return cvt<Microsoft::UI::Xaml::BringIntoViewOptions>(_self).repr(); })
        .def(py::init([]() { Microsoft::UI::Xaml::BringIntoViewOptions inst{  }; return cvt_out(inst); }))
        .def_property("HorizontalAlignmentRatio", [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::cself_t _self) { return cvt_out(_self.HorizontalAlignmentRatio()); }, [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::self_t _self, typename cvt<decltype(_self.HorizontalAlignmentRatio())>::arg_t v) { cvt<decltype(_self.HorizontalAlignmentRatio())>::param_t cvt_v{v}; _self.HorizontalAlignmentRatio(cvt_v); })
        .def_property("HorizontalOffset", [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::cself_t _self) { return cvt_out(_self.HorizontalOffset()); }, [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::self_t _self, typename cvt<decltype(_self.HorizontalOffset())>::arg_t v) { cvt<decltype(_self.HorizontalOffset())>::param_t cvt_v{v}; _self.HorizontalOffset(cvt_v); })
        .def_property("VerticalAlignmentRatio", [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::cself_t _self) { return cvt_out(_self.VerticalAlignmentRatio()); }, [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::self_t _self, typename cvt<decltype(_self.VerticalAlignmentRatio())>::arg_t v) { cvt<decltype(_self.VerticalAlignmentRatio())>::param_t cvt_v{v}; _self.VerticalAlignmentRatio(cvt_v); })
        .def_property("VerticalOffset", [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::cself_t _self) { return cvt_out(_self.VerticalOffset()); }, [](typename cvt<Microsoft::UI::Xaml::BringIntoViewOptions>::self_t _self, typename cvt<decltype(_self.VerticalOffset())>::arg_t v) { cvt<decltype(_self.VerticalOffset())>::param_t cvt_v{v}; _self.VerticalOffset(cvt_v); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_BringIntoViewRequestedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::BringIntoViewRequestedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::BringIntoViewRequestedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.BringIntoViewRequestedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::BringIntoViewRequestedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::BringIntoViewRequestedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::BringIntoViewRequestedEventArgs>(_self).repr(); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DataContextChangedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DataContextChangedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::DataContextChangedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DataContextChangedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DataContextChangedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DataContextChangedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DataContextChangedEventArgs>(_self).repr(); })
        .def_property("Handled", [](typename cvt<Microsoft::UI::Xaml::DataContextChangedEventArgs>::cself_t _self) { return cvt_out(_self.Handled()); }, [](typename cvt<Microsoft::UI::Xaml::DataContextChangedEventArgs>::self_t _self, typename cvt<decltype(_self.Handled())>::arg_t v) { cvt<decltype(_self.Handled())>::param_t cvt_v{v}; _self.Handled(cvt_v); })
        .def_property_readonly("NewValue", [](typename cvt<Microsoft::UI::Xaml::DataContextChangedEventArgs>::cself_t _self) { return cvt_out(_self.NewValue()); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DependencyObject(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DependencyObject, ::pywinui::holder<Microsoft::UI::Xaml::DependencyObject>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DependencyObject")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DependencyObject>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DependencyObject>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DependencyObject>(_self).repr(); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DependencyProperty(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DependencyProperty, ::pywinui::holder<Microsoft::UI::Xaml::DependencyProperty>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DependencyProperty")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DependencyProperty>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DependencyProperty>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DependencyProperty>(_self).repr(); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DependencyPropertyChangedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DependencyPropertyChangedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>(_self).repr(); })
        .def_property_readonly("NewValue", [](typename cvt<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>::cself_t _self) { return cvt_out(_self.NewValue()); })
        .def_property_readonly("OldValue", [](typename cvt<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>::cself_t _self) { return cvt_out(_self.OldValue()); })
        .def_property_readonly("Property", [](typename cvt<Microsoft::UI::Xaml::DependencyPropertyChangedEventArgs>::cself_t _self) { return cvt_out(_self.Property()); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DragEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DragEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::DragEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DragEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DragEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DragEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DragEventArgs>(_self).repr(); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DragStartingEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DragStartingEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::DragStartingEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DragStartingEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DragStartingEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DragStartingEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DragStartingEventArgs>(_self).repr(); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_DropCompletedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::DropCompletedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::DropCompletedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.DropCompletedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::DropCompletedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::DropCompletedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::DropCompletedEventArgs>(_self).repr(); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_EffectiveViewportChangedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.EffectiveViewportChangedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>(_self).repr(); })
        .def_property_readonly("BringIntoViewDistanceX", [](typename cvt<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>::cself_t _self) { return cvt_out(_self.BringIntoViewDistanceX()); })
        .def_property_readonly("BringIntoViewDistanceY", [](typename cvt<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>::cself_t _self) { return cvt_out(_self.BringIntoViewDistanceY()); })
        .def_property_readonly("EffectiveViewport", [](typename cvt<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>::cself_t _self) { return cvt_out(_self.EffectiveViewport()); })
        .def_property_readonly("MaxViewport", [](typename cvt<Microsoft::UI::Xaml::EffectiveViewportChangedEventArgs>::cself_t _self) { return cvt_out(_self.MaxViewport()); })
    ;
}

void add_enum_Microsoft_UI_Xaml_ElementSoundMode(const py::module_ &m) {
    py::enum_<Microsoft::UI::Xaml::ElementSoundMode>(m, "Microsoft.UI.Xaml.ElementSoundMode")
        .value("Default", Microsoft::UI::Xaml::ElementSoundMode::Default)
        .value("FocusOnly", Microsoft::UI::Xaml::ElementSoundMode::FocusOnly)
        .value("Off", Microsoft::UI::Xaml::ElementSoundMode::Off)
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_ExceptionRoutedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::ExceptionRoutedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::ExceptionRoutedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.ExceptionRoutedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::ExceptionRoutedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::ExceptionRoutedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::ExceptionRoutedEventArgs>(_self).repr(); })
        .def_property_readonly("ErrorMessage", [](typename cvt<Microsoft::UI::Xaml::ExceptionRoutedEventArgs>::cself_t _self) { return cvt_out(_self.ErrorMessage()); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_FrameworkElement(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::FrameworkElement, ::pywinui::holder<Microsoft::UI::Xaml::FrameworkElement>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.FrameworkElement")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::FrameworkElement>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::FrameworkElement>::cself_t _self) { return cvt<Microsoft::UI::Xaml::FrameworkElement>(_self).repr(); })
        .def_property_readonly("DataContext", [](typename cvt<Microsoft::UI::Xaml::FrameworkElement>::cself_t _self) { return cvt_out(_self.DataContext()); })
        .def_property("Visibility", [](typename cvt<Microsoft::UI::Xaml::FrameworkElement>::cself_t _self) { return cvt_out(_self.Visibility()); }, [](typename cvt<Microsoft::UI::Xaml::FrameworkElement>::self_t _self, typename cvt<decltype(_self.Visibility())>::arg_t v) { cvt<decltype(_self.Visibility())>::param_t cvt_v{v}; _self.Visibility(cvt_v); })
        .def("StartAnimation", [](typename cvt<Microsoft::UI::Xaml::FrameworkElement>::self_t _self, typename cvt<Microsoft::UI::Composition::CompositionAnimation>::arg_t animation) {cvt<Microsoft::UI::Composition::CompositionAnimation>::param_t cvt_animation{ animation }; static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::FrameworkElement::StartAnimation)>::value, "return value is not void"); _self.StartAnimation(cvt_animation); })
        .def("StopAnimation", [](typename cvt<Microsoft::UI::Xaml::FrameworkElement>::self_t _self, typename cvt<Microsoft::UI::Composition::CompositionAnimation>::arg_t animation) {cvt<Microsoft::UI::Composition::CompositionAnimation>::param_t cvt_animation{ animation }; static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::FrameworkElement::StopAnimation)>::value, "return value is not void"); _self.StopAnimation(cvt_animation); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_RoutedEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::RoutedEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::RoutedEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.RoutedEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::RoutedEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::RoutedEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::RoutedEventArgs>(_self).repr(); })
        .def_property_readonly("OriginalSource", [](typename cvt<Microsoft::UI::Xaml::RoutedEventArgs>::cself_t _self) { return cvt_out(_self.OriginalSource()); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_UIElement(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::UIElement, ::pywinui::holder<Microsoft::UI::Xaml::UIElement>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.UIElement")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::UIElement>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::UIElement>::cself_t _self) { return cvt<Microsoft::UI::Xaml::UIElement>(_self).repr(); })
        .def_property("Visibility", [](typename cvt<Microsoft::UI::Xaml::UIElement>::cself_t _self) { return cvt_out(_self.Visibility()); }, [](typename cvt<Microsoft::UI::Xaml::UIElement>::self_t _self, typename cvt<decltype(_self.Visibility())>::arg_t v) { cvt<decltype(_self.Visibility())>::param_t cvt_v{v}; _self.Visibility(cvt_v); })
        .def("StartAnimation", [](typename cvt<Microsoft::UI::Xaml::UIElement>::self_t _self, typename cvt<Microsoft::UI::Composition::CompositionAnimation>::arg_t animation) {cvt<Microsoft::UI::Composition::CompositionAnimation>::param_t cvt_animation{ animation }; static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::UIElement::StartAnimation)>::value, "return value is not void"); _self.StartAnimation(cvt_animation); })
        .def("StopAnimation", [](typename cvt<Microsoft::UI::Xaml::UIElement>::self_t _self, typename cvt<Microsoft::UI::Composition::CompositionAnimation>::arg_t animation) {cvt<Microsoft::UI::Composition::CompositionAnimation>::param_t cvt_animation{ animation }; static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::UIElement::StopAnimation)>::value, "return value is not void"); _self.StopAnimation(cvt_animation); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_Window(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::Window, ::pywinui::holder<Microsoft::UI::Xaml::Window>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.Window")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::Window>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::Window>::cself_t _self) { return cvt<Microsoft::UI::Xaml::Window>(_self).repr(); })
        .def("Activate", [](typename cvt<Microsoft::UI::Xaml::Window>::self_t _self) {static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::Window::Activate)>::value, "return value is not void"); _self.Activate(); })
        .def("Close", [](typename cvt<Microsoft::UI::Xaml::Window>::self_t _self) {static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::Window::Close)>::value, "return value is not void"); _self.Close(); })
        .def("SetTitleBar", [](typename cvt<Microsoft::UI::Xaml::Window>::self_t _self, typename cvt<Microsoft::UI::Xaml::UIElement>::arg_t titleBar) {cvt<Microsoft::UI::Xaml::UIElement>::param_t cvt_titleBar{ titleBar }; static_assert(ensure_void<decltype(&Microsoft::UI::Xaml::Window::SetTitleBar)>::value, "return value is not void"); _self.SetTitleBar(cvt_titleBar); })
    ;
}

void add_runtimeclass_Microsoft_UI_Xaml_WindowEventArgs(const py::module_ &m) {
    py::class_<Microsoft::UI::Xaml::WindowEventArgs, ::pywinui::holder<Microsoft::UI::Xaml::WindowEventArgs>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.WindowEventArgs")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::WindowEventArgs>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::WindowEventArgs>::cself_t _self) { return cvt<Microsoft::UI::Xaml::WindowEventArgs>(_self).repr(); })
        .def_property("Handled", [](typename cvt<Microsoft::UI::Xaml::WindowEventArgs>::cself_t _self) { return cvt_out(_self.Handled()); }, [](typename cvt<Microsoft::UI::Xaml::WindowEventArgs>::self_t _self, typename cvt<decltype(_self.Handled())>::arg_t v) { cvt<decltype(_self.Handled())>::param_t cvt_v{v}; _self.Handled(cvt_v); })
    ;
}

