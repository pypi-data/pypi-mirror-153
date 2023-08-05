/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

#define ADD_ATTRIBUTE(TYPEOBJ, NAME, VALUE)                               \
    do {                                                                  \
        if (PyDict_SetItemString((typeobj)->tp_dict, NAME, VALUE) != 0) { \
            log_error("Failed to add %s attribute", NAME);                \
            return 1;                                                     \
        }                                                                 \
    } while (0)

/* Add contrast attributes to string object */
static int add_attributes(PyTypeObject *typeobj) {
    ADD_ATTRIBUTE(typeobj, "cs__tracked", Py_False);
    ADD_ATTRIBUTE(typeobj, "cs__source", Py_False);
    ADD_ATTRIBUTE(typeobj, "cs__properties", Py_None);
    ADD_ATTRIBUTE(typeobj, "cs__source_event", Py_None);
    ADD_ATTRIBUTE(typeobj, "cs__source_type", Py_None);
    ADD_ATTRIBUTE(typeobj, "cs__source_tags", Py_None);

    PyType_Modified(typeobj);
    return 0;
}

#define HANDLE_PATCHING_EXCEPTION(MSG) \
    do {                               \
        log_error(MSG);                \
        retcode = 1;                   \
        goto cleanup_and_exit;         \
    } while (0)

#undef funchook_prep_wrapper
#define funchook_prep_wrapper(fh, oldf, newf)                          \
    do {                                                               \
        if (funchook_prepare((fh), (void **)(oldf), (void *)(newf)) != \
            FUNCHOOK_ERROR_SUCCESS) {                                  \
            log_exception(                                             \
                PyExc_RuntimeError,                                    \
                "failed to prepare hook at %s:%d: %s",                 \
                __FILE__,                                              \
                __LINE__,                                              \
                funchook_error_message(fh));                           \
            retcode = 1;                                               \
            goto cleanup_and_exit;                                     \
        }                                                              \
    } while (0)

#define STREAM_INIT(NAME)                                                   \
    int NAME##_init_new(PyObject *self, PyObject *args, PyObject *kwargs) { \
        int retval;                                                         \
                                                                            \
        /* Call the original init function */                               \
        if ((retval = NAME##_init_orig(self, args, kwargs)) != 0)           \
            goto cleanup_and_exit;                                          \
                                                                            \
        /* Safety check for args before we proceed */                       \
        if (args == NULL || !PySequence_Check(args))                        \
            goto cleanup_and_exit;                                          \
                                                                            \
        /* Create a source event for stream.__init__ */                     \
        create_stream_source_event(self, args, kwargs);                     \
                                                                            \
    cleanup_and_exit:                                                       \
        return retval;                                                      \
    }

static int (*stringio_init_orig)(PyObject *, PyObject *, PyObject *);
static int (*bytesio_init_orig)(PyObject *, PyObject *, PyObject *);
STREAM_INIT(stringio);
STREAM_INIT(bytesio);

int apply_stream_patches(funchook_t *funchook) {
    PyObject *io_module = NULL;
    PyTypeObject *StringIOType = NULL;
    PyTypeObject *BytesIOType = NULL;
    PyTypeObject *IOBaseType = NULL;
    int retcode = 0;

    if ((io_module = PyImport_ImportModule("_io")) == NULL) {
        HANDLE_PATCHING_EXCEPTION("Failed to import io module");
    }

    if ((StringIOType =
             (PyTypeObject *)PyObject_GetAttrString(io_module, "StringIO")) == NULL) {
        HANDLE_PATCHING_EXCEPTION("Failed to get StringIO type");
    }

    if ((BytesIOType = (PyTypeObject *)PyObject_GetAttrString(io_module, "BytesIO")) ==
        NULL) {
        HANDLE_PATCHING_EXCEPTION("Failed to get BytesIO type");
    }

    if ((IOBaseType = (PyTypeObject *)PyObject_GetAttrString(io_module, "_IOBase")) ==
        NULL) {
        HANDLE_PATCHING_EXCEPTION("Failed to get _io._IOBase type");
    }

    if ((retcode = add_attributes(StringIOType)) != 0) {
        log_error("Failed to add attributes to io.StringIO class");
        goto cleanup_and_exit;
    }

    if ((retcode = add_attributes(BytesIOType)) != 0) {
        log_error("Failed to add attributes to io.BytesIO class");
        goto cleanup_and_exit;
    }

    stringio_init_orig = StringIOType->tp_init;
    bytesio_init_orig = BytesIOType->tp_init;

    funchook_prep_wrapper(funchook, &stringio_init_orig, &stringio_init_new);
    funchook_prep_wrapper(funchook, &bytesio_init_orig, &bytesio_init_new);

    if ((retcode = patch_stringio_methods(funchook, StringIOType)) != 0)
        goto cleanup_and_exit;

    if ((retcode = patch_bytesio_methods(funchook, BytesIOType)) != 0)
        goto cleanup_and_exit;

    if ((retcode = patch_iobase_methods(funchook, IOBaseType)) != 0)
        goto cleanup_and_exit;

cleanup_and_exit:
    Py_XDECREF(io_module);
    Py_XDECREF(StringIOType);
    Py_XDECREF(BytesIOType);
    Py_XDECREF(IOBaseType);
    return retcode;
}
