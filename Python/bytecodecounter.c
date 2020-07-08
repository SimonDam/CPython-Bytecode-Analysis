#include "bytecodecounter.h"
#include "stdio.h"
#include <windows.h>

unsigned long long bcc_arr[BCC_ARR_SIZE];

void Py_PrintByteCodes()
{
    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        printf("%d,%llu\n", i, bcc_arr[i]);
    }
}

size_t Py_GetBCCPath(char *buffer, size_t *len)
{
    FILE *path_file; 
    errno_t path_file_err = fopen_s(&path_file, ".\\bcc.txt", "r");
    if(path_file_err != 0)
    {
        printf("\"bcc.txt\" could not be found\n.");
        return 0;
    }
    size_t characters = getline(&buffer, &len, path_file);
    fclose(path_file);
    return characters;
}

int Py_WriteByteCodes()
{
    char *path_str = NULL;
    size_t len = 0;

    Py_GetBCCPath(&path_str, &len);

    FILE *fp; 
    errno_t err = fopen_s(&fp, path_str, "w");
    if(err != 0)
    {
        printf("Unable to open file at path: %s\n", path_str);
        return 0;
    }

    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        printf("T\n");
        fprintf(path_str, "%d:%llu\n", i, bcc_arr[i]);
    }
    free(path_str);

    fclose(fp);
    return 1;
}
