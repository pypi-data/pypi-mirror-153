#ifndef TDEPSUMMARYSTRUCT
#define TDEPSUMMARYSTRUCT

#include <Python.h>
#include <fcntl.h>

#include "common.h"

typedef struct 
{
    char DateTime[20];
    uint16_t CalcType;
    double Time;
    double Time1;
    double Time2;
    double LMax;
    double AbsCutOff;
    uint32_t TimePts;
    double QMean;
    double QMax;
    double WMean;
    double WMax;
    double LMean;
    double FMax;
    double EMax;
    double RunTimeTot;
}__attribute__ ((__packed__)) TdepSummaryStruct;

extern PyTypeObject TdepSummaryType;
extern PyStructSequence_Desc TdepSummaryType_desc;

PyObject *create_TdepSummary(TdepSummaryStruct *tdep_struct);


#endif /* TDEPSUMMARYSTRUCT */
