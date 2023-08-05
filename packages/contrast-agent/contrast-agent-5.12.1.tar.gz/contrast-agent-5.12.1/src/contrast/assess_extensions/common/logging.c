/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <funchook.h>

#include <contrast/assess/logging.h>

#define CONTRAST_MODULE_STR "contrast.assess_extensions"
#define CONTRAST_LOGGER_STR "logger"
#define CONTRAST_LOG_METHOD_STR "log"

#define stderr_msg(msg) fprintf(stderr, msg)

static PyObject *logger = NULL;
static const char *log_level_map[] = {
    "info",
    "warning",
    "error",
    "critical",
    "debug",
};

void set_logger(PyObject *_logger) {
    Py_XINCREF(_logger);
    logger = _logger;
}

void teardown_logger() {
    Py_XDECREF(logger);
    logger = NULL;
}

void log_message_at_level(log_level_t level, const char *msg, ...) {
    PyObject *string = NULL;
    PyObject *result = NULL;
    va_list argptr;

    if (logger == NULL) {
        return;
    }

    va_start(argptr, msg);

    string = PyUnicode_FromFormatV(msg, argptr);

    va_end(argptr);

    if (string == NULL) {
        stderr_msg("Failed to format log message\n");
        return;
    }

    result = PyObject_CallMethod(logger, (char *)log_level_map[level], "O", string);
    if (result == NULL) {
        stderr_msg("Failed to call log method\n");
    }
}
