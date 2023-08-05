#include "MCSSummaryStruct.h"

PyTypeObject MCSSummaryType;

static PyStructSequence_Field MCSSummaryType_fields[] = {
    {"DateTime", "Date and time of creation"},
    {"InputFormat", "RiskSpectrum, FTAP orSets"},
    {"AcaseType", ""},
    {"AcaseSpec1_rsat", ""},
    {"AcaseSpec1_rsatexe", ""},
    {"AcaseSpec1_rsmisc", ""},
    {"AcaseSpec1_rsuit", ""},
    {"AcaseSpec1_rsmcs", ""},
    {"AcaseSpec2", ""},
    {"BCSetUsed", ""},
    {"CalcType", "Calculation type, Q, Q(T), F, F(T), W, W(T)"},
    {"Time", ""},
    {"CutOffType", "There are two types available - 'Probabilistic' and 'By cutset order'"},
    {"AbsCutOff", "Absolute cutoff value, ACUTM"},
    {"RelCutOff", "Relative cutoff value, RCUTM"},
    {"Approx", " Approximation order for calculating the top event probability or frequency"},
    {"IncludeCCF", "Include or not include these CCF when RiskSpectrum PSA carries out the generation of MCS"},
    {"NegationHandling", ""},
    {"SaveCutoff", "Set the ratio between the MCS that you dispose of and the MCS you want to save"},
    {"MaxSaveModMCS", "absolute limit on the number of saved modularised cutsets"},
    {"MaxSavedDemodMCS", "absolute limit on the number of saved demodularised cutsets"},
    {"Events", "Number of all events"},
    {"BEEvents", "Number of basic events"},
    {"CCFEvents", "Number of CCF events"},
    {"Gates", "Number of gates"},
    {"PrimaryEvents", "Number of "},
    {"ModEvents", "Number of "},
    {"ModBEEvents", "Number of "},
    {"ModCCFEvents", "Number of "},
    {"ModGates", "Number of "},
    {"ModPrimaryEvents", "Number of "},
    {"Modules", "Number of "},
    {"ModChildren", ""},
    {"BICSMod", ""},
    {"BICSDemod", ""},
    {"MCSMod", ""},
    {"TotDemodMCS", ""},
    {"MCSDemod", ""},
    {"MCSModSaved", "number of generated modelarised minimal cutsets"},
    {"MCSDemodSaved", "number of demodularised minimal cutsets"},
    {"fQ", ""},
    {"QBestApprox", ""},
    {"fW", ""},
    {"WBestApprow", ""},
    {"TruncErrorMod", ""},
    {"TruncErrorDemod", ""},
    {"TruncErrorTot", ""},
    {"UsedCutoffDemod", "final cutoff value for demodularisation"},
    {"UsedCutoffMod", "final cutoff value for generating the modularised minimal cutsets"},
    {"RunTimeTot", "Calculation execution time"},
    {"RunTimeMCS", "Time to perform the generation of MCS"},
    {
        NULL,
    },
};

PyStructSequence_Desc MCSSummaryType_desc = {
    "MCSSummaryStruct",  /* name */
    "MCSSummary struct", /* doc */
    MCSSummaryType_fields,
    51};

