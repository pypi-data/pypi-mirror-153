
#ifndef SCIPP_UNITS_EXPORT_H
#define SCIPP_UNITS_EXPORT_H

#ifdef SCIPP_UNITS_STATIC_DEFINE
#  define SCIPP_UNITS_EXPORT
#  define SCIPP_UNITS_NO_EXPORT
#else
#  ifndef SCIPP_UNITS_EXPORT
#    ifdef scipp_units_EXPORTS
        /* We are building this library */
#      define SCIPP_UNITS_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define SCIPP_UNITS_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef SCIPP_UNITS_NO_EXPORT
#    define SCIPP_UNITS_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef SCIPP_UNITS_DEPRECATED
#  define SCIPP_UNITS_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef SCIPP_UNITS_DEPRECATED_EXPORT
#  define SCIPP_UNITS_DEPRECATED_EXPORT SCIPP_UNITS_EXPORT SCIPP_UNITS_DEPRECATED
#endif

#ifndef SCIPP_UNITS_DEPRECATED_NO_EXPORT
#  define SCIPP_UNITS_DEPRECATED_NO_EXPORT SCIPP_UNITS_NO_EXPORT SCIPP_UNITS_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SCIPP_UNITS_NO_DEPRECATED
#    define SCIPP_UNITS_NO_DEPRECATED
#  endif
#endif

#endif /* SCIPP_UNITS_EXPORT_H */
