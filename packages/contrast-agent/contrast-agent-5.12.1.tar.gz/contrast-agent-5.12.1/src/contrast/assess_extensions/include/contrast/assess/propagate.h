/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_PROPAGATE_H_
#define _ASSESS_PROPAGATE_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>

int init_propagate(void);
int init_string_tracker(void);
int init_propagation(void);
void teardown_propagate(void);
int is_tracked(PyObject *source);
void call_string_propagator(
    char *prop_method_name,
    PyObject *source,
    PyObject *newstr,
    PyObject *hook_args,
    PyObject *hook_kwargs);
void propagate_concat(PyObject *l, PyObject *r, PyObject *result, char *propagator);
PyObject *propagate_repeat(
    ssizeargfunc orig_repeat, PyObject *self, Py_ssize_t n, char *propagator);
void propagate_stream(
    const char *event_name,
    PyObject *source,
    PyObject *result,
    PyObject *hook_args,
    PyObject *hook_kwargs);
void create_stream_source_event(PyObject *s, PyObject *args, PyObject *kwargs);
#if PY_MAJOR_VERSION < 3
void apply_exec_hook(const char *str);
#endif

#endif /* _ASSESS_PROPAGATE_H_ */
