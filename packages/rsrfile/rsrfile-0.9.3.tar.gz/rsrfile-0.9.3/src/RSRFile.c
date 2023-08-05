#define PY_SSIZE_T_CLEAN
#include "structures.h"
//#include "rsrfile.h"

#include "RSRFile.h"

static PyObject *RSRFile_open(RSRFile *self, PyObject *args)
{
    char *path_to_file;
    char *mode = NULL;
    if (!PyArg_ParseTuple(args, "s|s", &path_to_file, &mode))
    {
        PyErr_SetString(PyExc_ValueError, "Error!");
        return NULL;
    }

    int f_mode = O_RDONLY;
    int m_mode = PROT_READ;

    if (mode != NULL)
    {
        switch (*mode)
        {
        case 'r':
            // f_mode = O_RDONLY;
            // m_mode = PROT_READ;
            break;
        case 'w':
            f_mode = O_RDWR;
            m_mode = PROT_READ | PROT_WRITE;
            break;
        default:
            PyErr_SetString(PyExc_ValueError, "Error open mode value!");
            return NULL;
        }
    }

    int fp;
    if ((fp = open(path_to_file, f_mode)) == -1)
    {
        PyErr_SetString(PyExc_FileNotFoundError, "Error!");
        return NULL;
    }

    struct stat fileInfo;
    if (stat(path_to_file, &fileInfo) == -1)
    {
        PyErr_SetString(PyExc_FileNotFoundError, "Error!");
        return NULL;
    }
    // PROT_READ | PROT_WRITE
    uint8_t *mapped = mmap(0, fileInfo.st_size, m_mode, MAP_PRIVATE, fp, 0);
    if (mapped == MAP_FAILED)
    {
        PyErr_SetString(PyExc_MemoryError, "mapped() error!");
        return NULL;
    }
    if (f_mode == O_RDONLY)
    {
        close(fp);
    }
    else
    {
        self->fp = fp;
    }
    self->file_size = fileInfo.st_size;
    self->mapped = mapped;

    Py_RETURN_NONE;
}

static PyObject *RSRFile_close(RSRFile *self)
{
    if (self->fp != NULL)
    {
        close(self->fp);
    }
    if (self->mapped != NULL)
    {
        if (munmap(self->mapped, self->file_size) == -1)
        {
            PyErr_SetString(PyExc_MemoryError, "munmap() error!");
            return NULL;
        }
    }
    Py_RETURN_NONE;
}

#define CHECK_NULL_DECREF(obj) \
    if (obj != NULL)           \
    Py_DECREF(obj)

static void RSRFile_dealloc(RSRFile *self)
{

    RSRFile_close(self);
    CHECK_NULL_DECREF(self->MCSSummary);
    CHECK_NULL_DECREF(self->UNCSummary);
    CHECK_NULL_DECREF(self->TimeDepSummary);
    CHECK_NULL_DECREF(self->ResSummaryMisc);
    CHECK_NULL_DECREF(self->BEImpTable);
    CHECK_NULL_DECREF(self->CCFGImpTable);
    CHECK_NULL_DECREF(self->ParamImpTable);
    CHECK_NULL_DECREF(self->AttrImpTable);
    CHECK_NULL_DECREF(self->CompImpTable);
    CHECK_NULL_DECREF(self->SysImpTable);
    CHECK_NULL_DECREF(self->EGImpTable);
    CHECK_NULL_DECREF(self->pdf);
    CHECK_NULL_DECREF(self->cdf);
    CHECK_NULL_DECREF(self->mcs);
    CHECK_NULL_DECREF(self->mod_mcs);
    CHECK_NULL_DECREF(self->Events);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *RSRFile_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    RSRFile *self;
    self = (RSRFile *)type->tp_alloc(type, 0);
    if (self != NULL)
    {
        self->MCSSummary = NULL;
        self->UNCSummary = NULL;
        self->TimeDepSummary = NULL;
        self->ResSummaryMisc = NULL;
        self->BEImpTable = NULL;
        self->CCFGImpTable = NULL;
        self->ParamImpTable = NULL;
        self->AttrImpTable = NULL;
        self->CompImpTable = NULL;
        self->SysImpTable = NULL;
        self->EGImpTable = NULL;
        self->pdf = NULL;
        self->cdf = NULL;
        self->mcs = NULL;
        self->mod_mcs = NULL;
        self->Events = NULL;
    }
    return (PyObject *)self;
}

