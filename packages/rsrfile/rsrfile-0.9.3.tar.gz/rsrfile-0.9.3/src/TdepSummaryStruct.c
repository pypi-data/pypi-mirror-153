#include "TdepSummaryStruct.h"

PyTypeObject TdepSummaryType;

static PyStructSequence_Field TdepSummaryType_fields[] = {
    {"DateTime", "Date and time of creation"},
    {"CalcType", "Calculation type, Q, Q(T), F, F(T), W, W(T)"},
    {"Time", ""},
    {"Time1", ""},
    {"Time2", ""},
    {"LMax", ""},
    {"AbsCutOff", "Absolute cutoff"},
    {"TimePrs", ""},
    {"QMean", ""},
    {"QMax", ""},
    {"WMean", ""},
    {"WMax", ""},
    {"LMean", ""},
    {"FMax", ""},
    {"EMax", ""},
    {"RunTimeTot", "Calculation execution time"},
    {
        NULL,
    },
};

PyStructSequence_Desc TdepSummaryType_desc = {
    "TdepSummaryStruct",       /* name */
    "Time-dependent analysis", /* doc */
    TdepSummaryType_fields,
    16};

PyObject *create_TdepSummary(TdepSummaryStruct *tdep_struct)
{
    PyObject *tdep = PyStructSequence_New(&TdepSummaryType);

    PyObject *dt = DateTimeFromString(tdep_struct->DateTime);
    PyStructSequence_SetItem(tdep, 0, dt);
    // PyStructSequence_SetItem(tdep, 0, Py_BuildValue("s#", tdep_struct->DateTime, 19));

    PyStructSequence_SetItem(tdep, 1, Py_BuildValue("h", tdep_struct->CalcType));
    PyStructSequence_SetItem(tdep, 2, Py_BuildValue("d", tdep_struct->Time));
    PyStructSequence_SetItem(tdep, 3, Py_BuildValue("d", tdep_struct->Time1));
    PyStructSequence_SetItem(tdep, 4, Py_BuildValue("d", tdep_struct->Time2));
    PyStructSequence_SetItem(tdep, 5, Py_BuildValue("d", tdep_struct->LMax));
    PyStructSequence_SetItem(tdep, 6, Py_BuildValue("d", tdep_struct->AbsCutOff));
    PyStructSequence_SetItem(tdep, 7, Py_BuildValue("i", tdep_struct->TimePts));
    PyStructSequence_SetItem(tdep, 8, Py_BuildValue("d", tdep_struct->QMean));
    PyStructSequence_SetItem(tdep, 9, Py_BuildValue("d", tdep_struct->QMax));
    PyStructSequence_SetItem(tdep, 10, Py_BuildValue("d", tdep_struct->WMean));
    PyStructSequence_SetItem(tdep, 11, Py_BuildValue("d", tdep_struct->WMax));
    PyStructSequence_SetItem(tdep, 12, Py_BuildValue("d", tdep_struct->LMean));
    PyStructSequence_SetItem(tdep, 13, Py_BuildValue("d", tdep_struct->FMax));
    PyStructSequence_SetItem(tdep, 14, Py_BuildValue("d", tdep_struct->EMax));
    PyStructSequence_SetItem(tdep, 15, Py_BuildValue("d", tdep_struct->RunTimeTot));
    return tdep;
}