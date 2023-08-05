/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>

#define CONTRAST_MODULE_NAME "contrast"
#define STRING_TRACKER_NAME "STRING_TRACKER"
#define TRACK_METHOD_NAME "track"

#define POLICY_MODULE_NAME "contrast.agent.assess.policy.string_propagation"
#define PROPAGATE_NAME "propagate"

static PyObject *string_tracker = NULL;
static PyObject *policy_module = NULL;

int init_propagate() {
    int retcode = -1;

    if ((retcode = init_string_tracker()) < 0) {
        return retcode;
    }

    if ((retcode = init_propagation()) < 0) {
        return retcode;
    }

    return retcode;
}

int init_string_tracker() {
    PyObject *contrast_module = NULL;
    int retcode = -1;

    if (string_tracker != NULL) {
        log_exception(PyExc_RuntimeError, "string_tracker already initialized");
        goto cleanup_and_exit;
    }

    contrast_module = PyImport_ImportModule(CONTRAST_MODULE_NAME);
    if (contrast_module == NULL) {
        log_error("failed to import %s", CONTRAST_MODULE_NAME);
        goto cleanup_and_exit;
    }

    log_debug("imported contrast module %s", CONTRAST_MODULE_NAME);

    string_tracker = PyObject_GetAttrString(contrast_module, STRING_TRACKER_NAME);
    if (string_tracker == NULL) {
        log_error("failed to get %s object", STRING_TRACKER_NAME);
        goto cleanup_and_exit;
    }

    log_debug("got %s object", STRING_TRACKER_NAME);
    retcode = 0;

cleanup_and_exit:
    Py_XDECREF(contrast_module);
    return retcode;
}

int init_propagation() {
    if (policy_module != NULL) {
        log_exception(PyExc_RuntimeError, "policy module already initialized");
        return -1;
    }

    policy_module = PyImport_ImportModule(POLICY_MODULE_NAME);
    if (policy_module == NULL) {
        log_error("failed to import %s", POLICY_MODULE_NAME);
        return -1;
    }

    log_debug("imported propagation_policy module %s", POLICY_MODULE_NAME);
    return 0;
}

void teardown_propagate() {
    Py_XDECREF(string_tracker);
    Py_XDECREF(policy_module);
    string_tracker = NULL;
    policy_module = NULL;
}

inline int is_tracked(PyObject *source) {
    if (source == NULL || string_tracker == NULL)
        return 0;

    /* Right now we are choosing to not check whether the input corresponds to
     * a unicode or string type, since if it does not, then we expect the dict
     * lookup to fail anyway. It doesn't seem like this should be a big
     * performance hit, but we can always change this in the future.
     */
    return PySequence_Contains(string_tracker, source);
}

static inline bool need_to_pack(PyObject *obj) {
    return (
        !PySequence_Check(obj) || PyBytes_Check(obj) || PyUnicode_Check(obj) ||
        PyByteArray_Check(obj));
}

void call_string_propagator(
    char *prop_method_name,
    PyObject *source,
    PyObject *newstr,
    PyObject *hook_args,
    PyObject *hook_kwargs) {
    PyObject *result;
    PyObject *prop_hook_args;
    int free_hook_args = 0;

    /* No Python API calls should happen in this function prior to this check */
    if (!should_propagate())
        return;

    enter_propagation_scope();
    enter_contrast_scope();

    if (hook_args == NULL) {
        prop_hook_args = Py_None;
    } else if (need_to_pack(hook_args)) {
        prop_hook_args = PyTuple_Pack(1, hook_args);
        free_hook_args = 1;
    } else {
        prop_hook_args = hook_args;
    }

    result = PyObject_CallMethod(
        policy_module,
        prop_method_name,
        "OOOOO",
        newstr,                              /* target */
        (source == NULL ? Py_None : source), /* self_obj */
        newstr,                              /* ret */
        /* args */
        prop_hook_args,
        /* kwargs */
        (hook_kwargs == NULL ? Py_None : hook_kwargs));

    if (result == NULL) {
        PyErr_PrintEx(0);
        log_error("failed to propagate: %s", prop_method_name);
    }

    exit_contrast_scope();
    exit_propagation_scope();

    Py_XDECREF(result);
    if (free_hook_args) {
        Py_XDECREF(prop_hook_args);
    }
}

