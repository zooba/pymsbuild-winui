// ****************************************************** //
// Generated by scripts\controls.py
// ****************************************************** //
#include "pch.h"
#include "_winui.h"

PYBIND11_EMBEDDED_MODULE(_winui_Microsoft_UI_Xaml_Data, m) {

    py::class_<Microsoft::UI::Xaml::Data::ItemIndexRange, ::pywinui::holder<Microsoft::UI::Xaml::Data::ItemIndexRange>, Windows::Foundation::IInspectable>(m, "Microsoft.UI.Xaml.Data.ItemIndexRange")
        .def(py::init([](const ::winrt::Windows::Foundation::IInspectable &unk) { return ::pywinui::hold(unk.as<Microsoft::UI::Xaml::Data::ItemIndexRange>()); }))
        .def("__repr__", [](typename cvt<Microsoft::UI::Xaml::Data::ItemIndexRange>::cself_t _self) { return cvt<Microsoft::UI::Xaml::Data::ItemIndexRange>(_self).repr(); })
        .def(py::init([](typename cvt<int>::arg_t firstIndex, typename cvt<uint32_t>::arg_t length) { cvt<int>::param_t cvt_firstIndex{ firstIndex }; cvt<uint32_t>::param_t cvt_length{ length }; Microsoft::UI::Xaml::Data::ItemIndexRange inst{ cvt_firstIndex, cvt_length }; return cvt_out(inst); }))
        .def_property_readonly("FirstIndex", [](typename cvt<Microsoft::UI::Xaml::Data::ItemIndexRange>::cself_t _self) { return cvt_out(_self.FirstIndex()); })
        .def_property_readonly("LastIndex", [](typename cvt<Microsoft::UI::Xaml::Data::ItemIndexRange>::cself_t _self) { return cvt_out(_self.LastIndex()); })
        .def_property_readonly("Length", [](typename cvt<Microsoft::UI::Xaml::Data::ItemIndexRange>::cself_t _self) { return cvt_out(_self.Length()); })
    ;
}
