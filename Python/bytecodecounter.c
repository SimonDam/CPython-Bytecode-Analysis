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

BC_timings_buffer *_internal_timings_buffer;

// The space for this string is allocated in Py_SetFilename.
// TODO This might get freed at some point and therefore reallocated.
static char *input_file_path;

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

        if(temp[temp_len - 1] == '\n' || feof(fp))
        {
            // Success! We encountererd either the newline or EOF.
            *len = current_len;
            return full_string;
        }

        current_len += temp_len;
    }

    // We only get here if something went wrong.
    free(full_string);
    *len = 0;
    return NULL;
}

void Py_SetFilename(const wchar_t *file_path)
{
    int file_path_len = wcslen(file_path);
    // We allocate space for the global path.
    input_file_path = (char*)calloc(file_path_len + 1, sizeof(char));
    
    for(int i = 0; i < file_path_len; i++)
    {
        wchar_t cur_wchar = *(file_path + i);

        // On Windows, wchar_t and char are different length.
        #ifdef _WIN32
        if(cur_wchar > 255 || cur_wchar < 0)
        {
            printf(".py filenames should only contain ASCII characters when on Windows (for now).\n");
            printf("Consider renaming your .py file.\n");
            int buf_size = 100;
            char *new_input_file_path = (char*)realloc(input_file_path, buf_size * sizeof(char));
            if(new_input_file_path == NULL)
            {
                printf("Unable to allocate memory for string.\n");
            }
            time_t t = time(NULL);
            // The file name is "YYYY_MM_DD_HH_MM_SS_BCC at this point. We add the ".csv" later.
            strftime(input_file_path, buf_size-1, "%Y_%m_%d_%H_%M_%S_BCC", localtime(&t));
            printf("Output of this file will be called: \"%s.csv\"\n", input_file_path);
            return;
        }
        #endif
        // We copy it, since I honestly don't know if they are altering
        // it later and it's not like it's a lot of data, so I just want to 
        // make sure that this doesn't result in some annoying bug.
        // Also this is an easy to cast it to char for Windows.
        *(input_file_path + i) = (char)cur_wchar;
    }
}

char *Py_GetFilename(size_t *len)
{
    char *filename = input_file_path;
    *len = strlen(input_file_path);

    filename += *len - 1;
    while(*(filename-1) != PATH_SEP[0] && filename != input_file_path)
    {
        filename--;
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

char *Py_GetBCFullPath(size_t *len)
{
    size_t dir_path_len;
    char *path_str = Py_GetBCPath(&dir_path_len);
    if(path_str == NULL)
    {
        printf("Please specify a directorypath in bcc.txt to write the BCC files to.\n");
        return NULL;
    }
    size_t filename_len = 0;
    char *filename = Py_GetFilename(&filename_len);
    // Calculate the size of the full path and allocate space for the full path.
    // Length of directory + length of filename +  1 for null terminator.
    *len = dir_path_len + filename_len + 1;
    char* new_path_str = (char*)realloc(path_str, *len * sizeof(char));
    if(new_path_str == NULL)
    {
        printf("Unable to allocate memory to create path string: %s\n", path_str);
        *len = 0;
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
    size_t path_str_len;
    char *path_str = Py_GetBCFullPath(&path_str_len);
    // We add four to accomodate the ".csv". This length already accomodates a '\0' terminator.
    char *new_path_str = (char*)realloc(path_str, path_str_len + 4);
    if(new_path_str == NULL)
    {
        printf("Unable to allocate memory to create \".csv\" path string.\n");
        free(path_str);
        return 1;
    }
    path_str = new_path_str;
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

int Py_SaveBytecodeTimings(BC_timing timing, BC_timings_buffer *BCT_buffer)
{
    if(timing.opcode > BCC_ARR_SIZE - 1 || timing.opcode < 0)
    {
        printf("Invalid opcode: %d\n", timing.opcode);
    }
    else
    {
        BCT_buffer->buffer[BCT_buffer->cur_size] = timing;
        BCT_buffer->cur_size++;
        if(BCT_buffer->cur_size > BCT_BUFFER_SIZE - 1)
        {
            if(Py_WriteByteCodeTimings(BCT_buffer))
            {
                return 1;
            }
            BCT_buffer->cur_size = 0;
        }
    }
    return 0;
}

char *Py_GetBCTPath(size_t *len)
{
    size_t path_str_len;
    char *path_str = Py_GetBCFullPath(&path_str_len);
    if(path_str == NULL)
    {
        return NULL;
    }
    else
    {
        // We add four to accomodate the ".BCT". This length already accomodates a '\0' terminator.
        *len = path_str_len + 4;
        char *new_path_str = (char*)realloc(path_str, *len * sizeof(char));
        if(new_path_str == NULL)
        {
            printf("Unable to allocate memory to create \".BCT\" path string.\n");
            free(path_str);
            *len = 0;
            return NULL;
        }
        path_str = new_path_str;
        strcat(path_str, ".BCT");

        return path_str;
    }
}

int Py_WriteByteCodeTimings(BC_timings_buffer *BCT_buffer)
{
    size_t path_len;
    char *path_str = Py_GetBCTPath(&path_len);
    if(path_str == NULL)
    {
        printf("Unable to get path for BCT file.\n");
        free(path_str);
        return 1;
    }

    FILE *fp;
    fp = fopen(path_str, "a");
    if(fp == NULL)
    {
        printf("Unable to open BCT file at path. \"%s\".\n", path_str);
        free(path_str);
        return 1;
    }
    free(path_str);

    int opcode;
    long nsec;
    for(size_t i = 0; i < BCT_buffer->cur_size; i++)
    {
        opcode = BCT_buffer->buffer[i].opcode;
        nsec = BCT_buffer->buffer[i].nsec_dur;
        fprintf(fp, "%d:%ld\n", opcode, nsec);
    }

    fclose(fp);
    return 0;
}

int Py_Init_BCT(BC_timings_buffer *buffer)
{
    _internal_timings_buffer = buffer;
    size_t path_str_len;
    char *path_str = Py_GetBCTPath(&path_str_len);
    if(path_str == NULL)
    {
        printf("Unable to get path for BCT file.\n");
        free(path_str);
        return 1;
    }
    
    FILE *fp;
    fp = fopen(path_str, "w");
    if(fp == NULL)
    {
        printf("Unable to open BCT file at path. \"%s\".\n", path_str);
        free(path_str);
        return 1;
    }
    free(path_str);

    fprintf(fp, "Timing metric in ns:\n%ld\nBytecodetimings:\n", buffer->frequency);
    fclose(fp);
    return 0;
}