static void call_propagate_stream(
    const char *event_name,
    PyObject *source,
    PyObject *newstr,
    PyObject *hook_args,
    PyObject *hook_kwargs) {
    PyObject *result;
    PyObject *prop_hook_args;
    int free_hook_args = 0;

    enter_contrast_scope();

    if (hook_args == NULL)
        prop_hook_args = Py_None;
    else if (need_to_pack(hook_args)) {
        prop_hook_args = PyTuple_Pack(1, hook_args);
        free_hook_args = 1;
    } else
        prop_hook_args = hook_args;

    /* def propagate(method_name, target, obj, ret, args, kwargs) */
    result = PyObject_CallMethod(
        policy_module,
        "propagate_stream",
        "sOOOOO",
        event_name,                          /* method_name */
        newstr,                              /* target */
        (source == NULL ? Py_None : source), /* self_obj */
        newstr,                              /* ret */
        /* args */
        prop_hook_args,
        /* kwargs */
        (hook_kwargs == NULL ? Py_None : hook_kwargs));

    if (result == NULL) {
        PyErr_PrintEx(0);
        log_error("failed to propagate %s event", event_name);
    }

    exit_contrast_scope();
    Py_XDECREF(result);
    if (free_hook_args)
        Py_XDECREF(prop_hook_args);
}

void propagate_concat(PyObject *l, PyObject *r, PyObject *result, char *propagator) {
    PyObject *args;

    if (!should_propagate())
        return;

    if (PySequence_Length(result) < 2)
        return;

    if (!is_tracked(l) && !is_tracked(r))
        return;

    args = PyTuple_Pack(1, r);

    call_string_propagator(propagator, l, result, args, NULL);

    Py_XDECREF(args);
}

PyObject *propagate_repeat(
    ssizeargfunc orig_repeat, PyObject *self, Py_ssize_t n, char *propagator) {
    PyObject *args;

    PyObject *result = orig_repeat(self, n);

    if (result == NULL)
        return result;

    args = Py_BuildValue("(n)", n);

    call_string_propagator(propagator, self, result, args, Py_None);

    Py_XDECREF(args);
    return result;
}

static int has_attr_and_true(PyObject *stream, const char *attrname) {
    PyObject *attr;
    int result;

    if (!PyObject_HasAttrString(stream, attrname))
        return 0;

    if ((attr = PyObject_GetAttrString(stream, attrname)) == NULL) {
        PyErr_Clear();
        return 0;
    }

    result = attr == Py_True;

    Py_DECREF(attr);
    return result;
}

static int stream_tracked(PyObject *stream) {
    if (has_attr_and_true(stream, "cs__tracked"))
        return 1;

    if (has_attr_and_true(stream, "cs__source"))
        return 1;

    return 0;
}

void propagate_stream(
    const char *event_name,
    PyObject *source,
    PyObject *result,
    PyObject *hook_args,
    PyObject *hook_kwargs) {

    if (!should_propagate())
        return;

    if (!stream_tracked(source))
        return;

    if (is_tracked(result))
        return;

    enter_propagation_scope();
    call_propagate_stream(event_name, source, result, hook_args, hook_kwargs);
    exit_propagation_scope();
}

void create_stream_source_event(PyObject *stream, PyObject *args, PyObject *kwargs) {
    PyObject *result;

    if (!should_propagate())
        return;

    enter_contrast_scope();

    result = PyObject_CallMethod(
        policy_module,
        "create_stream_source_event",
        "OOO",
        stream,
        (args == NULL ? Py_None : args),
        (kwargs == NULL ? Py_None : kwargs));
    if (result == NULL) {
        PyErr_PrintEx(0);
        log_error("failed to create stream init event");
    }

    exit_contrast_scope();

    Py_XDECREF(result);
}
