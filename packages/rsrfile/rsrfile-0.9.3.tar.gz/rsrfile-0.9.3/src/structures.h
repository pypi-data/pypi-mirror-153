#ifndef STRUCTURES
#define STRUCTURES

#include <stdint.h>

#define ARRAY_SIZE(array) (sizeof(array) / sizeof(array[0]))
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

/*
Summary information offset
*/
#define MCSSUMMARY_OFFSET 0
#define UNCSUMMARY_OFFSET 1
#define TDEPSUMMARY_OFFSET 2
#define RESSUMMARYMISC_OFFSET 58

/*
Importance measurement offsets
*/
#define EVENTIMP_OFFSET 17
#define PARAMIMP_OFFSSET 19
#define EGIMP_OFFSET 23
#define ATTRIMP_OFFSET 27
#define SYSIMP_OFFSET 31
#define COMPIMP_OFFSET 35
#define CCFGIMP_OFFSET 39

/*
Modularization objects offset
*/
#define MODMCSSTRUCT_OFFSET 4
#define MODMCSEVENT_OFFSET 5
#define MODEVENT_OFFSET 6

/*
Minimal cut set objects offset
*/
#define MCSSTRUCT_OFFSET 8
#define MCSEVENT_OFFSET 9

//#define MODMCSEVENT_OFFSET 57

/*
Basic objects offset
*/
#define EVENT_OFFSET 10
#define BEVENT_OFFSET 11
#define CCFEVENT_OFFSET 12
#define PARAM_OFFSET 13

/*
Attributes objects offset
*/
#define EVENTGROUP_OFFSET 21
#define ATTR_OFFSET 25
#define COMP_OFFSET 29
#define SYS_OFFSET 33
#define CCFGROUP_OFFSET 37

/*
Uncertainty calculation results offset
*/
#define UNC_CDF_OFFSET 41
#define UNC_PDF_OFFSET 42
#define PDF_HISTOGRAM_OFFSET 43

#define TIMEDEPSTRUCT_OFFSET 44
#define AGROUPSTRUCT_OFFSET 45

/*
The maximum length of the identifier. Applies to almost all objects.
Since version 1.5+, the maximum length has become 50
*/
#define MAX_ID_LEN 20

typedef enum
{
    BASIC_EVENT = 5,
    CCF_EVENT = 12,
    MOD_EVENT = 99
} EventType;

enum ImpType
{
    BASIC_EVENTS = 1,
    PARAMS = 2,
    COMPONENTS = 4,
    SYSTEMS = 8,
    ATTRIBUTES = 16,
    CCFG = 16
};

typedef enum
{
    PROBABILITY = 1,
    FAILURE_RATE = 2,
    FREQUENCY = 3,
    REPAIR_RATE = 99,
    REPAIR_TIME = 99,
    TEST_INTERVAL = 5,
    TIME_TO_FIRST_TEST = 99,
    MISSION_TIME = 7,
    ALPHA = 8
} ParamType;

typedef enum
{
    CONTINUOSLY = 1,        /* Continuously monitored, repairable */
    PERIODICALLY = 2,       /* Periodically tested */
    CONST_PROBABILITY = 3,  /* Constant probability */
    CONST_MISSION_TIME = 4, /* Component with fixed mission time */
    CONST_FREQUENCY = 5,    /* Constant frequency */
    UNREPAIRABLE = 6        /* Unrepairable component  */
} RALABILITY_MODEL;

typedef enum
{
    NONE = 0,
    LOGNORM = 1
} DISTR_TYPE;

/*
TOC structure
*/
typedef struct
{
    int32_t Record;
    uint32_t StartByte;
    uint32_t Byte;
} __attribute__((__packed__)) AnFileHeaderStruct;

typedef struct
{
    uint16_t Type;
    uint32_t Num;
    char Id[MAX_ID_LEN];
    uint16_t TextRes;
    uint16_t GeRes;
    uint16_t BeRes;
    uint16_t ExchRes;
    uint16_t Unit;
} __attribute__((__packed__)) AnAcaseStruct;

typedef struct
{
    uint32_t TopNum;
    uint32_t AcaseNum;
} __attribute__((__packed__)) AnTopAcaseStruct;

typedef struct
{
    uint32_t AcaseNum;
    uint16_t SetupType;
    uint32_t SetupNum;
} __attribute__((__packed__)) AnAcaseSetupStruct;

