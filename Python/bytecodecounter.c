#include "bytecodecounter.h"
#include "Python.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <wchar.h>

unsigned long long bcc_arr[BCC_ARR_SIZE];

static wchar_t *input_file_path;

static const wchar_t BCC_Txt_Path[BCC_TXT_PATH_LEN] = L"."PATH_SEP"bcc.txt";

void Py_PrintByteCodes(void)
{
    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        printf("%d,%llu\n", i, bcc_arr[i]);
    }
}

wchar_t *Py_GetLine(FILE *fp)
{
    size_t current_len = 0;
    wchar_t *full_string = NULL;
    wchar_t temp[100];
    
    while(fgetws(temp, sizeof(temp), fp))
    {
        // Start by getting the length of the string.
        size_t temp_len = wcslen(temp);

        // In case full_length is about to overflow.
        if(SIZE_MAX - temp_len - 1 < current_len)
        {
            printf("Unusually large size read while reading from file (%zu).", current_len);
            // Just break here, since we still have to free full_string.
            break;
        }
        size_t new_len = current_len + temp_len + 1;
        wchar_t *test_alloc = (wchar_t*)realloc(full_string, new_len);
        if(test_alloc == NULL)
        {
            printf("Unable to allocate memory for string.");
            // Just break here, since we still have to free full_string.
            break;
        }

        full_string = test_alloc;
        // We copy the small string at the end of the larger one.
        wcscpy_s(full_string + current_len, temp_len + 1, temp);

        if(temp[temp_len - 1] == "\n" || feof(fp))
        {
            // Success! We encountererd either the newline or EOF.
            printf("FULLESTRING %ls", full_string);
            return full_string;
        }

        current_len += temp_len;
    }

    // We only get here if something went wrong.
    free(full_string);
    return NULL;
}

void Py_SetFilename(const wchar_t *file_path)
{
    // TODO add conversion from wchar_t to char here.
    input_file_path = calloc(wcslen(file_path)+1, sizeof(wchar_t));
    wcscpy(input_file_path, file_path);
}

wchar_t *Py_GetFilename(void)
{
    wchar_t *file_name = input_file_path;
    size_t inp_file_path_len = wcslen(input_file_path);

    file_name += inp_file_path_len - 1;
    while(*(file_name-1) != PATH_SEP[0] && file_name != input_file_path)
    {
        file_name--;
    }
    return file_name;
}

wchar_t *Py_GetBCCPath(void)
{
    FILE *fp;
    printf("HERE???");
    errno_t err = _wfopen_s(&fp, BCC_Txt_Path, "r, ccs=encoding");
    printf("!!!!");
    if(err != 0)
    {
        printf("Unable to access bcc.txt at path: %ls\n", BCC_Txt_Path);
        return NULL;
    }
    printf("HERE");

    // This can be NULL. We don't check for that here.
    wchar_t *BCC_Path = Py_GetLine(fp);
    fclose(fp);
    return BCC_Path;
}

int Py_WriteByteCodes(void)
{
    printf("1");
    wchar_t *path_str = Py_GetBCCPath();
    printf("1.5");
    if(*path_str == NULL)
    {
        printf("Please specify a directorypath in BCC.txt to write the BCC files to.\n");
        printf("No files where written, dumping BCC's to terminal:\n");
        Py_PrintByteCodes();
        return 0;
    }
    printf("2");
    wchar_t *file_name = Py_GetFilename();
    printf("3");
    // Calcualte the size of the full path and allocate space for the full path.
    size_t path_len = wcslen(path_str) + wcslen(file_name) + 1;
    path_str = (wchar_t*)realloc(path_str, path_len * sizeof(wchar_t));
    if(path_str == NULL)
    {
        printf("Unable to allocate memory to create path string: %ls\n", path_str);
        free(path_str);
        return 0;
    }

    // Combine the directory path and file name.
    wcscat_s(path_str, path_len * sizeof(wchar_t), file_name);

    FILE *fp; 
    errno_t err = _wfopen_s(&fp, path_str, "w, ccs=encoding");
    if(err != 0)
    {
        printf("Unable to open file at path: %ls\n", path_str);
        free(path_str);
        return 0;
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
    return 1;
}

