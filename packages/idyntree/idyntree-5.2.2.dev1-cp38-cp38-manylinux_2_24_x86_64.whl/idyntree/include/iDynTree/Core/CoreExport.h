
#ifndef IDYNTREE_CORE_EXPORT_H
#define IDYNTREE_CORE_EXPORT_H

#ifdef IDYNTREE_CORE_STATIC_DEFINE
#  define IDYNTREE_CORE_EXPORT
#  define IDYNTREE_CORE_NO_EXPORT
#else
#  ifndef IDYNTREE_CORE_EXPORT
#    ifdef idyntree_core_EXPORTS
        /* We are building this library */
#      define IDYNTREE_CORE_EXPORT 
#    else
        /* We are using this library */
#      define IDYNTREE_CORE_EXPORT 
#    endif
#  endif

#  ifndef IDYNTREE_CORE_NO_EXPORT
#    define IDYNTREE_CORE_NO_EXPORT 
#  endif
#endif

#ifndef IDYNTREE_CORE_DEPRECATED
#  define IDYNTREE_CORE_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef IDYNTREE_CORE_DEPRECATED_EXPORT
#  define IDYNTREE_CORE_DEPRECATED_EXPORT IDYNTREE_CORE_EXPORT IDYNTREE_CORE_DEPRECATED
#endif

#ifndef IDYNTREE_CORE_DEPRECATED_NO_EXPORT
#  define IDYNTREE_CORE_DEPRECATED_NO_EXPORT IDYNTREE_CORE_NO_EXPORT IDYNTREE_CORE_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef IDYNTREE_CORE_NO_DEPRECATED
#    define IDYNTREE_CORE_NO_DEPRECATED
#  endif
#endif

#endif /* IDYNTREE_CORE_EXPORT_H */
