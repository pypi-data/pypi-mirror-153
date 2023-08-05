/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

#define IS_TRACKABLE(X) \
    (PyUnicode_Check((X)) || PyBytes_Check((X)) || PyByteArray_Check((X)))

newfunc unicode_new_orig;
newfunc bytes_new_orig;
initproc bytearray_init_orig;

PyObject *bytes_new_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *result = bytes_new_orig(type, args, kwds);

    if (result == NULL)
        return result;

    call_string_propagator("propagate_bytes_cast", NULL, result, args, kwds);

    return result;
}

int bytearray_init_new(PyObject *self, PyObject *args, PyObject *kwds) {
    int result = bytearray_init_orig(self, args, kwds);

    if (result == -1)
        return result;

    /* Here we report self_obj=None and ret=self
       to maintain the illusion of casting */
    call_string_propagator("propagate_bytearray_cast", NULL, self, args, kwds);

    return result;
}

PyObject *unicode_new_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *result = unicode_new_orig(type, args, kwds);

    if (result == NULL)
        return result;

    call_string_propagator("propagate_unicode_cast", NULL, result, args, kwds);

    return result;
}

int apply_cast_patches(funchook_t *funchook) {
    ADD_NEWFUNC_HOOK(PyUnicode_Type, unicode_new);
    ADD_NEWFUNC_HOOK(PyBytes_Type, bytes_new);
    ADD_INITPROC_HOOK(PyByteArray_Type, bytearray_init);

    return 0;
}
