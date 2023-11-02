// ****************************************************** //
// Generated by scripts\controls.py
// ****************************************************** //
#include "pch.h"
#include "_winui.h"

void add_runtimeclass_Microsoft_UI_Dispatching_DispatcherQueue(const py::module_ &m) {
    py::class_<Microsoft::UI::Dispatching::DispatcherQueue, ::pywinui::holder<Microsoft::UI::Dispatching::DispatcherQueue>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Dispatching.DispatcherQueue")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Dispatching::DispatcherQueue>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueue>::cself_t _self) { return cvt<Microsoft::UI::Dispatching::DispatcherQueue>(_self).repr(); })
        .def_property_readonly("HasThreadAccess", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueue>::cself_t _self) { return cvt_out(_self.HasThreadAccess()); })
        .def("CreateTimer", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueue>::self_t _self) {return cvt_out(_self.CreateTimer()); })
        .def("TryEnqueue", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueue>::self_t _self, typename cvt<Microsoft::UI::Dispatching::DispatcherQueuePriority>::arg_t priority, typename cvt<Microsoft::UI::Dispatching::DispatcherQueueHandler>::arg_t callback) {cvt<Microsoft::UI::Dispatching::DispatcherQueuePriority>::param_t cvt_priority{ priority }; cvt<Microsoft::UI::Dispatching::DispatcherQueueHandler>::param_t cvt_callback{ callback }; return cvt_out(_self.TryEnqueue(cvt_priority, cvt_callback)); })
    ;
}

void add_callback_Microsoft_UI_Dispatching_DispatcherQueueHandler(const py::module_ &m) {
    py::class_<Microsoft::UI::Dispatching::DispatcherQueueHandler, ::pywinui::holder<Microsoft::UI::Dispatching::DispatcherQueueHandler>>(m, "Microsoft.UI.Dispatching.DispatcherQueueHandler")
        .def(py::init([](py::object callable) {static_assert(ensure_Invoke_void<decltype(&::winrt::get_abi<Microsoft::UI::Dispatching::DispatcherQueueHandler>(nullptr)->Invoke)>::value, "return value is not void"); Microsoft::UI::Dispatching::DispatcherQueueHandler inst{[callable]() {py::gil_scoped_acquire _g; callable();} }; return ::pywinui::hold(inst); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueHandler>::cself_t _self) { return cvt<Microsoft::UI::Dispatching::DispatcherQueueHandler>(_self).repr(); })
    ;
}

void add_enum_Microsoft_UI_Dispatching_DispatcherQueuePriority(const py::module_ &m) {
    py::enum_<Microsoft::UI::Dispatching::DispatcherQueuePriority>(m, "Microsoft.UI.Dispatching.DispatcherQueuePriority")
        .value("Normal", Microsoft::UI::Dispatching::DispatcherQueuePriority::Normal)
        .value("High", Microsoft::UI::Dispatching::DispatcherQueuePriority::High)
        .value("Low", Microsoft::UI::Dispatching::DispatcherQueuePriority::Low)
    ;
}

void add_runtimeclass_Microsoft_UI_Dispatching_DispatcherQueueTimer(const py::module_ &m) {
    py::class_<Microsoft::UI::Dispatching::DispatcherQueueTimer, ::pywinui::holder<Microsoft::UI::Dispatching::DispatcherQueueTimer>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Dispatching.DispatcherQueueTimer")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Dispatching::DispatcherQueueTimer>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::cself_t _self) { return cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>(_self).repr(); })
        .def_property("Interval", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::cself_t _self) { return cvt_out(_self.Interval()); }, [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::self_t _self, typename cvt<decltype(_self.Interval())>::arg_t v) { cvt<decltype(_self.Interval())>::param_t cvt_v{v}; _self.Interval(cvt_v); })
        .def_property("IsRepeating", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::cself_t _self) { return cvt_out(_self.IsRepeating()); }, [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::self_t _self, typename cvt<decltype(_self.IsRepeating())>::arg_t v) { cvt<decltype(_self.IsRepeating())>::param_t cvt_v{v}; _self.IsRepeating(cvt_v); })
        .def_property_readonly("IsRunning", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::cself_t _self) { return cvt_out(_self.IsRunning()); })
        .def("Start", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::self_t _self) {static_assert(ensure_void<decltype(&Microsoft::UI::Dispatching::DispatcherQueueTimer::Start)>::value, "return value is not void"); _self.Start(); })
        .def("Stop", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::self_t _self) {static_assert(ensure_void<decltype(&Microsoft::UI::Dispatching::DispatcherQueueTimer::Stop)>::value, "return value is not void"); _self.Stop(); })
        .def("Tick", [](typename cvt<Microsoft::UI::Dispatching::DispatcherQueueTimer>::self_t _self, py::object handler) { _self.Tick(event_handler<Microsoft::UI::Dispatching::DispatcherQueueTimer, Windows::Foundation::IInspectable>(handler));
        })
    ;
}

