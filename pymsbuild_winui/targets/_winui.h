#pragma once

using namespace winrt;
using namespace Windows::Foundation;
namespace py = pybind11;

// Base template for converting between winrt and pybind11 types.
template <typename T, typename _enable=void> struct cvt {
    typedef T natural_t;        // the "real" type
    typedef const natural_t& cself_t;   // the type to expect when passed as "const self"
    typedef natural_t& self_t;  // the type to expect when passed as non-const "self"
    typedef typename T py_t;    // the type pybind11 knows how to convert to/from
    typedef typename const py_t& arg_t; // the type we should expect when pybind11 will call us
    typedef cvt<T> param_t;     // the type to assign parameter values to (usually ourselves)
    natural_t value;            // storage for the value
    cvt(arg_t t) : value(t) { }
    operator py_t () const { return value; }
    py_t ret() { return value; }    // function (as well as cast) works better for cvt_out()
    operator const natural_t & () const { return value; }
    cvt(py::object o) : value(py::cast<natural_t>(o)) { }
    operator py::object () const { return py::cast(value); }
    std::wstring repr() const { return (std::wstringstream() << "<" << typeid(natural_t).name() << ">").str(); }
};

// Specialisation for primitives
template <typename T> struct cvt<T,
    std::enable_if_t<std::is_integral_v<T> || std::is_floating_point_v<T> || std::is_function_v<T>
>> {
    typedef T natural_t, cself_t, self_t, py_t, arg_t, param_t;
    T value;
    cvt(T t) : value(t) { }
    py_t ret() { return value; }
    operator T () const { return value; }
    cvt(py::object o) : value(py::cast<natural_t>(o)) { }
    operator py::object () const { return py::cast(value); }
    std::wstring repr() const { return std::to_wstring(value); }
};

template <typename T> static std::wstring default_cpp_repr(const T &value) {
    return (std::wstringstream() << "<" << typeid(natural_t).name() << ">").str();
}

// defined in winui_Windows_Foundation.cpp
std::wstring default_winrt_repr(const IInspectable &value);

template <typename T> struct is_IReference : std::false_type {};
template <typename T> struct is_IReference<IReference<T>> : std::true_type {};

template <typename T> struct cvt<T, std::enable_if_t<
    std::is_base_of_v<Windows::Foundation::IInspectable, T> && !is_IReference<T>::value
>>  {
    typedef T natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef typename ::pywinui::holder<natural_t> py_t;
    typedef typename IInspectable arg_t;
    typedef cvt<T> param_t;
    natural_t value;
    cvt(arg_t t) : value(t.try_as<natural_t>()) { }
    cvt(py_t o) : value(!py::none().is(o) ? py::cast<natural_t>(o) : nullptr) { }
    operator natural_t () const { return value; }
    operator py_t () const { return py_t(value); }
    py_t ret() { return py_t(value); }
    std::wstring repr() { return default_winrt_repr(value); }
};

template <typename T> struct cvt<IReference<T>> {
    typedef T natural_t;
    typedef const IReference<natural_t>& cself_t;
    typedef IReference<natural_t>& self_t;
    typedef py::object py_t;
    typedef const py_t& arg_t;
    typedef cvt<IReference<T>> param_t;
    std::optional<natural_t> value;
    cvt(IInspectable o) : value(o.try_as<natural_t>()) { }
    cvt(arg_t o) : value(o ? std::make_optional<natural_t>(cvt<natural_t>(o)) : std::nullopt) { }
    operator IReference<natural_t> () const { return value ? std::move(winrt::box_value(*value).as<IReference<natural_t>>()) : nullptr; }
    operator py_t () const { return value ? cvt<natural_t>(*value) : py::none(); }
    py_t ret() { return (py_t)*this; }
    std::wstring repr() { return default_winrt_repr(value); }
};

template <> struct cvt<winrt::hstring> {
    typedef winrt::hstring natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef std::wstring py_t;
    typedef std::wstring_view arg_t;
    typedef winrt::hstring param_t;
    const winrt::hstring value;
    cvt(winrt::hstring o) : value{o} { }
    cvt(arg_t o) : value{o} {}
    operator winrt::hstring () const { return value; }
    operator std::wstring () const { return std::wstring { value }; }
    py_t ret() { return std::wstring { value }; }
    cvt(py::object o) : value(!py::none().is(o) ? py::cast<std::wstring>(o) : nullptr) { }
    operator py::object () const { return py::cast(std::wstring { value }); }
    std::wstring repr(); // defined in winui_Windows_Foundation.cpp
};

