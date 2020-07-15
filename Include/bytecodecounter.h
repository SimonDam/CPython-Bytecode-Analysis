#ifndef BYTE_CODE_COUNTER_H
#define BYTE_CODE_COUNTER_H
#define DECL_BCC_TIMERS \
    LARGE_INTEGER frequency; \
    LARGE_INTEGER bc_time_start; \
    LARGE_INTEGER bc_time_end \

#define INIT_BCC_TIMERS \
    QueryPerformanceCounter(&bc_time_start); \
    QueryPerformanceCounter(&bc_time_end); \
    QueryPerformanceFrequency(&frequency) \

#define INC_OPCODE_ARR(index) \
    QueryPerformanceCounter(&bc_time_end); \
    if(index > BCC_ARR_SIZE - 1 || index < 0){ \
        printf("Unable to increment opcode: %d", index); \
    } \
    else{ \
        bcc_arr[index]++; \
        long double difference = (long double)(bc_time_end.QuadPart - bc_time_start.QuadPart); \
        long double time = difference / frequency.QuadPart; \
    } \
    QueryPerformanceCounter(&bc_time_start); \

#ifdef _WIN32
    #define PATH_SEP "\\"
#else
    #define PATH_SEP "/"
#endif

/* TODO Find out how to include opcode.h and use it to determine the BCC arr size.*/
#define BCC_ARR_SIZE 258//EXCEPT_HANDLER+1
#define BCC_TXT_PATH_LEN 11
unsigned long long bcc_arr[];

void Py_PrintByteCodes(void);

/*wchar_t *Py_GetLine(FILE); //TODO Why does this argument not build with "FILE*"*/

//wchar_t *Py_ReadBCCPath(void);

int Py_WriteByteCodes(void);

/*void Py_SetFilename(wchar_t); //TODO Why does this argument not build with "wchar_t*"*/

//wchar_t *Py_GetFilename(void);

#endif /* BYTE_CODE_COUNTER_H */
