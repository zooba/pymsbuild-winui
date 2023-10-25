#pragma once
#include <windows.h>
#include <unknwn.h>
#include <restrictederrorinfo.h>
#include <hstring.h>

// conflicts with Storyboard::GetCurrentTime
#undef GetCurrentTime

#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Media.Playback.h>
#include <winrt/Windows.ApplicationModel.Activation.h>
#include <winrt/Microsoft.UI.h>
#include <winrt/Microsoft.UI.Composition.h>
#include <winrt/Microsoft.UI.Xaml.h>
#include <winrt/Microsoft.UI.Xaml.Controls.h>
#include <winrt/Microsoft.UI.Xaml.Controls.Primitives.h>
#include <winrt/Microsoft.UI.Xaml.Data.h>
#include <winrt/Microsoft.UI.Xaml.Interop.h>
#include <winrt/Microsoft.UI.Xaml.Markup.h>
#include <winrt/Microsoft.UI.Xaml.Media.h>
#include <winrt/Microsoft.UI.Xaml.Navigation.h>
#include <winrt/Microsoft.UI.Xaml.Shapes.h>
#include <winrt/Microsoft.UI.Dispatching.h>
#include <wil/cppwinrt_helpers.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <exception>
#include <sstream>

#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#include <pybind11\chrono.h>
#include <pybind11\embed.h>

namespace pywinui {
    template <typename T> struct holder {
        T v;
        holder(T t) : v{t} { }
        holder(T *t) : v{*t} { }
        inline T *get() const { return (T *)&v; }
    };

    template <typename T>
    std::enable_if_t<std::is_base_of_v<winrt::Windows::Foundation::IInspectable, T>, holder<T>> hold(const T& t) { return holder<T>(t); }
    template <typename T>
    std::enable_if_t<!std::is_base_of_v<winrt::Windows::Foundation::IInspectable, T>, T> hold(const T& t) { return t; }
}

PYBIND11_DECLARE_HOLDER_TYPE(T, ::pywinui::holder<T>, true);
