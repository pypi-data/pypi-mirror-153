#include <Python.h>
#include <fcntl.h>

typedef struct 
{
    double Mantissa;
    uint32_t Exp;
}__attribute__ ((__packed__)) LargeNumStruct;

extern PyTypeObject LargeNumType;
extern PyStructSequence_Desc LargeNumType_desc;

PyObject *create_LargeNum(LargeNumStruct *ln_struct);