static int RSRFile_init(RSRFile *self, PyObject *args, PyObject *kwds)
{

    RSRFile_open(self, args);
    if (PyErr_Occurred())
    {
        return -1;
    }
    uint16_t mResults = *(uint16_t *)self->mapped;
    if (mResults != 100)
    {
        PyErr_SetString(PyExc_Exception, "File format error");
        return -1;
    }
    self->headers = (AnFileHeaderStruct *)&self->mapped[2];

    return 0;
}

static PyObject *RSRFile_enter(RSRFile *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self);
    return (PyObject *)self;
}

static PyObject *RSRFile_exit(RSRFile *self, PyObject *args)
{
    RSRFile_close(self);

    Py_DECREF(self);
    Py_RETURN_NONE;
}

static PyMemberDef RSRFile_members[] = {
    {"filepath", T_STRING, offsetof(RSRFile, filepath), 0, "Path to file"},
    {"mode", T_CHAR, offsetof(RSRFile, mode), 0, "Access mode to file"},
    {NULL} /* Sentinel */
};

static PyObject *mcs_summary_get(RSRFile *self, void *closure)
{
    if (self->MCSSummary == NULL)
    {
        if (self->headers[MCSSUMMARY_OFFSET].Record != 0)
        {
            MCSSummaryStruct *const mcs_struct = (MCSSummaryStruct *)&self->mapped[self->headers[MCSSUMMARY_OFFSET].StartByte];
            PyObject *const result = create_MCSSummary(mcs_struct);
            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->MCSSummary = result;
        }
    }
    Py_INCREF(self->MCSSummary);
    return self->MCSSummary;
}

static PyObject *unc_summary_get(RSRFile *self, void *closure)
{
    if (self->UNCSummary == NULL)
    {
        if (self->headers[UNCSUMMARY_OFFSET].Record != 0)
        {
            UNCSummaryStruct *const unc_struct = (UNCSummaryStruct *)&self->mapped[self->headers[UNCSUMMARY_OFFSET].StartByte];
            PyObject *const result = create_UNCSummary(unc_struct);
            if (result == NULL)
            {

                Py_RETURN_NONE;
            }
            self->UNCSummary = result;
        }
    }
    Py_INCREF(self->UNCSummary);
    return self->UNCSummary;
}

static PyObject *timedep_summary_get(RSRFile *self, void *closure)
{
    if (self->TimeDepSummary == NULL)
    {
        if (self->headers[TDEPSUMMARY_OFFSET].Record != 0)
        {
            TdepSummaryStruct *tdp_struct = (TdepSummaryStruct *)&self->mapped[self->headers[TDEPSUMMARY_OFFSET].StartByte];
            PyObject *const result = create_TdepSummary(tdp_struct);
            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->TimeDepSummary = result;
        }
    }
    Py_INCREF(self->TimeDepSummary);
    return self->TimeDepSummary;
}

static PyObject *misc_summary_get(RSRFile *self, void *closure)
{
    if (self->ResSummaryMisc == NULL)
    {
        if (self->headers[RESSUMMARYMISC_OFFSET].Record != 0)
        {

            ResSummaryMiscStruct *misc_struct = (ResSummaryMiscStruct *)&self->mapped[self->headers[RESSUMMARYMISC_OFFSET].StartByte];

            PyObject *const result = create_ResSummaryMisc(misc_struct);
            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->ResSummaryMisc = result;
        }
    }
    Py_INCREF(self->ResSummaryMisc);
    return self->ResSummaryMisc;
}

