#include "common.h"

PyObject *DateTimeFromString(char *str)
{

    int year, month, day, hour, minute, second;
    const int micros = 0;
    if (sscanf(str, "%d-%d-%d %d:%d:%d",
               &year, &month, &day, &hour, &minute, &second) == EOF)
    {
        PyErr_SetString(PyExc_Exception, "datetime() error!");
        return NULL;
    }

    if (!PyDateTimeAPI)
    {
        PyDateTime_IMPORT;
    }

    PyObject *dt = PyDateTime_FromDateAndTime(year, month, day, hour, minute, second, micros);

    return dt;
}

const size_t trim(const char *str, size_t len)
{
    len--;
    while ((*(str + len) == ' ') || *(str + len) == (char)0)
    {
        len--;
    }
    return len + 1;
}