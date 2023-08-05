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

#include <funchook.h>

#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

/*
 * Concat:
 *
 * Combines two strings into a new string
 *
 * Source: Origin/Self
 * Target: Return
 * Action: Append
 */

void (*unicode_append_orig)(PyObject **l, PyObject *r);
binaryfunc unicode_concat_orig;
binaryfunc bytes_concat_orig;
binaryfunc bytearray_concat_orig;
binaryfunc bytearray_iconcat_orig;

void unicode_append_new(PyObject **l, PyObject *r) {
    PyObject *orig_l = *l;
    Py_XINCREF(orig_l);

    unicode_append_orig(l, r);

    if (*l == NULL)
        goto cleanup_and_return;

    propagate_concat(orig_l, r, *l, "propagate_unicode_concat");

cleanup_and_return:
    Py_XDECREF(orig_l);
}

PyObject *unicode_concat_new(PyObject *l, PyObject *r) {
    PyObject *result = unicode_concat_orig(l, r);

    if (result == NULL)
        return result;

    propagate_concat(l, r, result, "propagate_unicode_concat");

    return result;
}

PyObject *bytes_concat_new(PyObject *l, PyObject *r) {
    PyObject *result = bytes_concat_orig(l, r);

    if (result == NULL)
        return result;

    propagate_concat(l, r, result, "propagate_bytes_concat");

    return result;
}

PyObject *bytearray_concat_new(PyObject *l, PyObject *r) {
    PyObject *result = bytearray_concat_orig(l, r);

    if (result == NULL)
        return result;

    propagate_concat(l, r, result, "propagate_bytearray_concat");

    return result;
}

/* in-place concatenation */
PyObject *bytearray_iconcat_new(PyObject *self, PyObject *other) {
    PyObject *result = bytearray_iconcat_orig(self, other);

    if (result == NULL)
        return result;

    propagate_concat(self, other, result, "propagate_bytearray_concat");

    return result;
}

int apply_cat_patch(funchook_t *funchook) {
    unicode_append_orig = PyUnicode_Append;
    unicode_concat_orig = PyUnicode_Concat;
    bytes_concat_orig = PyBytes_Type.tp_as_sequence->sq_concat;
    bytearray_concat_orig = PyByteArray_Concat;
    bytearray_iconcat_orig = PyByteArray_Type.tp_as_sequence->sq_inplace_concat;

    funchook_prep_wrapper(funchook, &unicode_append_orig, unicode_append_new);
    funchook_prep_wrapper(funchook, &unicode_concat_orig, unicode_concat_new);
    funchook_prep_wrapper(funchook, &bytes_concat_orig, bytes_concat_new);
    funchook_prep_wrapper(funchook, &bytearray_concat_orig, bytearray_concat_new);
    funchook_prep_wrapper(funchook, &bytearray_iconcat_orig, bytearray_iconcat_new);

    return 0;
}
