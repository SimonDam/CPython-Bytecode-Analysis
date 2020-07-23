#ifndef BYTE_CODE_COUNTER_H
#define BYTE_CODE_COUNTER_H

#include <stdio.h>
#include <wchar.h>
#include <time.h>

#ifdef _WIN32
    #define DECL_BCC_TIMERS \
        LARGE_INTEGER frequency; \
        LARGE_INTEGER bc_time_start; \
        LARGE_INTEGER bc_time_end \
    
    #define INIT_BCC_TIMERS \
        QueryPerformanceFrequency(&frequency) \
        QueryPerformanceCounter(&bc_time_end); \
        QueryPerformanceCounter(&bc_time_start); \

    #define INC_OPCODE_ARR(index) \
        QueryPerformanceCounter(&bc_time_end); \
        if(index > BCC_ARR_SIZE - 1 || index < 0) \
        { \
            printf("Invalid opcode: %d", index); \
        } \
        else \
        { \
            bcc_arr[index]++; \
            long double difference = (long double)(bc_time_end.QuadPart - bc_time_start.QuadPart); \
            long double time = difference / frequency.QuadPart; \
        } \
        QueryPerformanceCounter(&bc_time_start) \

    #define PATH_SEP "\\"

#else
    #define DECL_BCC_TIMERS \
        struct timespec bc_time_start; \
        struct timespec bc_time_end; \
        clockid_t clk_id = CLOCK_PROCESS_CPUTIME_ID; \
        int abemad;\
    
    #define INIT_BCC_TIMERS \
        clock_gettime(clk_id, &bc_time_end); \
        clock_gettime(clk_id, &bc_time_start); \
        abemad = 0;\

    #define INC_OPCODE_ARR(opcode) \
        clock_gettime(clk_id, &bc_time_end); \
        if(opcode > BCC_ARR_SIZE - 1 || opcode < 0) \
        { \
            printf("Invalid opcode: %d", opcode); \
        } \
        else \
        { \
            bcc_arr[opcode]++; \
            long difference = bc_time_end - bc_time_start;
        } \
        clock_gettime(clk_id, &bc_time_start); \
    
    #define PATH_SEP "/"
#endif

// TODO Find out how to include opcode.h and use it to determine BCC_ARR_SIZE.
#define BCC_ARR_SIZE 258//EXCEPT_HANDLER+1
#define BCC_TXT_PATH_LEN 11

unsigned long long bcc_arr[BCC_ARR_SIZE];

void Py_PrintByteCodes(void);

char *Py_GetLine(FILE *fp);

char *Py_ReadBCCPath(void);

int Py_WriteByteCodes(void);

void Py_SetFilename(const wchar_t *file_path);

char *Py_GetFilename(void);

#endif /* BYTE_CODE_COUNTER_H */
