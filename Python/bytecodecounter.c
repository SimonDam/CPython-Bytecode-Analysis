#include "bytecodecounter.h"
#include "stdio.h"

unsigned long long bcc_arr[BCC_ARR_SIZE];

void Py_PrintByteCodes()
{
    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        printf("%d:%llu\n", i, bcc_arr[i]);
    }
    return 0;
}

int Py_WriteByteCodes(char *path_str)
{
    FILE *fp; 
    errno_t err = fopen_s(&fp, path_str, "w");
    if(err != 0)
    {
        printf("Unable to open file at path: %s\n", path_str);
        return 0;
    }

    for(int i = 0; i < BCC_ARR_SIZE; i++)
    {
        fprintf(fp, "%d:%llu\n", i, bcc_arr[i]);
    }

    fclose(fp);
    return 1;
}
