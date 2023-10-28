#include "pch.h"
#include "_winui.h"

using namespace winrt;
using namespace Windows::Foundation;
namespace py = pybind11;

PYBIND11_EMBEDDED_MODULE(_winui_Windows_Foundation_Collections, m) {
    using Elem = ::Windows::Foundation::IInspectable;
    using Cls = ::Windows::Foundation::Collections::IVector<Elem>;
    py::class_<Cls, ::pywinui::holder<Cls>>(m, "Windows.Foundation.Collections.ObservableVector")
        .def(py::init([]() { return ::pywinui::hold<Cls>(winrt::single_threaded_vector<Elem>()); }))
        .def("append", [](Cls &c, const Elem &e) { c.Append(e); })
        .def("clear", [](Cls &c) { c.Clear(); })
        .def("insert", [](Cls &c, uint32_t index, const Elem &e) { c.InsertAt(index, e); })
        .def("__delitem__", [](Cls &c, uint32_t index) { c.RemoveAt(index); })
        .def("__getitem__", [](Cls &c, uint32_t index) { return c.GetAt(index); })
        .def("__len__", [](const Cls &c) { return c.Size(); })
    ;

}

