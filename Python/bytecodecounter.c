#include "bytecodecounter.h"
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

unsigned long long bcc_arr[BCC_ARR_SIZE];

void Py_PrintByteCodes()
{
    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        printf("%d,%llu\n", i, bcc_arr[i]);
    }
}

char *Py_GetLine(FILE *fp)
{
    size_t current_len = 0;
    char *full_string = NULL;
    char temp[100];

    while(fgets(temp, sizeof(temp), fp))
    {
        // Start by getting the length of the string.
        size_t temp_len = strlen(temp);

        // In case full_length is about to overflow.
        if(SIZE_MAX - temp_len - 1 < current_len)
        {
            printf("Unusually large size read while reading from file (%zu).", current_len);
            // Just break here, since we still have to free full_string.
            break;
        }
        size_t new_len = current_len + temp_len + 1;
        char *test_alloc = (char *)realloc(full_string, new_len);
        if(test_alloc == NULL)
        {
            printf("Unable to allocate memory for string.");
            // Just break here, since we still have to free full_string.
            break;
        }

        full_string = test_alloc;
        // We copy the small string, into the larger one.
        strcpy_s(full_string + current_len, temp_len + 1, temp);

        if(temp[temp_len - 1] == "\n" || feof(fp))
        {
            // Success! We encountererd either the newline or EOF.
            return full_string;
        }

        current_len += temp_len;
    }

    // We only get here if something went wrong.
    free(full_string);
    return NULL;
}

char *Py_GetBCCPath()
{
    FILE *fp;
    errno_t err = fopen_s(&fp, ".\\bcc.txt", "r");
    if(err != 0)
    {
        printf("Unable to bcc.txt at path: %s\n", ".\\bcc.txt");
        return NULL;
    }

    // This can be NULL. We don't check for that here.
    char *BCCPath = Py_GetLine(fp);
    fclose(fp);
    return BCCPath;
}

int Py_WriteByteCodes()
{
    char *path_str = Py_GetBCCPath();
    if(*path_str == NULL)
    {
        printf("Please specify a directorypath in BCC.txt to write the BCC files to.\n");
        printf("No files where written, dumping BCC's to terminal:\n");
        Py_PrintByteCodes();
        return 0;
    }

    char *file_name = "test.csv"; //TODO Get the filename from the input arguments.

    // Calcualte the size of the full path and allocate space for the full path.
    size_t path_len = strlen(path_str) + strlen(file_name) + 1;
    path_str = (char*)realloc(path_str, path_len * sizeof(char));
    if(path_str == NULL)
    {
        printf("Unable to allocate memory to create path string: %s\n", path_str);
        free(path_str);
        return 0;
    }

    // Combine the directory path and file name.
    strcat_s(path_str, path_len * sizeof(char), file_name);

    FILE *fp; 
    errno_t err = fopen_s(&fp, path_str, "w");
    if(err != 0)
    {
        printf("Unable to open file at path: %s\n", path_str);
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
