#include "ResSummaryMiscStruct.h"
#include "common.h"
#include "structures.h"

PyTypeObject ResSummaryMiscType;

static PyStructSequence_Field ResSummaryMiscType_fields[] = {
    {"iDummy", ""},
    {"fDummy", ""},
    {"cDummy", ""},
    {
        NULL,
    },
};

PyStructSequence_Desc ResSummaryMiscType_desc = {
    "ResSummaryMiscStruct",  /* name */
    "ResSummaryMisc struct", /* doc */
    ResSummaryMiscType_fields,
    3};

PyObject *create_ResSummaryMisc(ResSummaryMiscStruct *misc_struct)
{
    PyObject *misc_obj = PyStructSequence_New(&ResSummaryMiscType);

    /* iDummy */
    PyObject *iDummy_obj = PyTuple_New(10);
    for (int i = 0; i < 10; i++)
    {
        PyTuple_SET_ITEM(iDummy_obj, i,
                         Py_BuildValue("i", misc_struct->iDummy[i]));
    }
    PyStructSequence_SetItem(misc_obj, 0, iDummy_obj);

    /* fDummy */
    PyObject *fDummy_obj = PyTuple_New(10);
    for (int i = 0; i < 10; i++)
    {
        PyTuple_SET_ITEM(fDummy_obj, i,
                         Py_BuildValue("d", misc_struct->fDummy[i]));
    }
    PyStructSequence_SetItem(misc_obj, 1, fDummy_obj);

    /* cDummy */
    PyObject *cDummy_obj = PyTuple_New(10);
    for (int i = 0; i < 10; i++)
    {
        const size_t str_len = trim(misc_struct->cDummy[i], MAX_ID_LEN);
        PyTuple_SET_ITEM(cDummy_obj, i,
                         Py_BuildValue("s#", misc_struct->cDummy[i], str_len));
    }
    PyStructSequence_SetItem(misc_obj, 2, cDummy_obj);

    return misc_obj;
}