typedef struct
{
    uint16_t Type;
    uint32_t Num;
    char Id[MAX_ID_LEN];
    uint16_t DistType;
    double Mean;
    double DistPar1;
    double DistPar2;
    uint16_t Unit;
} __attribute__((__packed__)) MCSParStruct;

typedef struct
{
    uint32_t Num;
    char Id[MAX_ID_LEN];
} __attribute__((__packed__)) MCSNullValParStruct;

typedef struct
{
    uint32_t CreatorApp;
    uint32_t CreatorVerMajor;
    uint32_t CreatorVerMinor;
    uint32_t CreatorVerRev;
    uint32_t CreationYear;
    uint32_t CreationMonth;
    uint32_t CreationDay;
    double d1; // byte[] MiscBuffer1;
    double d2; // byte[] MiscBuffer2;
    double d3; // byte[] MiscBuffer3;
    uint32_t MiscValue1;
    uint32_t MiscValue2;
    uint32_t MiscValue3;
} __attribute__((__packed__)) MCSVersionStruct;

typedef struct
{
    double Mean;
    uint32_t FirstEvent;
    uint32_t LastEvent;
} __attribute__((__packed__)) MCSStruct;

typedef struct
{
    uint32_t Index;
    uint16_t EventType;
    // char Name[MAX_ID_LEN];
    double Mean;
    uint16_t InitEnabl;
    char reserc[8];
} __attribute__((__packed__)) GenEventStruct;

typedef struct
{
    uint32_t Index[10];
    double ImpSens;
} __attribute__((__packed__)) RecImpResStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN];
    uint32_t LastEvent;
} __attribute__((__packed__)) AttributeStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN];
    uint32_t LastCCFEvent;
    uint32_t LastBEEvent;
} __attribute__((__packed__)) CCFGroupStruct;

typedef struct
{
    double x;
    double y;
} __attribute__((__packed__)) DistPou32Struct;

typedef struct
{
    double t;
    double Q;
    double W;
    double L;
    double E;
    double F;
} __attribute__((__packed__)) TimeDepStruct;

typedef struct
{
    uint32_t Acase;
    uint16_t AcaseType;
    uint32_t Top;
    char NameAcase[MAX_ID_LEN];
    char NameTop[MAX_ID_LEN];
    uint16_t CalcType;
    double Time;
    uint16_t CutOffType;
    double AbsCutOff;
    double RelCutOff;
    double FinalCutOff;
    double QMCS;
    double WMCS;
    uint32_t NoMCSMod;
    uint32_t NoMCSDemod;
    uint32_t Simulations;
    uint16_t SimType;
    double Median;
    double MeanUNC;
    double f5th;
    double f95th;
    uint16_t Importance;
    double Time1;
    double Time2;
    uint32_t TimePts;
    double QMean;
    double QMax;
    double WMean;
    double WMax;
    double LMean;
    double LMax;
    double FMax;
    double EMax;
} __attribute__((__packed__)) AGroupResStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN];
    uint16_t nModType;
    uint32_t FirstChild;
    uint32_t LastChild;
    uint32_t BCNum;
    uint16_t GateDep;
} __attribute__((__packed__)) GateEventStruct;

typedef struct
{
    uint32_t Index;
    double Value;
    double FV;
    double RDF;
    double FC;
    double RIF;
    double SensHigh;
    double SensLow;
    double Sens;
} __attribute__((__packed__)) ImpStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN];
    uint16_t ModType;
    uint32_t LastChild;
} __attribute__((__packed__)) MODEventStruct;

typedef struct
{
    uint32_t Index;
    uint16_t EventType;
    double Mean;
    double fW;
    uint16_t InitEnable;

} __attribute__((__packed__)) EventStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN]; // Unique name
    uint16_t RelModel;     /* Reliability model */
    uint32_t LastPar;
    uint16_t InitEnabl;
} __attribute__((packed)) BEEventStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN];
    uint16_t CCFModel;
    uint16_t RelModel;
    uint16_t Events;
    uint16_t TotEvents;
    uint32_t LastPar;
} __attribute__((__packed__)) CCFEventStruct;

typedef struct
{
    uint32_t Index;
    char Name[MAX_ID_LEN];
    uint16_t PARType;
    uint16_t DistType;
    double Value;
    uint32_t FirstDistValue;
} __attribute__((__packed__)) ParStruct;

#endif /* STRUCTURES */
