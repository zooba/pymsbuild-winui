#include "pch.h"
#include "_winui.h"

using namespace winrt;
using namespace Windows::Foundation;
namespace py = pybind11;

PYBIND11_EMBEDDED_MODULE(_winui_Windows_Foundation_Collections, m) {
    using Elem = ::Windows::Foundation::IInspectable;
    using Cls = ::Windows::Foundation::Collections::IVector<Elem>;
    py::class_<Cls, ::pywinui::holder<Cls>>(m, "Windows.Foundation.Collections.IVector")
        .def(py::init([]() { return ::pywinui::hold<Cls>(winrt::single_threaded_observable_vector<Elem>()); }))
        .def("append", [](Cls &c, const Elem &e) { c.Append(e); })
        .def("extend", [](Cls &c, py::object iterable) {
            for (auto it = py::iter(iterable); it != py::iterator::sentinel(); ++it) {
                c.Append(py::cast<Elem>(*it));
            }
        })
        .def("replace_all", [](Cls &c, py::object iterable) {
            std::vector<Elem> tmp;
            for (auto it = py::iter(iterable); it != py::iterator::sentinel(); ++it) {
                tmp.emplace_back(py::cast<Elem>(*it));
            }
            py::gil_scoped_release _g;
            c.ReplaceAll(tmp);
        })
        .def("clear", [](Cls &c) { c.Clear(); })
        .def("insert", [](Cls &c, uint32_t index, const Elem &e) { c.InsertAt(index, e); })
        .def("__delitem__", [](Cls &c, uint32_t index) { c.RemoveAt(index); })
        .def("__getitem__", [](Cls &c, uint32_t index) { return c.GetAt(index); })
        .def("__len__", [](const Cls &c) { return c.Size(); })
        .def("__repr__", [](const Cls &c) {
            std::wstringstream s{L"["};
            auto end = c.Size() - 1;
            for (uint32_t i = 0; i <= end; ++i) {
                cvt<Elem> v(c.GetAt(i));
                s << v.repr();
                if (i != end) {
                    s << L", ";
                }
            }
            s << L"]";
            return s.str();
        })
    ;

}

