#ifndef BYTE_CODE_COUNTER_H
#define BYTE_CODE_COUNTER_H

#include "Python.h"
#include <stdio.h>
#include <wchar.h>
#include <time.h>

// TODO Find out how to include opcode.h and use it to determine BCC_ARR_SIZE.
#define BCC_ARR_SIZE 258 // EXCEPT_HANDLER+1
#define BCC_TXT_PATH_LEN 11
#define BCT_BUFFER_SIZE 1000000
#define BILLION 1000000000

#define BCT_CLOCK CLOCK_PROCESS_CPUTIME_ID 

typedef struct BC_timing_struct
{
    long nsec_dur;
    int opcode;
} BC_timing;

typedef struct BC_timings_buffer_struct
{
    BC_timing *buffer;
    size_t cur_size;
    long frequency;
    int is_init;
} BC_timings_buffer;


void Py_PrintByteCodes(void);

char *Py_GetLine(FILE *fp, size_t *len);

char *Py_GetBCPath(size_t *len);

char *Py_GetBCFullPath(char *filename, size_t filename_len, size_t *out_len);

char *Py_AddFileExt(char *filename, size_t filename_len, char *file_ext, size_t file_ext_len);

int Py_WriteByteCodes(void);

char* Py_VerifyFilename(const wchar_t *file_path, size_t *len);

char *Py_GetFilename(const wchar_t *filename_path, size_t *len);

int Py_SaveBytecodeTimings(BC_timing timing);

int Py_WriteByteCodeTimings(BC_timings_buffer buffer);

int Py_Init_BCT(const wchar_t *file_path);

char *Py_GetDate(size_t *len);

int Py_Exit_BCT(void);

unsigned long long bcc_arr[BCC_ARR_SIZE];

BC_timings_buffer *_internal_timings_buffer;

#ifdef _WIN32
    #define DECL_BCC_TIMERS \
        LARGE_INTEGER frequency; \
        LARGE_INTEGER bc_time_start; \
        LARGE_INTEGER bc_time_end \
    
    #define INIT_BCC_TIMERS \
        QueryPerformanceFrequency(&frequency) \
        QueryPerformanceCounter(&bc_time_end); \
        QueryPerformanceCounter(&bc_time_start); \

    #define INC_OPCODE_ARR(opcode) \
        QueryPerformanceCounter(&bc_time_end); \

        QueryPerformanceCounter(&bc_time_start) \

    #define PATH_SEP "\\"

#else
    #define DECL_BCC_TIMERS \
        struct timespec bc_time_start; \
        struct timespec bc_time_end; \
        clockid_t clk_id = BCT_CLOCK; \
    
    #define INIT_BCC_TIMERS \
        clock_gettime(clk_id, &bc_time_end); \
        clock_gettime(clk_id, &bc_time_start); \

    #define INC_OPCODE_ARR(opcode) \
        clock_gettime(clk_id, &bc_time_end); \
        long diff = 0; \
        if(bc_time_end.tv_nsec >= bc_time_start.tv_nsec) \
        { \
            diff = bc_time_end.tv_nsec - bc_time_start.tv_nsec; \
        } \
        else /* Handle the case where bc_time_end overflows. */ \
        { \
            diff = (bc_time_end.tv_nsec + 1000000000L) - bc_time_start.tv_nsec; \
        } \
        BC_timing timing = \
        { \
            .nsec_dur = diff, \
            .opcode = opcode \
        }; \
        Py_SaveBytecodeTimings(timing); \
        clock_gettime(clk_id, &bc_time_start); \
    
    #define PATH_SEP "/"
#endif

#endif /* BYTE_CODE_COUNTER_H */
