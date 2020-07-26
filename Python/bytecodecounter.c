#include "Python.h"
#include "bytecodecounter.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#ifdef _WIN32
    #include <windows.h>
#else
    #include <time.h>
#endif

unsigned long long bcc_arr[BCC_ARR_SIZE];

BC_timings_buffer BCT_buffer;

static char *output_file_path;

static const char BCC_Txt_Path[BCC_TXT_PATH_LEN] = "."PATH_SEP"bcc.txt";

// TODO refactor these functions into different files.
void Py_PrintByteCodes(void)
{
    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        printf("%d,%llu\n", i, bcc_arr[i]);
    }
}

char *Py_GetLine(FILE *fp, size_t *len)
{
    size_t current_len = 0;
    char *full_string = NULL;

    char temp[32];
    while(fgets(temp, sizeof(temp), fp))
    {
        // Start by getting the length of the string.
        size_t temp_len = strlen(temp);

        // In case full_length is about to overflow.
        if(SIZE_MAX - temp_len - 1 < current_len)
        {
            printf("Unusually large size read while reading line from file (%zu).\n", current_len);
            // Just break here, since we still have to free full_string.
            break;
        }
        size_t new_len = current_len + temp_len + 1;
        char *test_alloc = (char*)realloc(full_string, new_len);
        if(test_alloc == NULL)
        {
            printf("Unable to allocate memory for string.\n");
            // Just break here, since we still have to free full_string.
            break;
        }

        full_string = test_alloc;
        // We copy the small string at the end of the larger one.
        strcpy(full_string + current_len, temp);
        current_len += temp_len;
        if(temp[temp_len - 1] == '\n' || feof(fp))
        {
            // Success! We encountererd either the newline or EOF.
            *len = current_len;
            return full_string;
        }
    }

    // We only get here if something went wrong.
    free(full_string);
    *len = 0;
    return NULL;
}

char* Py_VerifyFilename(const wchar_t *file_path, size_t *len)
{
    *len = wcslen(file_path);
    // We allocate space for the global path.
    char *ch_file_path = (char*)calloc(*len + 1, sizeof(char));
    printf("SET '%s' '%ls'\n", ch_file_path, file_path);
    ssize_t no_of_bytes = wcstombs(ch_file_path, file_path, sizeof(char) * (*len));
    printf("SET '%s' '%ls' %zu %zu\n", ch_file_path, file_path, no_of_bytes, *len);
    // On Windows, wchar_t and char are different length.
    #ifdef _WIN32
    if(no_of_bytes == -1)
    {
        printf(".py filenames should only contain ASCII characters when on Windows (for now).\n");
        printf("Consider renaming your .py file.\n");
        ch_file_path = Py_GetDate(len);
        printf("Output of this file will be called: \"%s.csv\"\n", ch_file_path);
        return ch_file_path;
    }
    #endif
    // We copy it, since I honestly don't know if they are altering
    // it later and it's not like it's a lot of data, so I just want to 
    // make sure that this doesn't result in some annoying bug.
    return ch_file_path;
}

char *Py_GetDate(size_t *len)
{
    int buf_size = 100; // Date won't exceed this size.
    char *date_str = (char*)calloc(buf_size, sizeof(char));
    if(date_str == NULL)
    {
        printf("Unable to allocate memory for string.\n");
    }
    time_t t = time(NULL);
    // The file name is "YYYY_MM_DD_HH_MM_SS_BCC at this point. We add the ".csv" later.
    *len = strftime(date_str, buf_size-1, "%Y_%m_%d_%H_%M_%S_BCC", localtime(&t));
    return date_str;
}

char *Py_GetFilename(const wchar_t *filename_path, size_t *len)
{
    // When running the Python in REPL mode, or when building the project
    // the filename might not get set. We therefore simply give it the time 
    // time as the filename.
    if(filename_path == NULL)
    {
        return Py_GetDate(len);
    }

    char *filename = Py_VerifyFilename(filename_path, len);
    filename += *len - 1;
    while(*(filename-1) != PATH_SEP[0] && *len > 0)
    {
        filename--;
        (*len)--;
    }
    return filename;
}

char *Py_GetBCPath(size_t *len)
{
    FILE *fp;
    fp = fopen(BCC_Txt_Path, "r");
    if(fp == NULL)
    {
        printf("Unable to access bcc.txt at path: %s\n.", BCC_Txt_Path);
        return NULL;
    }

    // This can be NULL. We don't check for that here.
    char *BCC_Path = Py_GetLine(fp, len);
    fclose(fp);
    return BCC_Path;
}

char *Py_GetBCFullPath(char *filename, size_t filename_len, size_t *out_len)
{
    size_t dir_path_len;
    char *path_str = Py_GetBCPath(&dir_path_len);
    if(path_str == NULL)
    {
        return NULL;
    }

    // Calculate the size of the full path and allocate space for the full path.
    // Length of directory + length of filename +  1 for null terminator.
    *out_len = dir_path_len + filename_len + 1;
    char *new_path_str = (char*)realloc(path_str, (*out_len) * sizeof(char) + 1);
    if(new_path_str == NULL)
    {
        printf("Unable to allocate memory to create path string: %s\n", path_str);
        *out_len = 0;
        free(path_str);
        return NULL;
    }

    path_str = new_path_str;

    // Concatenate the directory path, file name.
    strcat(path_str, filename);
    return path_str;
}

