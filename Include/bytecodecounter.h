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

// TODO Find out how to include opcode.h and use it to determine the BCC arr size.
#define BCC_ARR_SIZE 258//EXCEPT_HANDLER+1
unsigned long long bcc_arr[];

void Py_PrintByteCodes();

// char *Py_GetLine(FILE *fp); TODO Find out why this refuses to build when including it.

char *Py_ReadBCCPath();

int Py_WriteByteCodes();

#endif /* BYTE_CODE_COUNTER_H */
