/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/propagate.h>
#include <contrast/assess/utils.h>

/* we need these really ugly method names for automatic hook-specific propagator
   generation to work properly */

unaryfunc bytes___repr___orig;
unaryfunc unicode___repr___orig;
unaryfunc bytearray___repr___orig;
HOOK_UNARYFUNC(bytes___repr__);
HOOK_UNARYFUNC(unicode___repr__);
HOOK_UNARYFUNC(bytearray___repr__);

int apply_repr_patches(funchook_t *funchook) {
    bytes___repr___orig = PyBytes_Type.tp_repr;
    unicode___repr___orig = PyUnicode_Type.tp_repr;
    bytearray___repr___orig = PyByteArray_Type.tp_repr;

    funchook_prep_wrapper(funchook, &bytes___repr___orig, bytes___repr___new);
    funchook_prep_wrapper(funchook, &unicode___repr___orig, unicode___repr___new);
    funchook_prep_wrapper(funchook, &bytearray___repr___orig, bytearray___repr___new);

    return 0;
}
