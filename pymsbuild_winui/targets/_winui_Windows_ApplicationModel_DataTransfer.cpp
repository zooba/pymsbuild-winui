// ****************************************************** //
// Generated by scripts\controls.py
// ****************************************************** //
#include "pch.h"
#include "_winui.h"

template <> struct cvt<Microsoft::UI::Composition::CompositionAnimation>  {
    typedef Microsoft::UI::Composition::CompositionAnimation natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<Microsoft::UI::Composition::CompositionAnimation> param_t;
    std::optional<natural_t> value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    py_t ret() { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator py_t () const { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator const natural_t & () const { return value.value_or(nullptr); }
    operator Microsoft::UI::Composition::ICompositionAnimationBase () const { return value ? value->as<Microsoft::UI::Composition::ICompositionAnimationBase>() : nullptr; }
};

template <> struct cvt<Microsoft::UI::Composition::ExpressionAnimation>  {
    typedef Microsoft::UI::Composition::ExpressionAnimation natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<Microsoft::UI::Composition::ExpressionAnimation> param_t;
    std::optional<natural_t> value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    py_t ret() { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator py_t () const { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator const natural_t & () const { return value.value_or(nullptr); }
    operator Microsoft::UI::Composition::ICompositionAnimationBase () const { return value ? value->as<Microsoft::UI::Composition::ICompositionAnimationBase>() : nullptr; }
};

template <> struct cvt<Microsoft::UI::Composition::KeyFrameAnimation>  {
    typedef Microsoft::UI::Composition::KeyFrameAnimation natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<Microsoft::UI::Composition::KeyFrameAnimation> param_t;
    std::optional<natural_t> value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    py_t ret() { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator py_t () const { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator const natural_t & () const { return value.value_or(nullptr); }
    operator Microsoft::UI::Composition::ICompositionAnimationBase () const { return value ? value->as<Microsoft::UI::Composition::ICompositionAnimationBase>() : nullptr; }
};

template <> struct cvt<Microsoft::UI::Composition::NaturalMotionAnimation>  {
    typedef Microsoft::UI::Composition::NaturalMotionAnimation natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<Microsoft::UI::Composition::NaturalMotionAnimation> param_t;
    std::optional<natural_t> value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    py_t ret() { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator py_t () const { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator const natural_t & () const { return value.value_or(nullptr); }
    operator Microsoft::UI::Composition::ICompositionAnimationBase () const { return value ? value->as<Microsoft::UI::Composition::ICompositionAnimationBase>() : nullptr; }
};

template <> struct cvt<Microsoft::UI::Composition::SpringVector3NaturalMotionAnimation>  {
    typedef Microsoft::UI::Composition::SpringVector3NaturalMotionAnimation natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<Microsoft::UI::Composition::SpringVector3NaturalMotionAnimation> param_t;
    std::optional<natural_t> value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    py_t ret() { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator py_t () const { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator const natural_t & () const { return value.value_or(nullptr); }
    operator Microsoft::UI::Composition::ICompositionAnimationBase () const { return value ? value->as<Microsoft::UI::Composition::ICompositionAnimationBase>() : nullptr; }
};

template <> struct cvt<Microsoft::UI::Composition::Vector3NaturalMotionAnimation>  {
    typedef Microsoft::UI::Composition::Vector3NaturalMotionAnimation natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<Microsoft::UI::Composition::Vector3NaturalMotionAnimation> param_t;
    std::optional<natural_t> value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    py_t ret() { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator py_t () const { return ::pywinui::holder<natural_t>(value.value_or(nullptr)); }
    operator const natural_t & () const { return value.value_or(nullptr); }
    operator Microsoft::UI::Composition::ICompositionAnimationBase () const { return value ? value->as<Microsoft::UI::Composition::ICompositionAnimationBase>() : nullptr; }
};


PYBIND11_EMBEDDED_MODULE(_winui_Windows_ApplicationModel_DataTransfer, m) {
    py::enum_<Windows::ApplicationModel::DataTransfer::DataPackageOperation>(m, "Windows.ApplicationModel.DataTransfer.DataPackageOperation")
        .value("None", Windows::ApplicationModel::DataTransfer::DataPackageOperation::None)
        .value("Copy", Windows::ApplicationModel::DataTransfer::DataPackageOperation::Copy)
        .value("Move", Windows::ApplicationModel::DataTransfer::DataPackageOperation::Move)
        .value("Link", Windows::ApplicationModel::DataTransfer::DataPackageOperation::Link)
    ;

    py::class_<Windows::ApplicationModel::DataTransfer::DataPackage, ::pywinui::holder<Windows::ApplicationModel::DataTransfer::DataPackage>, Windows::Foundation::IInspectable>(m, "Windows.ApplicationModel.DataTransfer.DataPackage")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Windows::ApplicationModel::DataTransfer::DataPackage>()); }))
        .def("__repr__", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::cself_t _self) { return default_repr(cvt<Windows::ApplicationModel::DataTransfer::DataPackage>(_self)); } )
        .def_property("RequestedOperation", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::cself_t _self) { return cvt_out(_self.RequestedOperation()); }, [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<decltype(_self.RequestedOperation())>::arg_t v) { cvt<decltype(_self.RequestedOperation())>::param_t cvt_v{v}; _self.RequestedOperation(cvt_v); })
        .def("SetApplicationLink", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<Windows::Foundation::Uri>::arg_t value) {cvt<Windows::Foundation::Uri>::param_t cvt_value{ value }; static_assert(ensure_void<decltype(&Windows::ApplicationModel::DataTransfer::DataPackage::SetApplicationLink)>::value, "return value is not void"); _self.SetApplicationLink(cvt_value); })
        .def("SetData", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<winrt::hstring>::arg_t formatId, typename cvt<Windows::Foundation::IInspectable>::arg_t value) {cvt<winrt::hstring>::param_t cvt_formatId{ formatId }; cvt<Windows::Foundation::IInspectable>::param_t cvt_value{ value }; static_assert(ensure_void<decltype(&Windows::ApplicationModel::DataTransfer::DataPackage::SetData)>::value, "return value is not void"); _self.SetData(cvt_formatId, cvt_value); })
        .def("SetHtmlFormat", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<winrt::hstring>::arg_t value) {cvt<winrt::hstring>::param_t cvt_value{ value }; static_assert(ensure_void<decltype(&Windows::ApplicationModel::DataTransfer::DataPackage::SetHtmlFormat)>::value, "return value is not void"); _self.SetHtmlFormat(cvt_value); })
        .def("SetRtf", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<winrt::hstring>::arg_t value) {cvt<winrt::hstring>::param_t cvt_value{ value }; static_assert(ensure_void<decltype(&Windows::ApplicationModel::DataTransfer::DataPackage::SetRtf)>::value, "return value is not void"); _self.SetRtf(cvt_value); })
        .def("SetText", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<winrt::hstring>::arg_t value) {cvt<winrt::hstring>::param_t cvt_value{ value }; static_assert(ensure_void<decltype(&Windows::ApplicationModel::DataTransfer::DataPackage::SetText)>::value, "return value is not void"); _self.SetText(cvt_value); })
        .def("SetWebLink", [](typename cvt<Windows::ApplicationModel::DataTransfer::DataPackage>::self_t _self, typename cvt<Windows::Foundation::Uri>::arg_t value) {cvt<Windows::Foundation::Uri>::param_t cvt_value{ value }; static_assert(ensure_void<decltype(&Windows::ApplicationModel::DataTransfer::DataPackage::SetWebLink)>::value, "return value is not void"); _self.SetWebLink(cvt_value); })
    ;
}
