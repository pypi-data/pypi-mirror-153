#ifndef RSRFILE
#define RSRFILE

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <datetime.h>
#include <sys/mman.h>
#include <fcntl.h>

#include "MCSSummaryStruct.h"
#include "UNCSummaryStruct.h"
#include "TdepSummaryStruct.h"
#include "ResSummaryMiscStruct.h"
#include "ImpTable.h"
#include "MCSStruct.h"
#include "MCSEvent.h"

#include "structures.h"

typedef struct
{
    PyObject_HEAD
    PyObject *MCSSummary; /* General information about the calculation results */
    PyObject *UNCSummary;     /*General information about the results of the uncertainty calculation  */
    PyObject *TimeDepSummary;
    PyObject *ResSummaryMisc;
    PyObject *BEImpTable;
    PyObject *CCFGImpTable;
    PyObject *ParamImpTable;
    PyObject *AttrImpTable;
    PyObject *CompImpTable;
    PyObject *SysImpTable;
    PyObject *EGImpTable;
    PyObject *pdf;
    PyObject *cdf; 
    PyObject *mcs; 
    PyObject *mod_mcs; 
    PyObject *Events;
    PyObject *filepath;
    PyObject *mode;
    uint8_t *mapped;
    AnFileHeaderStruct *headers;
    int fp;
    off_t file_size;
    
} RSRFile;

extern PyTypeObject RSRFileType;

#endif /* RSRFILE */
