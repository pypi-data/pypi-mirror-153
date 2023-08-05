#include "ImpTable.h"

static const char *const long_header_labels[] = {
    "ID", "Type", "Value", "FV", "FC", "RDF", "RIF", "Sense", "SensHigh", "SensLow"};

static const char *const short_header_labels[] = {
    "ID", "FC", "RDF", "RIF", "Sense", "SensHigh", "SensLow"};

PyObject *create_BEImportanceTable(
    const ImpStruct *const imp_struct,
    const EventStruct *const event_struct,
    const BEEventStruct *const beevent_struct,
    const CCFEventStruct *const ccfevent_struct,
    const MODEventStruct *const modevent_struct,
    const uint_fast32_t count)
{

    PyObject *col_obj = PyTuple_New(count + 1);

    PyObject *header_obj = PyTuple_New(ARRAY_SIZE(long_header_labels));
    for (uint_fast8_t i = 0; i < ARRAY_SIZE(long_header_labels); i++)
    {
        PyTuple_SET_ITEM(header_obj, i, Py_BuildValue("s", long_header_labels[i]));
    }
    PyTuple_SET_ITEM(col_obj, 0, header_obj);

    for (uint_fast32_t i = 0; i < count; i++)
    {
        const uint32_t imp_index = imp_struct[i].Index;
        const uint32_t event_index = event_struct[imp_index].Index;
        const EventType event_type = event_struct[imp_index].EventType;

        const char *name;
        PyObject *row_obj = PyTuple_New(ARRAY_SIZE(long_header_labels));
        switch (event_type)
        {
        case BASIC_EVENT:
            name = beevent_struct[event_index].Name;
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "BE"));
            break;
        case CCF_EVENT:
            name = ccfevent_struct[event_index].Name;
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "CCF"));
            break;
        case MOD_EVENT:
            name = ccfevent_struct[event_index].Name;
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "MOD"));
            break;
        default: /* Error! */
            PyErr_SetString(PyExc_Exception, "Error. Can't read event id. Undefine event type");
            return NULL;
        }

        const size_t len = trim(name, MAX_ID_LEN);

        PyTuple_SET_ITEM(row_obj, 0, Py_BuildValue("s#", name, len));
        PyTuple_SET_ITEM(row_obj, 2, Py_BuildValue("d", imp_struct[i].Value));
        PyTuple_SET_ITEM(row_obj, 3, Py_BuildValue("d", imp_struct[i].FV));
        PyTuple_SET_ITEM(row_obj, 4, Py_BuildValue("d", imp_struct[i].FC));
        PyTuple_SET_ITEM(row_obj, 5, Py_BuildValue("d", imp_struct[i].RDF));
        PyTuple_SET_ITEM(row_obj, 6, Py_BuildValue("d", imp_struct[i].RIF));
        PyTuple_SET_ITEM(row_obj, 7, Py_BuildValue("d", imp_struct[i].Sens));
        PyTuple_SET_ITEM(row_obj, 8, Py_BuildValue("d", imp_struct[i].SensHigh));
        PyTuple_SET_ITEM(row_obj, 9, Py_BuildValue("d", imp_struct[i].SensLow));

        PyTuple_SET_ITEM(col_obj, i + 1, row_obj);
    }

    return col_obj;
}

PyObject *create_ParamImportanceTable(
    const ImpStruct *const imp_struct,
    const ParStruct *const param_struct,
    const uint_fast32_t count)
{
    PyObject *col_obj = PyTuple_New(count + 1);

    PyObject *header_obj = PyTuple_New(ARRAY_SIZE(long_header_labels));
    for (uint_fast8_t i = 0; i < ARRAY_SIZE(long_header_labels); i++)
    {
        PyTuple_SET_ITEM(header_obj, i, Py_BuildValue("s", long_header_labels[i]));
    }

    PyTuple_SET_ITEM(col_obj, 0, header_obj);

    for (uint_fast32_t i = 0; i < count; i++)
    {
        const uint32_t imp_index = imp_struct[i].Index;
        const uint32_t param_index = param_struct[imp_index].Index;

        const char *const name = param_struct[imp_index].Name;
        const size_t len = trim(name, MAX_ID_LEN);

        PyObject *row_obj = PyTuple_New(ARRAY_SIZE(long_header_labels));
        PyTuple_SET_ITEM(row_obj, 0, Py_BuildValue("s#", name, len));

        const ParamType param_type = param_struct[imp_index].PARType;

        switch (param_type)
        {
        case PROBABILITY:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "P"));
            break;
        case FAILURE_RATE:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "FR"));
            break;
        case FREQUENCY:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "F"));
            break;
        case TEST_INTERVAL:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "TI"));
            break;
        case MISSION_TIME:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "TM"));
            break;
        case ALPHA:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "CCFG"));
            break;
        default:
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("s", "UNDEFINE"));
            break;
        }
        PyTuple_SET_ITEM(row_obj, 2, Py_BuildValue("d", imp_struct[i].Value));
        PyTuple_SET_ITEM(row_obj, 3, Py_BuildValue("d", imp_struct[i].FV));
        PyTuple_SET_ITEM(row_obj, 4, Py_BuildValue("d", imp_struct[i].FC));
        PyTuple_SET_ITEM(row_obj, 5, Py_BuildValue("d", imp_struct[i].RDF));
        PyTuple_SET_ITEM(row_obj, 6, Py_BuildValue("d", imp_struct[i].RIF));
        PyTuple_SET_ITEM(row_obj, 7, Py_BuildValue("d", imp_struct[i].Sens));
        PyTuple_SET_ITEM(row_obj, 8, Py_BuildValue("d", imp_struct[i].SensHigh));
        PyTuple_SET_ITEM(row_obj, 9, Py_BuildValue("d", imp_struct[i].SensLow));

        PyTuple_SET_ITEM(col_obj, i + 1, row_obj);
    }

    return col_obj;
}