static PyObject *be_im_get(RSRFile *self, void *closure)
{
    if (self->BEImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[EVENTIMP_OFFSET].Record;
        if (count > 0)
        {
            PyObject *result = create_BEImportanceTable(
                (const ImpStruct *const)&self->mapped[self->headers[EVENTIMP_OFFSET].StartByte],
                (const EventStruct *const)&self->mapped[self->headers[EVENT_OFFSET].StartByte],
                (const BEEventStruct *const)&self->mapped[self->headers[BEVENT_OFFSET].StartByte],
                (const CCFEventStruct *const)&self->mapped[self->headers[CCFEVENT_OFFSET].StartByte],
                (const MODEventStruct *const)&self->mapped[self->headers[MODEVENT_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->BEImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->BEImpTable);
    return self->BEImpTable;
}

static PyObject *param_im_get(RSRFile *self, void *closure)
{
    if (self->ParamImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[PARAMIMP_OFFSSET].Record;
        if (count > 0)
        {

            PyObject *result = create_ParamImportanceTable(
                (const ImpStruct *const)&self->mapped[self->headers[PARAMIMP_OFFSSET].StartByte],
                (const ParStruct *const)&self->mapped[self->headers[PARAM_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->ParamImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->ParamImpTable);
    return self->ParamImpTable;
}

static PyObject *unc_get(RSRFile *self, const uint_fast8_t type)
{
    const uint8_t count = self->headers[type].Record;
    if (count > 0)
    {

        PyObject *result = PyTuple_New(count + 1);

        PyObject *header_obj = PyTuple_New(2);
        PyTuple_SET_ITEM(header_obj, 0, Py_BuildValue("s", "x"));
        if (type == UNC_PDF_OFFSET)
        {
            PyTuple_SET_ITEM(header_obj, 1, Py_BuildValue("s", "f(x)"));
        }
        else
        {
            PyTuple_SET_ITEM(header_obj, 1, Py_BuildValue("s", "F(x)"));
        }

        PyTuple_SET_ITEM(result, 0, header_obj);

        const DistPou32Struct *const unc_distr_struct =
            (DistPou32Struct *)&self->mapped[self->headers[type].StartByte];

        for (uint_fast8_t i = 0; i < count; i++)
        {
            const double x = unc_distr_struct[i].x;
            const double f = unc_distr_struct[i].y;

            PyObject *row_obj = PyTuple_New(2);

            PyTuple_SET_ITEM(row_obj, 0, Py_BuildValue("d", x));
            PyTuple_SET_ITEM(row_obj, 1, Py_BuildValue("d", f));

            PyTuple_SET_ITEM(result, i + 1, row_obj);
        }
        return result;
    }

    return NULL;
}

static PyObject *cdf_get(RSRFile *self, void *closure)
{
    if (self->cdf == NULL)
    {
        PyObject *result = unc_get(self, UNC_CDF_OFFSET);
        if (result == NULL)
        {
            Py_RETURN_NONE;
        }
        self->cdf = result;
    }
    Py_INCREF(self->cdf);
    return self->cdf;
}

static PyObject *pdf_get(RSRFile *self, void *closure)
{
    if (self->pdf == NULL)
    {
        PyObject *result = unc_get(self, UNC_PDF_OFFSET);
        if (result == NULL)
        {
            Py_RETURN_NONE;
        }
        self->pdf = result;
    }
    Py_INCREF(self->pdf);
    return self->pdf;
}

static PyObject *ccfg_im_get(RSRFile *self, void *closure)
{
    if (self->CCFGImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[CCFGIMP_OFFSET].Record;
        if (count > 0)
        {

            PyObject *result = ccfg_importance_table(
                (const ImpStruct *const)&self->mapped[self->headers[CCFGIMP_OFFSET].StartByte],
                (const CCFGroupStruct *const)&self->mapped[self->headers[CCFGROUP_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->CCFGImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->CCFGImpTable);
    return self->CCFGImpTable;
}

static PyObject *attr_im_get(RSRFile *self, void *closure)
{
    if (self->AttrImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[ATTRIMP_OFFSET].Record;
        if (count > 0)
        {

            PyObject *result = attr_importance_table(
                (const ImpStruct *const)&self->mapped[self->headers[ATTRIMP_OFFSET].StartByte],
                (const AttributeStruct *const)&self->mapped[self->headers[ATTR_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->AttrImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->AttrImpTable);
    return self->AttrImpTable;
}

static PyObject *comp_im_get(RSRFile *self, void *closure)
{
    if (self->CompImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[COMPIMP_OFFSET].Record;
        if (count > 0)
        {

            PyObject *result = attr_importance_table(
                (const ImpStruct *const)&self->mapped[self->headers[COMPIMP_OFFSET].StartByte],
                (const AttributeStruct *const)&self->mapped[self->headers[COMP_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->CompImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->CompImpTable);
    return self->CompImpTable;
}

static PyObject *sys_im_get(RSRFile *self, void *closure)
{
    if (self->SysImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[SYSIMP_OFFSET].Record;
        if (count > 0)
        {
            PyObject *result = attr_importance_table(
                (const ImpStruct *const)&self->mapped[self->headers[SYSIMP_OFFSET].StartByte],
                (const AttributeStruct *const)&self->mapped[self->headers[SYS_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->SysImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->SysImpTable);
    return self->SysImpTable;
}

static PyObject *eg_im_get(RSRFile *self, void *closure)
{
    if (self->EGImpTable == NULL)
    {
        const uint_fast32_t count = self->headers[EGIMP_OFFSET].Record;
        if (count > 0)
        {
            PyObject *result = attr_importance_table(
                (const ImpStruct *const)&self->mapped[self->headers[EGIMP_OFFSET].StartByte],
                (const AttributeStruct *const)&self->mapped[self->headers[EVENTGROUP_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->EGImpTable = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->EGImpTable);
    return self->EGImpTable;
}

static PyObject *mcs_get(RSRFile *self, void *closure)
{
    if (self->mcs == NULL)
    {
        const uint_fast32_t count = self->headers[MCSSTRUCT_OFFSET].Record;
        if (count > 0)
        {

            PyObject *result = create_mcs(
                (const MCSStruct *const)&self->mapped[self->headers[MCSSTRUCT_OFFSET].StartByte],
                (const uint32_t *const)&self->mapped[self->headers[MCSEVENT_OFFSET].StartByte],
                (const EventStruct *const)&self->mapped[self->headers[EVENT_OFFSET].StartByte],
                (const BEEventStruct *const)&self->mapped[self->headers[BEVENT_OFFSET].StartByte],
                (const CCFEventStruct *const)&self->mapped[self->headers[CCFEVENT_OFFSET].StartByte],
                (const MODEventStruct *const)&self->mapped[self->headers[MODEVENT_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->mcs = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->mcs);
    return self->mcs;
}

static PyObject *mod_mcs_get(RSRFile *self, void *closure)
{
    if (self->mod_mcs == NULL)
    {
        const uint_fast32_t count = self->headers[MODMCSSTRUCT_OFFSET].Record;
        if (count > 0)
        {
            PyObject *result = create_mcs(
                (const MCSStruct *const)&self->mapped[self->headers[MODMCSSTRUCT_OFFSET].StartByte],
                (const int32_t *const)&self->mapped[self->headers[MODMCSEVENT_OFFSET].StartByte],
                (const EventStruct *const)&self->mapped[self->headers[EVENT_OFFSET].StartByte],
                (const BEEventStruct *const)&self->mapped[self->headers[BEVENT_OFFSET].StartByte],
                (const CCFEventStruct *const)&self->mapped[self->headers[CCFEVENT_OFFSET].StartByte],
                (const MODEventStruct *const)&self->mapped[self->headers[MODEVENT_OFFSET].StartByte],
                count);

            if (result == NULL)
            {
                Py_RETURN_NONE;
            }
            self->mod_mcs = result;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->mod_mcs);
    return self->mod_mcs;
}

static PyObject *events_get(RSRFile *self, void *closure)
{
    if (self->Events == NULL)
    {
        const uint32_t count = self->headers[EVENT_OFFSET].Record;
        if (count > 0)
        {
            PyObject *dict_obj = PyDict_New();

            const EventStruct *const events =
                &self->mapped[self->headers[EVENT_OFFSET].StartByte];

            const BEEventStruct *const beevent_struct =
                &self->mapped[self->headers[BEVENT_OFFSET].StartByte];

            const CCFEventStruct *const ccfevent_struct =
                &self->mapped[self->headers[CCFEVENT_OFFSET].StartByte];

            const MODEventStruct *const modevent_struct =
                &self->mapped[self->headers[MODEVENT_OFFSET].StartByte];

            for (uint32_t i = 1; i < count; i++)
            {
                EventStruct event = events[i];
                const uint32_t event_index = event.Index;
                const EventType event_type = event.EventType;

                PyObject *value_obj = PyStructSequence_New(&MCSEventType);
                PyStructSequence_SetItem(value_obj, 0, PyFloat_FromDouble(event.Mean));
                PyStructSequence_SetItem(value_obj, 1, PyFloat_FromDouble(event.fW));

                const char *name;
                switch (event_type)
                {
                case BASIC_EVENT:
                    name = beevent_struct[event_index].Name;
                    break;
                case CCF_EVENT:
                    name = ccfevent_struct[event_index].Name;
                    break;
                case MOD_EVENT:
                    name = modevent_struct[event_index].Name;
                    break;
                default:
                    PyErr_SetString(PyExc_Exception, "Error. Can't read event id. Undefine event type");
                    return NULL;
                }

                const size_t len = trim(name, MAX_ID_LEN);
                PyDict_SetItem(dict_obj, Py_BuildValue("s#", name, len), value_obj);
            }
            self->Events = dict_obj;
        }
        else
        {
            Py_RETURN_NONE;
        }
    }
    Py_INCREF(self->Events);
    return self->Events;
}

static PyGetSetDef RSRFile_getsets[] = {
    {"mcs_summary", (getter)mcs_summary_get, NULL,
     "Minimal cut sets summary information", /* doc */
     NULL /* closure */},

    {"unc_summary", (getter)unc_summary_get, NULL,
     "Uncertainty analysis summary information", /* doc */
     NULL /* closure */},

    {"timedep_summary", (getter)timedep_summary_get, NULL,
     "Time-dependent analysis summary information", /* doc */
     NULL /* closure */},

    {"misc_summary", (getter)misc_summary_get, NULL,
     "Misc summary information", /* doc */
     NULL /* closure */},

    {"be_im", (getter)be_im_get, NULL,
     "Importance of basic events",
     NULL /* closure */},

    {"param_im", (getter)param_im_get, NULL,
     "Importance of parameters",
     NULL /* closure */},

    {"ccfg_im", (getter)ccfg_im_get, NULL,
     "Importance of common cause failure groups", /* doc */
     NULL /* closure */},

    {"attr_im", (getter)attr_im_get, NULL,
     "Importance of attributes",
     NULL /* closure */},

    {"comp_im", (getter)comp_im_get, NULL,
     "Importance of components",
     NULL /* closure */},

    {"sys_im", (getter)sys_im_get, NULL,
     "Importance of systems",
     NULL /* closure */},

    {"eg_im", (getter)eg_im_get, NULL,
     "Importance of event groups", /* doc */
     NULL /* closure */},

    {"pdf", (getter)pdf_get, NULL,
     "Probability density function of results", /* doc */
     NULL /* closure */},

    {"cdf", (getter)cdf_get, NULL,
     "Cumulative distribution function of results", /* doc */
     NULL /* closure */},

    {"mcs", (getter)mcs_get, NULL,
     "Minimal cut sets", /* doc */
     NULL /* closure */},

    {"mod_mcs", (getter)mod_mcs_get, NULL,
     "Mod. minimal cut sets", /* doc */
     NULL /* closure */},

    {"events", (getter)events_get, NULL,
     "Dictionary of events used in the minimum sections", /* doc */
     NULL /* closure */},

    {NULL}};

static PyMethodDef RSRFile_methods[] = {
    {"open", (PyCFunction)RSRFile_open, METH_VARARGS, "Open rsr file"},
    {"close", (PyCFunction)RSRFile_close, METH_NOARGS, "Close file"},
    {"__enter__", (PyCFunction)RSRFile_enter, METH_NOARGS, "Enter the runtime context"},
    {"__exit__", (PyCFunction)RSRFile_exit, METH_VARARGS, "Exit the runtime context"},
    {NULL} /* Sentinel */
};

PyTypeObject RSRFileType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "rsrfile.RSRFile",
    .tp_doc = PyDoc_STR("RSR File objects"),
    .tp_basicsize = sizeof(RSRFile),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = RSRFile_new,
    .tp_init = (initproc)RSRFile_init,
    .tp_dealloc = (destructor)RSRFile_dealloc,
    .tp_members = RSRFile_members,
    .tp_methods = RSRFile_methods,
    .tp_getset = RSRFile_getsets,
};