int Py_WriteByteCodes(void)
{
    // We add four to accomodate the ".csv". This length already accomodates a '\0' terminator.
    size_t path_str_len = strlen(output_file_path);
    char *path_str = (char*)realloc(output_file_path, path_str_len + 4);
    if(path_str == NULL)
    {
        printf("Unable to allocate memory to create \".csv\" path string.\n");
        free(path_str);
        return 1;
    }
    strcat(path_str, ".csv");

    FILE *fp; 
    fp = fopen(path_str, "w");
    if(fp == NULL)
    {
        printf("Unable to open file at path: %s\n", path_str);
        free(path_str);
        return 1;
    }
    free(path_str);

    // Write header to .csv file.
    fprintf(fp, "bytecode,count\n");
    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        // Write bytecode and counts to .csv file.
        fprintf(fp, "%d,%llu\n", i, bcc_arr[i]);
    }

    fclose(fp);
    return 0;
}

int Py_SaveBytecodeTimings(BC_timing timing)
{
    printf("Before\n");
    if(!BCT_buffer.is_init)
    {
        wchar_t *testo = L"a";
        printf("After %ls\n", testo);
        Py_Init_BCT(testo);
        printf("Afte2r\n");
    }
    printf("OKOKOK\n");
    if(timing.opcode > BCC_ARR_SIZE - 1 || timing.opcode < 0)
    {
        printf("Invalid opcode: %d\n", timing.opcode);
    }
    else
    {
        BCT_buffer.cur_size++;
        if(BCT_buffer.cur_size > BCT_BUFFER_SIZE - 1)
        {
            printf("SRSLY? %d\n", BCT_buffer.is_init);
            if(Py_WriteByteCodeTimings(BCT_buffer))
            {
                printf("???\n");
                BCT_buffer.cur_size = 0;
                return 1;
            }
            printf("PRE\n");
            BCT_buffer.cur_size = 0;
            printf("POST\n");
        }
        BCT_buffer.buffer[BCT_buffer.cur_size] = timing;
        
    }
    return 0;
}

char *Py_GetBCTPath(char *filename, size_t len)
{
    size_t path_str_len;
    char *path_str = Py_GetBCFullPath(filename, len, &path_str_len);
    if(path_str == NULL)
    {
        len = 0;
        return NULL;
    }
    else
    {
        // We add four to accomodate the ".BCT". This length already accomodates a '\0' terminator.
        path_str_len += 4;
        char *new_path_str = (char*)realloc(path_str, (path_str_len * sizeof(char)) + 1);
        if(new_path_str == NULL)
        {
            printf("Unable to allocate memory to create \".BCT\" path string.\n");
            free(path_str);
            return NULL;
        }

        path_str = new_path_str;
        strcat(path_str, ".BCT");
        return path_str;
    }
}

int Py_WriteByteCodeTimings(BC_timings_buffer BCT_buffer)
{
    printf("INSIDE\n");
    if(output_file_path == NULL)
    {
        printf("Unable to get path for BCT file.\n");
        free(output_file_path);
        return 1;
    }

    FILE *fp;
    fp = fopen(output_file_path, "a");
    printf("%s", output_file_path);
    if(fp == NULL)
    {
        printf("Unable to open BCT file at path. \"%s\".\n", output_file_path);
        free(output_file_path);
        return 1;
    }

    int opcode;
    long nsec;
    for(size_t i = 0; i < BCT_buffer.cur_size; i++)
    {
        opcode = BCT_buffer.buffer[i].opcode;
        nsec = BCT_buffer.buffer[i].nsec_dur;
        fprintf(fp, "%d:%ld\n", opcode, nsec);
    }

    fclose(fp);
    return 0;
}

int Py_Init_BCT(const wchar_t *file_path)
{
    // TODO, why does it segfault on the call to this function???
    printf("INIT\n");
    // TODO move this into a seperate function.
    #ifdef _WIN32
    #else
        struct timespec temp;
        clock_getres(BCT_CLOCK, &temp);
        long frequency = BILLION / temp.tv_nsec;
    #endif
    BC_timings_buffer buffer = 
    {
        .frequency = frequency,
        .cur_size = 0,
        .is_init = 1
    };

    BCT_buffer = buffer;

    if(file_path == NULL)
    {
        return 1;
    }

    printf("IN INIT FILE PATH: %ls\n", file_path);
    size_t len;
    char *filename = Py_GetFilename(file_path, &len);
    output_file_path = Py_GetBCTPath(filename, len);
    if(output_file_path == NULL)
    {
        return 1;
    }
    
    FILE *fp;
    fp = fopen(output_file_path, "w");
    if(fp == NULL)
    {
        printf("Unable to open BCT file at path. \"%s\".\n", output_file_path);
        return 1;
    }

    fprintf(fp, "Timing metric in ns:\n%ld\nBytecodetimings:\n", BCT_buffer.frequency);
    fclose(fp);
    return 0;
}

int Py_Exit_BCT(void)
{
    // During building the project, we only want to write to file if 
    // Py_Init_BCT has been run.
    // If we do not test for this here, then building the project will fail.
    // TOOD, figure out a better place to call Py_Init_BCT
    if(BCT_buffer.is_init)
    {
        return Py_WriteByteCodeTimings(BCT_buffer);
    }
    return 1;
}