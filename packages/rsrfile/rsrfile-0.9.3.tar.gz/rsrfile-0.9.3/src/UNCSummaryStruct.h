#ifndef UNCSUMMARYSTRUCT
#define UNCSUMMARYSTRUCT

#include <Python.h>
#include <fcntl.h>
#include "common.h"

typedef struct 
{
    char DateTime[20];
    uint16_t CalcType;
    double Time;
    double AbsCutOff;
    uint32_t Simulations;
    uint16_t SimType;
    uint16_t Seed;
    uint16_t RndType;
    double Mean;
    double Median;
    double f5th;
    double f95th;
    double RunTimeTot;
}__attribute__ ((__packed__)) UNCSummaryStruct;

extern PyTypeObject UNCSummaryType;
extern PyStructSequence_Desc UNCSummaryType_desc;

PyObject *create_UNCSummary(UNCSummaryStruct *unc_struct);

#endif /* UNCSUMMARYSTRUCT */
