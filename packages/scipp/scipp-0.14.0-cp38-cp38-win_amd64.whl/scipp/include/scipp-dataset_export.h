
#ifndef SCIPP_DATASET_EXPORT_H
#define SCIPP_DATASET_EXPORT_H

#ifdef SCIPP_DATASET_STATIC_DEFINE
#  define SCIPP_DATASET_EXPORT
#  define SCIPP_DATASET_NO_EXPORT
#else
#  ifndef SCIPP_DATASET_EXPORT
#    ifdef scipp_dataset_EXPORTS
        /* We are building this library */
#      define SCIPP_DATASET_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define SCIPP_DATASET_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef SCIPP_DATASET_NO_EXPORT
#    define SCIPP_DATASET_NO_EXPORT 
#  endif
#endif

#ifndef SCIPP_DATASET_DEPRECATED
#  define SCIPP_DATASET_DEPRECATED __declspec(deprecated)
#endif

#ifndef SCIPP_DATASET_DEPRECATED_EXPORT
#  define SCIPP_DATASET_DEPRECATED_EXPORT SCIPP_DATASET_EXPORT SCIPP_DATASET_DEPRECATED
#endif

#ifndef SCIPP_DATASET_DEPRECATED_NO_EXPORT
#  define SCIPP_DATASET_DEPRECATED_NO_EXPORT SCIPP_DATASET_NO_EXPORT SCIPP_DATASET_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SCIPP_DATASET_NO_DEPRECATED
#    define SCIPP_DATASET_NO_DEPRECATED
#  endif
#endif

#endif /* SCIPP_DATASET_EXPORT_H */
