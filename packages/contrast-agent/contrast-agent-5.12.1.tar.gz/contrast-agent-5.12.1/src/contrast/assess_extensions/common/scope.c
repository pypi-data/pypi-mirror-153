/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/scope.h>

#define IN_SCOPE 1
#define NOT_IN_SCOPE 0

static PyObject *cvar_contrast_scope = NULL;
static PyObject *cvar_propagation_scope = NULL;
static PyObject *cvar_trigger_scope = NULL;

#define NUM_SCOPE_TYPES 3

/* We use these for comparisons and inc/dec operations on the current ContextVar value
 */
static PyObject *one = NULL;
static PyObject *zero = NULL;
static PyObject *negative_one = NULL;

#define NUM_STATIC_PY_INTS 3

/* init_contrast_scope_cvars sets PyErr_Format so we can return NULL here */
#define INIT_CVARS_RETURN_NULL_ON_FAILURE                                            \
    if (should_initialize_scope_cvars() && !init_contrast_scope_cvars(NULL, NULL)) { \
        return NULL;                                                                 \
    }

#define INIT_CVARS_RETURN_WITHOUT_VALUE_ON_FAILURE                                   \
    if (should_initialize_scope_cvars() && !init_contrast_scope_cvars(NULL, NULL)) { \
        return;                                                                      \
    }

/* Helper struct to initialize cvars */
typedef struct cvars {
    PyObject **cvar;
    char *name;
} contrast_cvar_t;

/* This struct is used as a helper to init all integer python object constants */
typedef struct int_constants {
    PyObject **int_obj;
    int val;
} int_constants_t;

static int cvar_in_scope(PyObject *cvar, const char *scope_name) {
    PyObject *current_scope = NULL;
    /* return NOT_IN_SCOPE by default */
    int in_scope = NOT_IN_SCOPE;

    if (cvar == NULL || scope_name == NULL) {
        return NOT_IN_SCOPE;
    }

    /* Return 0 on success whether or not a value was found */
    if (PyContextVar_Get(cvar, NULL, &current_scope) < 0) {
        log_error("Failed to get ContextVar value for %s", scope_name);
        return NOT_IN_SCOPE;
    }

    if (current_scope == NULL) {
        return NOT_IN_SCOPE;
    }

    in_scope = PyObject_RichCompareBool(current_scope, zero, Py_GT);

    Py_DECREF(current_scope);

    return in_scope == 1;
}

static inline int should_initialize_scope_cvars() {
    return (
        cvar_contrast_scope == NULL || cvar_propagation_scope == NULL ||
        cvar_trigger_scope == NULL);
}

PyObject *set_exact_scope(PyObject *self, PyObject *py_target_scope) {
    PyObject *token = NULL;
    PyObject *target_obj_value = NULL;
    int target_scopes[NUM_SCOPE_TYPES] = {NOT_IN_SCOPE, NOT_IN_SCOPE, NOT_IN_SCOPE};
    int i = 0;

    if (py_target_scope == Py_None || py_target_scope == NULL) {
        PyErr_Format(PyExc_RuntimeError, "'NoneType' is not a valid scope object");
        return NULL;
    }

    INIT_CVARS_RETURN_NULL_ON_FAILURE

    PyObject *cvars[NUM_SCOPE_TYPES] = {
        cvar_contrast_scope, cvar_propagation_scope, cvar_trigger_scope};

    if (!PyArg_ParseTuple(
            py_target_scope,
            "iii",
            &target_scopes[CONTRAST_SCOPE],
            &target_scopes[PROPAGATION_SCOPE],
            &target_scopes[TRIGGER_SCOPE])) {
        PyErr_Format(PyExc_RuntimeError, "Failed to parse storage args from tuple");
        return NULL;
    }

    for (i = 0; i < NUM_SCOPE_TYPES; i++) {
        token = NULL;
        target_obj_value = NULL;

        if (cvars[i] == NULL) {
            PyErr_Format(PyExc_RuntimeError, "Failed to set new scope");
            return NULL;
        }

        if ((target_obj_value = PyLong_FromLong(target_scopes[i])) == NULL) {
            PyErr_Format(
                PyExc_RuntimeError, "Failed to create new integer and set new scope");
            return NULL;
        }

        /* Returns a token object containing the previous value. We don't need it so
         * discard it in cleanup */
        token = PyContextVar_Set(cvars[i], target_obj_value);

        Py_XDECREF(token);
        Py_XDECREF(target_obj_value);

        if (token == NULL) {
            PyErr_Format(PyExc_RuntimeError, "Failed to set new scope");
            return NULL;
        }
    }

    Py_RETURN_NONE;
}