template <> struct cvt<Numerics::float2> {
    typedef Numerics::float2 natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef py::object py_t;
    typedef const py_t& arg_t;
    typedef cvt<Numerics::float2> param_t;
    natural_t value;
    cvt(natural_t o) : value(o) { }
    cvt(arg_t o) : value{ py::cast<float>(o[py::cast(0)]), py::cast<float>(o[py::cast(1)]) } { }
    operator natural_t () const { return value; }
    operator py_t () const { return py::make_tuple(value.x, value.y); }
    py_t ret() { return (py_t)*this; }
    std::wstring repr() const { return (std::wstringstream() << "Vector2(" << value.x << ", " << value.y << ")").str(); }
};

template <> struct cvt<Numerics::float3> {
    typedef Numerics::float3 natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef py::object py_t;
    typedef const py_t& arg_t;
    typedef cvt<Numerics::float3> param_t;
    natural_t value;
    cvt(natural_t o) : value(o) { }
    cvt(arg_t o) : value{ py::cast<float>(o[py::cast(0)]), py::cast<float>(o[py::cast(1)]), py::cast<float>(o[py::cast(2)]) } { }
    operator natural_t () const { return value; }
    operator py_t () const { return py::make_tuple(value.x, value.y, value.z); }
    py_t ret() { return (py_t)*this; }
    std::wstring repr() const { return (std::wstringstream() << "Vector3(" << value.x << ", " << value.y << ", " << value.z << ")").str(); }
};

template <> struct cvt<Numerics::float4> {
    typedef Numerics::float4 natural_t;
    typedef const natural_t& cself_t;
    typedef natural_t& self_t;
    typedef py::object py_t;
    typedef const py_t& arg_t;
    typedef cvt<Numerics::float4> param_t;
    natural_t value;
    cvt(natural_t o) : value(o) { }
    cvt(arg_t o) : value{ py::cast<float>(o[py::cast(0)]), py::cast<float>(o[py::cast(1)]), py::cast<float>(o[py::cast(2)]), py::cast<float>(o[py::cast(3)]) } { }
    operator natural_t () const { return value; }
    operator py_t () const { return py::make_tuple(value.x, value.y, value.z, value.w); }
    py_t ret() { return (py_t)*this; }
    std::wstring repr() const { return (std::wstringstream() << "Vector4(" << value.x << ", " << value.y << ", " << value.z << ", " << value.w << ")").str(); }
};


// Helper function for converting _into_ pybind11 recognisable values
template <typename T> auto cvt_out(T v) { return cvt<T>(v).ret(); }


// Used to static_assert that a method/function returns void
template <typename T> struct ensure_void {};
template <>           struct ensure_void<void> : std::true_type { };
template <>           struct ensure_void<void(void)> : std::true_type { };
template <>           struct ensure_void<void(void) const> : std::true_type { };

template <typename... Args> struct ensure_void<void(Args...)> : std::true_type { };
template <typename... Args> struct ensure_void<void(Args...) const> : std::true_type { };
template <typename... Args> struct ensure_void<void(*)(Args...)> : std::true_type { };

template <typename U, typename T> struct ensure_void<U T::*> : ensure_void<U> { };

// Used to static_assert that a callback/delegate type returns void
template <typename T>       struct ensure_Invoke_void { };
template <>                 struct ensure_Invoke_void<int32_t(*)(void) noexcept> : std::true_type { };
template <typename... Args> struct ensure_Invoke_void<int32_t(*)(Args...) noexcept> : std::true_type { };
template <typename... Args> struct ensure_Invoke_void<int32_t(*)(Args..., void**) noexcept> : std::false_type { };


// Concrete lambda for IAsyncOperation completions
template <typename OpResult>
struct asyncop_completer {
    asyncop_completer(py::object handler) : handler(handler) { }
    py::object handler;

    void operator() (typename cvt<IAsyncOperation<OpResult>>::cself_t sender, AsyncStatus) {
        py::gil_scoped_acquire _gil;
        try {
            handler(cvt_out<OpResult>(sender.GetResults()));
        } catch (py::error_already_set &eas) {
            eas.discard_as_unraisable(__func__);
        } catch (const std::exception &) {
            DebugBreak();
        }
    }
};


// Concrete lambda for event handlers
template <typename Sender, typename EventArgs>
struct event_handler {
    event_handler(py::object handler) : handler(handler) { }
    py::object handler;

    void operator() (typename cvt<Sender>::cself_t sender, typename cvt<EventArgs>::cself_t args) {
        py::gil_scoped_acquire _gil;
        try {
            handler(cvt_out<Sender>(sender), cvt_out<EventArgs>(args));
        } catch (py::error_already_set& eas) {
            eas.discard_as_unraisable(__func__);
        } catch (const std::exception&) {
            DebugBreak();
        }
    };
};


// Include generated type conversions
#include "_winui_converters.h"
