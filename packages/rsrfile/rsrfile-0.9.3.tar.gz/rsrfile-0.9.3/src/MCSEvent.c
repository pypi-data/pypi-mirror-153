#include "MCSEvent.h"

PyTypeObject MCSEventType;

PyStructSequence_Field MCSEventType_fields[] = {
    {"Mean", "Numerical value based on the reliability model and the parameters assigned to the event"},
    {"fW", ""},
    {
        NULL,
    },
};

PyStructSequence_Desc MCSEventType_desc = {
    "MCSEvent",  /* name */
    "MCSEvent struct", /* doc */
    MCSEventType_fields,
    2};