PyObject *ccfg_importance_table(
    const ImpStruct *const imp_struct,
    const CCFGroupStruct *const ccfg_struct,
    const uint_fast32_t count)
{

    PyObject *col_obj = PyTuple_New(count + 1);

    PyObject *header_obj = PyTuple_New(ARRAY_SIZE(short_header_labels));
    for (uint_fast8_t i = 0; i < ARRAY_SIZE(short_header_labels); i++)
    {
        PyTuple_SET_ITEM(header_obj, i, Py_BuildValue("s", short_header_labels[i]));
    }
    PyTuple_SET_ITEM(col_obj, 0, header_obj);

    for (uint_fast32_t i = 0; i < count; i++)
    {
        const uint32_t imp_index = imp_struct[i].Index;
        const CCFGroupStruct ccfg = ccfg_struct[imp_index];

        const size_t len = trim(ccfg.Name, MAX_ID_LEN);

        PyObject *row_obj = PyTuple_New(ARRAY_SIZE(short_header_labels));

        PyTuple_SET_ITEM(row_obj, 0, Py_BuildValue("s#", ccfg.Name, len));
        PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("d", imp_struct[i].FC));
        PyTuple_SET_ITEM(row_obj, 2, Py_BuildValue("d", imp_struct[i].RDF));
        PyTuple_SET_ITEM(row_obj, 3, Py_BuildValue("d", imp_struct[i].RIF));
        PyTuple_SET_ITEM(row_obj, 4, Py_BuildValue("d", imp_struct[i].Sens));
        PyTuple_SET_ITEM(row_obj, 5, Py_BuildValue("d", imp_struct[i].SensHigh));
        PyTuple_SET_ITEM(row_obj, 6, Py_BuildValue("d", imp_struct[i].SensLow));

        PyTuple_SET_ITEM(col_obj, i + 1, row_obj);
    }

    return col_obj;
}

PyObject *attr_importance_table(
    const ImpStruct *const imp_struct,
    const AttributeStruct *const attr_struct,
    const uint_fast32_t count)
{

    PyObject *col_obj = PyTuple_New(count + 1);

    PyObject *header_obj = PyTuple_New(ARRAY_SIZE(short_header_labels));
    for (uint_fast8_t i = 0; i < ARRAY_SIZE(short_header_labels); i++)
    {
        PyTuple_SET_ITEM(header_obj, i, Py_BuildValue("s", short_header_labels[i]));
    }
    PyTuple_SET_ITEM(col_obj, 0, header_obj);

    for (uint_fast32_t i = 0; i < count; i++)
    {
        const ImpStruct imp = imp_struct[i];
        const AttributeStruct attr = attr_struct[imp.Index];

        const size_t len = trim(attr.Name, MAX_ID_LEN);
        PyObject *row_obj = PyTuple_New(ARRAY_SIZE(short_header_labels));

        PyTuple_SET_ITEM(row_obj, 0, Py_BuildValue("s#", attr.Name, len));
        PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("d", imp.FC));
        PyTuple_SET_ITEM(row_obj, 2, Py_BuildValue("d", imp.RDF));
        PyTuple_SET_ITEM(row_obj, 3, Py_BuildValue("d", imp.RIF));
        PyTuple_SET_ITEM(row_obj, 4, Py_BuildValue("d", imp.Sens));
        PyTuple_SET_ITEM(row_obj, 5, Py_BuildValue("d", imp.SensHigh));
        PyTuple_SET_ITEM(row_obj, 6, Py_BuildValue("d", imp.SensLow));

        PyTuple_SET_ITEM(col_obj, i + 1, row_obj);
    }

    return col_obj;
}