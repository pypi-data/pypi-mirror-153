/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <assert.h>
#include <ctype.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include <funchook.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

/*
 * Subscript:
 *
 * Returns a slice of a string
 *
 * Source: Origin/Self
 * Target: Return
 * Action: Keep
 */

#define HOOK_SUBSCRIPT(NAME)                                             \
    PyObject *NAME##_item_new(PyObject *a, PyObject *b) {                \
        PyObject *result;                                                \
                                                                         \
        enter_propagation_scope();                                       \
        result = NAME##_item_orig(a, b);                                 \
        exit_propagation_scope();                                        \
                                                                         \
        PyObject *args = PyTuple_Pack(1, b);                             \
                                                                         \
        /* Record input and result */                                    \
        if (result != NULL && !PyNumber_Check(result))                   \
            call_string_propagator(                                      \
                "propagate_" #NAME "_subscript", a, result, args, NULL); \
                                                                         \
        Py_XDECREF(args);                                                \
        return result;                                                   \
    }

#define HOOK_SLICE(NAME)                                                    \
    PyObject *NAME##_slice_new(PyObject *a, Py_ssize_t i1, Py_ssize_t i2) { \
        PyObject *result;                                                   \
                                                                            \
        enter_contrast_scope();                                             \
        result = NAME##_slice_orig(a, i1, i2);                              \
        exit_contrast_scope();                                              \
                                                                            \
        PyObject *slice = build_slice(a, i1, i2);                           \
                                                                            \
        PyObject *args = PyTuple_Pack(1, slice);                            \
                                                                            \
        /* Record input and result */                                       \
        if (result != NULL)                                                 \
            call_string_propagator(                                         \
                "propagate_" #NAME "_subscript", a, result, args, NULL);    \
                                                                            \
        Py_XDECREF(slice);                                                  \
        Py_XDECREF(args);                                                   \
                                                                            \
        return result;                                                      \
    }

binaryfunc unicode_item_orig;
binaryfunc bytes_item_orig;
binaryfunc bytearray_item_orig;
HOOK_SUBSCRIPT(unicode);
HOOK_SUBSCRIPT(bytes);
HOOK_SUBSCRIPT(bytearray);

/* apply our patches */
int apply_subscript_patch(funchook_t *funchook) {
    bytes_item_orig = PyBytes_Type.tp_as_mapping->mp_subscript;
    funchook_prep_wrapper(funchook, &bytes_item_orig, bytes_item_new);

    unicode_item_orig = PyUnicode_Type.tp_as_mapping->mp_subscript;
    funchook_prep_wrapper(funchook, &unicode_item_orig, unicode_item_new);

    bytearray_item_orig = PyByteArray_Type.tp_as_mapping->mp_subscript;
    funchook_prep_wrapper(funchook, &bytearray_item_orig, bytearray_item_new);

    return 0;
}