PyObject *init_contrast_scope_cvars(PyObject *unused, PyObject *unused2) {
    /*
       Initialize all 3 ContextVars and constant Python int objects.
    */

    int i = 0;
    char error_msg[64];

    int_constants_t int_constants[NUM_STATIC_PY_INTS] = {
        {&one, 1}, {&zero, 0}, {&negative_one, -1}};

    contrast_cvar_t init_cvar_arr[NUM_SCOPE_TYPES] = {
        {&cvar_contrast_scope, "Contrast Scope"},
        {&cvar_propagation_scope, "Propagation Scope"},
        {&cvar_trigger_scope, "Trigger Scope"}};

    /* Initialize our constant python int objects */
    for (i = 0; i < NUM_STATIC_PY_INTS; i++) {
        if (*int_constants[i].int_obj == NULL) {
            if ((*int_constants[i].int_obj = PyLong_FromLong(int_constants[i].val)) ==
                NULL) {
                snprintf(
                    error_msg,
                    sizeof(error_msg) - 1,
                    "Failed to create new integer constant");
                goto error;
            }
        }
    }

    /* Initialize each ContextVar. Decided not to set a default value because we can
     * check for NULL when we get a ContextVar */
    for (i = 0; i < NUM_SCOPE_TYPES; i++) {
        if (*init_cvar_arr[i].cvar == NULL) {
            if ((*init_cvar_arr[i].cvar =
                     PyContextVar_New(init_cvar_arr[i].name, NULL)) == NULL) {
                snprintf(
                    error_msg,
                    sizeof(error_msg) - 1,
                    "Failed to create new ContextVar named %s",
                    init_cvar_arr[i].name);
                goto error;
            }
        }
    }

    Py_RETURN_NONE;

error:
    for (i = 0; i < NUM_SCOPE_TYPES; i++) {
        Py_CLEAR(*init_cvar_arr[i].cvar);
        *init_cvar_arr[i].cvar = NULL;
    }

    for (i = 0; i < NUM_STATIC_PY_INTS; i++) {
        Py_CLEAR(*int_constants[i].int_obj);
        *int_constants[i].int_obj = NULL;
    }

    PyErr_Format(PyExc_RuntimeError, error_msg);

    return NULL;
}

static int get_scope_as_int(PyObject *cvar) {
    PyObject *current_scope_obj = NULL;
    /* return NOT_IN_SCOPE by default */
    int scope = NOT_IN_SCOPE;

    if (cvar == NULL) {
        return NOT_IN_SCOPE;
    }

    /* Return 0 on success whether or not a value was found */
    if (PyContextVar_Get(cvar, NULL, &current_scope_obj) < 0) {
        log_error("Failed to get current scope object");
    }

    if (current_scope_obj != NULL) {
        scope = PyLong_AsLong(current_scope_obj);
        if (scope < 0) {
            scope = NOT_IN_SCOPE;

            if (PyErr_Occurred()) {
                log_error("Failed to get current scope as int");
                PyErr_Clear();
            }
        }
    }

    Py_XDECREF(current_scope_obj);

    return scope;
}

static void update_cvar_value(PyObject *cvar, int modifier) {
    PyObject *modifier_obj = zero;
    PyObject *old_value = NULL;
    PyObject *token = NULL;
    PyObject *new_value_obj = NULL;
    /* new_value isn't used if we have a valid (i.e scope >= 0) previously existing
     * value */
    int new_value = (modifier > 0) ? 1 : NOT_IN_SCOPE;
    int cmp_result = 0;

    if (cvar == NULL || one == NULL || zero == NULL || negative_one == NULL) {
        return;
    }

    /* Return 0 on success whether or not a value was found */
    if (PyContextVar_Get(cvar, NULL, &old_value) < 0) {
        log_error("Failed to get contextvar");
        goto cleanup;
    }

    if (old_value == NULL) {
        new_value_obj = PyLong_FromLong(new_value);
    } else {
        if (modifier > 0) {
            modifier_obj = one;
        } else if (modifier < 0) {
            modifier_obj = negative_one;
        }

        cmp_result = PyObject_RichCompareBool(old_value, zero, Py_LE);
        if (cmp_result == 1 || cmp_result == -1) {
            new_value_obj = PyLong_FromLong(new_value);
        } else {
            new_value_obj = PyNumber_Add(old_value, modifier_obj);
        }
    }

    if (new_value_obj) {
        /* Returns a token object containing the previous value. We don't need it so
         * discard it in cleanup */
        token = PyContextVar_Set(cvar, new_value_obj);
    }

cleanup:
    Py_XDECREF(old_value);
    Py_XDECREF(token);
    Py_XDECREF(new_value_obj);
}