PyObject *create_MCSSummary(MCSSummaryStruct *mcs_struct)
{
    PyObject *mcs_obj = PyStructSequence_New(&MCSSummaryType);

    PyObject *dt = DateTimeFromString(mcs_struct->DateTime);
    PyStructSequence_SetItem(mcs_obj, 0, dt);
    // PyStructSequence_SetItem(mcs_obj, 0, Py_BuildValue("s#", mcs_struct->DateTime, 19));
    PyStructSequence_SetItem(mcs_obj, 1, Py_BuildValue("h", mcs_struct->InputFormat));
    PyStructSequence_SetItem(mcs_obj, 2, Py_BuildValue("h", mcs_struct->AcaseType));
    PyStructSequence_SetItem(mcs_obj, 3, Py_BuildValue("i", mcs_struct->AcaseSpec1_rsat));
    PyStructSequence_SetItem(mcs_obj, 4, Py_BuildValue("i", mcs_struct->AcaseSpec1_rsatexe));
    PyStructSequence_SetItem(mcs_obj, 5, Py_BuildValue("i", mcs_struct->AcaseSpec1_rsmisc));
    PyStructSequence_SetItem(mcs_obj, 6, Py_BuildValue("i", mcs_struct->AcaseSpec1_rsuit));
    PyStructSequence_SetItem(mcs_obj, 7, Py_BuildValue("i", mcs_struct->AcaseSpec1_rsmcs));
    PyStructSequence_SetItem(mcs_obj, 8, Py_BuildValue("i", mcs_struct->AcaseSpec2));
    PyStructSequence_SetItem(mcs_obj, 9, Py_BuildValue("i", mcs_struct->BCSetUsed));
    PyStructSequence_SetItem(mcs_obj, 10, Py_BuildValue("h", mcs_struct->CalcType));
    PyStructSequence_SetItem(mcs_obj, 11, Py_BuildValue("d", mcs_struct->Time));
    PyStructSequence_SetItem(mcs_obj, 12, Py_BuildValue("h", mcs_struct->CutOffType));
    PyStructSequence_SetItem(mcs_obj, 13, Py_BuildValue("d", mcs_struct->AbsCutOff));
    PyStructSequence_SetItem(mcs_obj, 14, Py_BuildValue("d", mcs_struct->RelCutOff));
    PyStructSequence_SetItem(mcs_obj, 15, Py_BuildValue("h", mcs_struct->Approx));
    PyStructSequence_SetItem(mcs_obj, 16, Py_BuildValue("h", mcs_struct->IncludeCCF));
    PyStructSequence_SetItem(mcs_obj, 17, Py_BuildValue("h", mcs_struct->NegationHandling));
    PyStructSequence_SetItem(mcs_obj, 18, Py_BuildValue("d", mcs_struct->SaveCutoff));
    PyStructSequence_SetItem(mcs_obj, 19, Py_BuildValue("i", mcs_struct->MaxSavedModMCS));
    PyStructSequence_SetItem(mcs_obj, 20, Py_BuildValue("i", mcs_struct->MaxSavedDemodMCS));
    PyStructSequence_SetItem(mcs_obj, 21, Py_BuildValue("i", mcs_struct->Events));
    PyStructSequence_SetItem(mcs_obj, 22, Py_BuildValue("i", mcs_struct->BEEvents));
    PyStructSequence_SetItem(mcs_obj, 23, Py_BuildValue("i", mcs_struct->CCFEvents));
    PyStructSequence_SetItem(mcs_obj, 24, Py_BuildValue("i", mcs_struct->Gates));
    PyStructSequence_SetItem(mcs_obj, 25, Py_BuildValue("i", mcs_struct->PrimaryEvents));
    PyStructSequence_SetItem(mcs_obj, 26, Py_BuildValue("i", mcs_struct->ModEvents));
    PyStructSequence_SetItem(mcs_obj, 27, Py_BuildValue("i", mcs_struct->ModBEEvents));
    PyStructSequence_SetItem(mcs_obj, 28, Py_BuildValue("i", mcs_struct->ModCCFEvents));
    PyStructSequence_SetItem(mcs_obj, 29, Py_BuildValue("i", mcs_struct->ModGates));
    PyStructSequence_SetItem(mcs_obj, 30, Py_BuildValue("i", mcs_struct->ModPrimaryEvents));
    PyStructSequence_SetItem(mcs_obj, 31, Py_BuildValue("i", mcs_struct->Modules));
    PyStructSequence_SetItem(mcs_obj, 32, Py_BuildValue("i", mcs_struct->ModChildren));
    PyStructSequence_SetItem(mcs_obj, 33, create_LargeNum(&mcs_struct->BICSMod));
    PyStructSequence_SetItem(mcs_obj, 34, create_LargeNum(&mcs_struct->BICSDemod));
    PyStructSequence_SetItem(mcs_obj, 35, Py_BuildValue("i", mcs_struct->MCSMod));
    PyStructSequence_SetItem(mcs_obj, 36, create_LargeNum(&mcs_struct->TotDemodMCS));
    PyStructSequence_SetItem(mcs_obj, 37, Py_BuildValue("i", mcs_struct->MCSDemod));
    PyStructSequence_SetItem(mcs_obj, 38, Py_BuildValue("i", mcs_struct->MCSModSaved));
    PyStructSequence_SetItem(mcs_obj, 39, Py_BuildValue("i", mcs_struct->MCSDemodSaved));

    PyObject *fQ_obj = PyTuple_New(4);
    for (int i = 0; i < 4; i++)
    {
        PyTuple_SET_ITEM(fQ_obj, i, PyFloat_FromDouble(mcs_struct->fQ[i]));
    }
    PyStructSequence_SetItem(mcs_obj, 40, fQ_obj);

    PyStructSequence_SetItem(mcs_obj, 41, Py_BuildValue("d", mcs_struct->QBestApprox));

    PyObject *fW_obj = PyTuple_New(4);
    for (int i = 0; i < 4; i++)
    {
        PyTuple_SET_ITEM(fW_obj, i, PyFloat_FromDouble(mcs_struct->fW[i]));
    }
    PyStructSequence_SetItem(mcs_obj, 42, fW_obj);

    PyStructSequence_SetItem(mcs_obj, 43, Py_BuildValue("d", mcs_struct->WBestApprox));
    PyStructSequence_SetItem(mcs_obj, 44, Py_BuildValue("d", mcs_struct->TruncErrorMod));
    PyStructSequence_SetItem(mcs_obj, 45, Py_BuildValue("d", mcs_struct->TruncErrorDemod));
    PyStructSequence_SetItem(mcs_obj, 46, Py_BuildValue("d", mcs_struct->TruncErrorTot));
    PyStructSequence_SetItem(mcs_obj, 47, Py_BuildValue("d", mcs_struct->UsedCutoffDemod));
    PyStructSequence_SetItem(mcs_obj, 48, Py_BuildValue("d", mcs_struct->UsedCutoffMod));
    PyStructSequence_SetItem(mcs_obj, 49, Py_BuildValue("d", mcs_struct->RunTimeTot));
    PyStructSequence_SetItem(mcs_obj, 50, Py_BuildValue("d", mcs_struct->RunTimeMCS));

    return mcs_obj;
}