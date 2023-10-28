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


PYBIND11_EMBEDDED_MODULE(_winui_Windows_UI_Xaml_Interop, m) {

}