static void modify_scope_by_id(ScopeLevel_t scope_id, int modifier) {
    switch (scope_id) {
        case CONTRAST_SCOPE:
            update_cvar_value(cvar_contrast_scope, modifier);
            break;
        case PROPAGATION_SCOPE:
            update_cvar_value(cvar_propagation_scope, modifier);
            break;
        case TRIGGER_SCOPE:
            update_cvar_value(cvar_trigger_scope, modifier);
            break;
    }
}

inline void enter_contrast_scope(void) {
    INIT_CVARS_RETURN_WITHOUT_VALUE_ON_FAILURE

    modify_scope_by_id(CONTRAST_SCOPE, 1);
}

inline void exit_contrast_scope(void) {
    INIT_CVARS_RETURN_WITHOUT_VALUE_ON_FAILURE

    modify_scope_by_id(CONTRAST_SCOPE, -1);
}

inline void enter_propagation_scope(void) {
    INIT_CVARS_RETURN_WITHOUT_VALUE_ON_FAILURE

    modify_scope_by_id(PROPAGATION_SCOPE, 1);
}

inline void exit_propagation_scope(void) {
    INIT_CVARS_RETURN_WITHOUT_VALUE_ON_FAILURE

    modify_scope_by_id(PROPAGATION_SCOPE, -1);
}

inline int should_propagate(void) {
    return !(
        get_scope_as_int(cvar_contrast_scope) ||
        get_scope_as_int(cvar_propagation_scope) ||
        get_scope_as_int(cvar_trigger_scope));
}

PyObject *enter_scope(PyObject *self, PyObject *args) {
    ScopeLevel_t scope_id;

    INIT_CVARS_RETURN_NULL_ON_FAILURE

    if (!PyArg_ParseTuple(args, "i", &scope_id)) {
        /* PyArg_ParseTuple sets PyErr */
        return NULL;
    }

    modify_scope_by_id(scope_id, 1);

    Py_RETURN_NONE;
}

PyObject *exit_scope(PyObject *self, PyObject *args) {
    ScopeLevel_t scope_id;

    INIT_CVARS_RETURN_NULL_ON_FAILURE

    if (!PyArg_ParseTuple(args, "i", &scope_id)) {
        /* PyArg_ParseTuple sets PyErr */
        return NULL;
    }

    modify_scope_by_id(scope_id, -1);

    Py_RETURN_NONE;
}

PyObject *in_scope(PyObject *self, PyObject *args) {
    ScopeLevel_t scope_id;

    if (!PyArg_ParseTuple(args, "i", &scope_id)) {
        /* PyArg_ParseTuple sets PyErr */
        return NULL;
    }

    INIT_CVARS_RETURN_NULL_ON_FAILURE

    switch (scope_id) {
        case CONTRAST_SCOPE:
            return PyBool_FromLong(cvar_in_scope(cvar_contrast_scope, "Contrast"));
        case PROPAGATION_SCOPE:
            return PyBool_FromLong(
                cvar_in_scope(cvar_propagation_scope, "Propagation"));
        case TRIGGER_SCOPE:
            return PyBool_FromLong(cvar_in_scope(cvar_trigger_scope, "Trigger"));
    }

    Py_RETURN_FALSE;
}

PyObject *in_contrast_or_propagation_scope(PyObject *self, PyObject *ignored) {
    INIT_CVARS_RETURN_NULL_ON_FAILURE

    return PyBool_FromLong(
        cvar_in_scope(cvar_contrast_scope, "Contrast") |
        cvar_in_scope(cvar_propagation_scope, "Propagation"));
}

PyObject *get_current_scope(PyObject *self, PyObject *ignored) {
    INIT_CVARS_RETURN_NULL_ON_FAILURE

    return Py_BuildValue(
        "(iii)",
        get_scope_as_int(cvar_contrast_scope),
        get_scope_as_int(cvar_propagation_scope),
        get_scope_as_int(cvar_trigger_scope));
}
