#include "LargeNumStruct.h"

PyTypeObject LargeNumType;

static PyStructSequence_Field LargeNumType_fields[] = {
    {"mantissa", "The part of a floating-point number which represents the significant digits of that number"},
    {"exp", "The magnitude of the number" },
    {NULL,},
};

PyStructSequence_Desc LargeNumType_desc = {
    "LargeNumStruct", /* name */
    "RiskSpectrum large number struct", /* doc */
    LargeNumType_fields,
    2
};

PyObject *create_LargeNum(LargeNumStruct *ln_struct)
{
    PyObject *num = PyStructSequence_New(&LargeNumType);
    PyStructSequence_SetItem(num, 0, PyFloat_FromDouble(ln_struct->Mantissa));
    PyStructSequence_SetItem(num, 1, Py_BuildValue("h", ln_struct->Exp));
    return num;
}