#ifndef MCSSUMMARYSTRUCT
#define MCSSUMMARYSTRUCT

#include <Python.h>
#include <fcntl.h>
 
#include "LargeNumStruct.h"
#include "common.h"


typedef enum
{
    Q_CALC =6,
    F_CALC =9

} CALC_TYPE;

typedef enum
{
    SEQUENCE = 32,
    EVENTS = 33

} ACASE_TYPE;

typedef struct  
{
    char DateTime[20];
    uint16_t InputFormat;
    uint16_t AcaseType;
    uint32_t AcaseSpec1_rsat;
    uint32_t AcaseSpec1_rsatexe;
    uint32_t AcaseSpec1_rsmisc;
    uint32_t AcaseSpec1_rsuit;
    uint32_t AcaseSpec1_rsmcs;
    uint32_t AcaseSpec2;
    uint32_t BCSetUsed;
    uint16_t CalcType;
    double Time;
    uint16_t CutOffType;
    double AbsCutOff;
    double RelCutOff;
    uint16_t Approx;
    uint16_t IncludeCCF;
    uint16_t NegationHandling;
    double SaveCutoff;
    uint32_t MaxSavedModMCS;
    uint32_t MaxSavedDemodMCS;
    uint32_t Events;
    uint32_t BEEvents;
    uint32_t CCFEvents;
    uint32_t Gates;
    uint32_t PrimaryEvents;
    uint32_t ModEvents;
    uint32_t ModBEEvents;
    uint32_t ModCCFEvents;
    uint32_t ModGates;
    uint32_t ModPrimaryEvents;
    uint32_t Modules;
    uint32_t ModChildren;
    LargeNumStruct BICSMod;
    LargeNumStruct BICSDemod;
    uint32_t MCSMod;
    LargeNumStruct TotDemodMCS;
    uint32_t MCSDemod;
    uint32_t MCSModSaved;
    uint32_t MCSDemodSaved;
    /*
    fQ[0] - MCUB
    fQ[1] - first order approximation  of Q
    fQ[2] - second order approximation of Q
    fQ[3] - third order approximation  of Q
    */
    double fQ[4];
    double QBestApprox;
    /*
    fW[0] - MCUB
    fW[1] - first order approximation  of W
    fW[2] - second order approximation of W
    fW[3] - third order approximation  of W
    */
    double fW[4];
    double WBestApprox;
    double TruncErrorMod;
    double TruncErrorDemod;
    double TruncErrorTot;
    double UsedCutoffDemod;
    double UsedCutoffMod;
    double RunTimeTot;
    double RunTimeMCS;
}__attribute__ ((__packed__)) MCSSummaryStruct;

extern PyTypeObject MCSSummaryType;
extern PyStructSequence_Desc MCSSummaryType_desc;

PyObject *create_MCSSummary(MCSSummaryStruct *mcs_struct);

#endif /* MCSSUMMARYSTRUCT */
