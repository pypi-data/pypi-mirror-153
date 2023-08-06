
#ifndef SCIPP_VARIABLE_EXPORT_H
#define SCIPP_VARIABLE_EXPORT_H

#ifdef SCIPP_VARIABLE_STATIC_DEFINE
#  define SCIPP_VARIABLE_EXPORT
#  define SCIPP_VARIABLE_NO_EXPORT
#else
#  ifndef SCIPP_VARIABLE_EXPORT
#    ifdef scipp_variable_EXPORTS
        /* We are building this library */
#      define SCIPP_VARIABLE_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define SCIPP_VARIABLE_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef SCIPP_VARIABLE_NO_EXPORT
#    define SCIPP_VARIABLE_NO_EXPORT 
#  endif
#endif

#ifndef SCIPP_VARIABLE_DEPRECATED
#  define SCIPP_VARIABLE_DEPRECATED __declspec(deprecated)
#endif

#ifndef SCIPP_VARIABLE_DEPRECATED_EXPORT
#  define SCIPP_VARIABLE_DEPRECATED_EXPORT SCIPP_VARIABLE_EXPORT SCIPP_VARIABLE_DEPRECATED
#endif

#ifndef SCIPP_VARIABLE_DEPRECATED_NO_EXPORT
#  define SCIPP_VARIABLE_DEPRECATED_NO_EXPORT SCIPP_VARIABLE_NO_EXPORT SCIPP_VARIABLE_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SCIPP_VARIABLE_NO_DEPRECATED
#    define SCIPP_VARIABLE_NO_DEPRECATED
#  endif
#endif

#endif /* SCIPP_VARIABLE_EXPORT_H */
