// ****************************************************** //
// Generated by scripts\controls.py
// ****************************************************** //
#include "pch.h"
#include "_winui.h"

extern void add_runtimeclass_Microsoft_UI_Xaml_Input_DoubleTappedRoutedEventArgs(const py::module_ &m);
extern void add_runtimeclass_Microsoft_UI_Xaml_Input_Pointer(const py::module_ &m);
extern void add_runtimeclass_Microsoft_UI_Xaml_Input_PointerRoutedEventArgs(const py::module_ &m);
extern void add_runtimeclass_Microsoft_UI_Xaml_Input_RightTappedRoutedEventArgs(const py::module_ &m);
extern void add_runtimeclass_Microsoft_UI_Xaml_Input_TappedRoutedEventArgs(const py::module_ &m);

PYBIND11_EMBEDDED_MODULE(_winui_Microsoft_UI_Xaml_Input, m) {
    add_runtimeclass_Microsoft_UI_Xaml_Input_DoubleTappedRoutedEventArgs(m);
    add_runtimeclass_Microsoft_UI_Xaml_Input_Pointer(m);
    add_runtimeclass_Microsoft_UI_Xaml_Input_PointerRoutedEventArgs(m);
    add_runtimeclass_Microsoft_UI_Xaml_Input_RightTappedRoutedEventArgs(m);
    add_runtimeclass_Microsoft_UI_Xaml_Input_TappedRoutedEventArgs(m);
}