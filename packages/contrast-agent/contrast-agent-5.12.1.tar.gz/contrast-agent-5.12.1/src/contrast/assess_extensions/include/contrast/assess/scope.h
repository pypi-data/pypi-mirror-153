/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_SCOPE_H_
#define _ASSESS_SCOPE_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <patchlevel.h>

typedef enum
{
    CONTRAST_SCOPE = 0,
    PROPAGATION_SCOPE,
    TRIGGER_SCOPE,
} ScopeLevel_t;

PyObject *set_exact_scope(PyObject *self, PyObject *args);
PyObject *enter_scope(PyObject *self, PyObject *args);
PyObject *exit_scope(PyObject *self, PyObject *args);
PyObject *in_scope(PyObject *self, PyObject *args);
PyObject *in_contrast_or_propagation_scope(PyObject *self, PyObject *args);
PyObject *get_current_scope(PyObject *, PyObject *);
PyObject *init_contrast_scope_cvars(PyObject *, PyObject *);

void enter_contrast_scope(void);
void exit_contrast_scope(void);
void enter_propagation_scope(void);
void exit_propagation_scope(void);
int should_propagate(void);

#endif /* _ASSESS_SCOPE_H_ */
