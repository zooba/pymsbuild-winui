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
#include <winrt/Windows.ApplicationModel.Contacts.h>
#include <winrt/Windows.ApplicationModel.DataTransfer.h>
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
#include <winrt/Windows.UI.Xaml.Interop.h>  // for TypeName
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
    template <typename T>
    std::enable_if_t<std::is_base_of_v<winrt::Windows::Foundation::IUnknown, T>, T> init_value() { return nullptr; }
    template <typename T>
    std::enable_if_t<!std::is_base_of_v<winrt::Windows::Foundation::IUnknown, T>, T> init_value() { return T{}; }

    template <typename T> struct holder {
        struct inner { T obj{}; inner() : obj{init_value<T>()} {}; };
        ::std::unique_ptr<inner> _p;
        holder(T t) : _p{::std::make_unique<inner>()} { _p->obj = t; }
        holder(T *t) : _p{::std::make_unique<inner>()} { _p->obj = *t; }
        inline T *get() const { return &_p->obj; }
    };

    template <typename T>
    std::enable_if_t<std::is_base_of_v<winrt::Windows::Foundation::IUnknown, T>, holder<T>> hold(const T& t) { return holder<T>(t); }
    template <typename T>
    std::enable_if_t<!std::is_base_of_v<winrt::Windows::Foundation::IUnknown, T>, T> hold(const T& t) { return t; }

    template <typename F, typename R=typename std::invoke_result_t<F>>
    std::enable_if_t<!std::is_void_v<R> && !std::is_base_of_v<winrt::Windows::Foundation::IUnknown, R>, R> call_and_hold(F &&fn) { return std::invoke(std::forward<F>(fn)); }
    template <typename F, typename R=typename std::invoke_result_t<F>>
    std::enable_if_t<std::is_base_of_v<winrt::Windows::Foundation::IUnknown, R>, holder<R>> call_and_hold(F &&fn) { return holder<R>(std::invoke(std::forward<F>(fn))); }
    template <typename F, typename R=typename std::invoke_result_t<F>>
    std::enable_if_t<std::is_void_v<R>, void> call_and_hold(F &&fn) { std::invoke(std::forward<F>(fn)); }
}

PYBIND11_DECLARE_HOLDER_TYPE(T, ::pywinui::holder<T>, true);
