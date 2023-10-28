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


PYBIND11_EMBEDDED_MODULE(_winui_Windows_Media_Playback, m) {
    py::enum_<Windows::Media::Playback::MediaPlaybackState>(m, "Windows.Media.Playback.MediaPlaybackState")
        .value("None", Windows::Media::Playback::MediaPlaybackState::None)
        .value("Opening", Windows::Media::Playback::MediaPlaybackState::Opening)
        .value("Buffering", Windows::Media::Playback::MediaPlaybackState::Buffering)
        .value("Playing", Windows::Media::Playback::MediaPlaybackState::Playing)
        .value("Paused", Windows::Media::Playback::MediaPlaybackState::Paused)
    ;

    py::class_<Windows::Media::Playback::MediaPlaybackSession, ::pywinui::holder<Windows::Media::Playback::MediaPlaybackSession>, Windows::Foundation::IInspectable>(m, "Windows.Media.Playback.MediaPlaybackSession")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Windows::Media::Playback::MediaPlaybackSession>()); }))
        .def("__repr__", [](typename cvt<Windows::Media::Playback::MediaPlaybackSession>::cself_t _self) { return default_repr(cvt<Windows::Media::Playback::MediaPlaybackSession>(_self)); } )
        .def_property_readonly("NaturalDuration", [](typename cvt<Windows::Media::Playback::MediaPlaybackSession>::cself_t _self) { return cvt_out(_self.NaturalDuration()); })
        .def_property_readonly("PlaybackState", [](typename cvt<Windows::Media::Playback::MediaPlaybackSession>::cself_t _self) { return cvt_out(_self.PlaybackState()); })
        .def_property_readonly("Position", [](typename cvt<Windows::Media::Playback::MediaPlaybackSession>::cself_t _self) { return cvt_out(_self.Position()); })
    ;
    py::class_<Windows::Media::Playback::MediaPlayer, ::pywinui::holder<Windows::Media::Playback::MediaPlayer>, Windows::Foundation::IInspectable>(m, "Windows.Media.Playback.MediaPlayer")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Windows::Media::Playback::MediaPlayer>()); }))
        .def("__repr__", [](typename cvt<Windows::Media::Playback::MediaPlayer>::cself_t _self) { return default_repr(cvt<Windows::Media::Playback::MediaPlayer>(_self)); } )
        .def_property_readonly("PlaybackSession", [](typename cvt<Windows::Media::Playback::MediaPlayer>::cself_t _self) { return cvt_out(_self.PlaybackSession()); })
        .def("Pause", [](typename cvt<Windows::Media::Playback::MediaPlayer>::self_t _self) {ensure_void<decltype(_self.Pause())> ensure; (void)ensure;(_self.Pause()); })
        .def("Play", [](typename cvt<Windows::Media::Playback::MediaPlayer>::self_t _self) {ensure_void<decltype(_self.Play())> ensure; (void)ensure;(_self.Play()); })
        .def("StepBackwardOneFrame", [](typename cvt<Windows::Media::Playback::MediaPlayer>::self_t _self) {ensure_void<decltype(_self.StepBackwardOneFrame())> ensure; (void)ensure;(_self.StepBackwardOneFrame()); })
        .def("StepForwardOneFrame", [](typename cvt<Windows::Media::Playback::MediaPlayer>::self_t _self) {ensure_void<decltype(_self.StepForwardOneFrame())> ensure; (void)ensure;(_self.StepForwardOneFrame()); })
    ;
}
