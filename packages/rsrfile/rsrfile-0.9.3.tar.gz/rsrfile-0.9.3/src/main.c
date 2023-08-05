#include <Python.h>
#include <sys/mman.h>
#include <fcntl.h>

#include "RSRFile.h"

static PyObject *
builtin_open(PyObject *self, PyObject *args, PyObject *kwds)
{
    return PyObject_Call((PyObject *)&RSRFileType, args, kwds);
}

static PyMethodDef addList_funcs[] = {
    {"open", (PyCFunction)builtin_open, METH_VARARGS, "open file"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef rsrfile = {
    PyModuleDef_HEAD_INIT,
    "rsrfile",
    "Read RiskSpectrum PSA results bin-files",
    -1,
    addList_funcs};

static PyObject *m = NULL;

PyMODINIT_FUNC PyInit_rsrfile(void)
{
    m = PyModule_Create(&rsrfile);
    if (m == NULL)
    {
        return NULL;
    }

    PyDateTime_IMPORT;

    PyStructSequence_InitType(&LargeNumType, &LargeNumType_desc);
    PyStructSequence_InitType(&MCSSummaryType, &MCSSummaryType_desc);
    PyStructSequence_InitType(&UNCSummaryType, &UNCSummaryType_desc);
    PyStructSequence_InitType(&TdepSummaryType, &TdepSummaryType_desc);
    PyStructSequence_InitType(&ResSummaryMiscType, &ResSummaryMiscType_desc);

    PyStructSequence_InitType(&MCSEventType, &MCSEventType_desc);

    if (PyType_Ready(&RSRFileType) < 0)
    {
        return NULL;
    }

    Py_INCREF(&RSRFileType);
    if (PyModule_AddObject(m, "RSRFile", (PyObject *)&RSRFileType) < 0)
    {
        Py_DECREF(&RSRFileType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
