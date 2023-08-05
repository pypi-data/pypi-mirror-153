#include "UNCSummaryStruct.h"

PyTypeObject UNCSummaryType;

static PyStructSequence_Field UNCSummaryType_fields[] = {
    {"DateTime", "Date and time of creation"},
    {"CalcType", "Calculation type, Q, Q(T), F, F(T), W, W(T)"},
    {"Time", ""},
    {"AbsCutOff", "Absolute cutoff"},
    {"Simulations", "Number of simulations to run"},
    {"SimType", "Uncertainty analysis based on parameter values or basic event probabilities"},
    {"Seed", "Seed value"},
    {"RngType", "Manual or random seed value"},
    {"Mean", "Point estimate of mean"},
    {"Median", "Point estimate of median "},
    {"f5th", "5th percentile"},
    {"f95th", "95th percentile"},
    {"RunTimeTot", "Calculation execution time"},
    {
        NULL,
    },
};

PyStructSequence_Desc UNCSummaryType_desc = {
    "UNCSummaryStruct",     /* name */
    "Uncertainty analysis", /* doc */
    UNCSummaryType_fields,
    13};

PyObject *DateTimeFromString(char *str);

PyObject *create_UNCSummary(UNCSummaryStruct *unc_struct)
{
    PyObject *UNCSummary_obj = PyStructSequence_New(&UNCSummaryType);

    PyObject *dt = DateTimeFromString(unc_struct->DateTime);
    PyStructSequence_SetItem(UNCSummary_obj, 0, dt);
    // PyStructSequence_SetItem(UNCSummary_obj, 0, Py_BuildValue("s#", unc_struct->DateTime, 19));

    PyStructSequence_SetItem(UNCSummary_obj, 1, Py_BuildValue("h", unc_struct->CalcType));
    PyStructSequence_SetItem(UNCSummary_obj, 2, Py_BuildValue("d", unc_struct->Time));
    PyStructSequence_SetItem(UNCSummary_obj, 3, Py_BuildValue("d", unc_struct->AbsCutOff));
    PyStructSequence_SetItem(UNCSummary_obj, 4, Py_BuildValue("i", unc_struct->Simulations));
    PyStructSequence_SetItem(UNCSummary_obj, 5, Py_BuildValue("h", unc_struct->SimType));
    PyStructSequence_SetItem(UNCSummary_obj, 6, Py_BuildValue("h", unc_struct->Seed));
    PyStructSequence_SetItem(UNCSummary_obj, 7, Py_BuildValue("h", unc_struct->RndType));
    PyStructSequence_SetItem(UNCSummary_obj, 8, Py_BuildValue("d", unc_struct->Mean));
    PyStructSequence_SetItem(UNCSummary_obj, 9, Py_BuildValue("d", unc_struct->Median));
    PyStructSequence_SetItem(UNCSummary_obj, 10, Py_BuildValue("d", unc_struct->f5th));
    PyStructSequence_SetItem(UNCSummary_obj, 11, Py_BuildValue("d", unc_struct->f95th));
    PyStructSequence_SetItem(UNCSummary_obj, 12, Py_BuildValue("d", unc_struct->RunTimeTot));
    return UNCSummary_obj;
}