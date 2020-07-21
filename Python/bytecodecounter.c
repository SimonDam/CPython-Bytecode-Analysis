#include "bytecodecounter.h"
#include "Python.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>
#include <time.h>

#ifdef _WIN32
    #include <windows.h>
#else
    //#include <linux/hrtimer.h>
#endif

unsigned long long bcc_arr[BCC_ARR_SIZE];

// The space for this string is allocated in Py_SetFilename.
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

char *Py_GetLine(FILE *fp)
{
    size_t current_len = 0;
    char *full_string = NULL;
    char temp[20];
    
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
        char *test_alloc = (char*)realloc(full_string, new_len);
        if(test_alloc == NULL)
        {
            printf("Unable to allocate memory for string.");
            // Just break here, since we still have to free full_string.
            break;
        }

        full_string = test_alloc;
        // We copy the small string at the end of the larger one.
        strcpy(full_string + current_len, temp);

        if(temp[temp_len - 1] == '\n' || feof(fp))
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
            printf(".py filenames should only contain ASCII characters when on Windows (for now).");
            printf("Consider renaming your .py file.\n");
            int buf_size = 100;
            input_file_path = (char*)realloc(input_file_path, buf_size * sizeof(char));
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

char *Py_GetFilename(void)
{
    char *filename = input_file_path;
    size_t inp_file_path_len = strlen(input_file_path);

    filename += inp_file_path_len - 1;
    while(*(filename-1) != PATH_SEP[0] && filename != input_file_path)
    {
        filename--;
    }
    return filename;
}

char *Py_GetBCCPath(void)
{
    FILE *fp;
    fp = fopen(BCC_Txt_Path, "r");
    if(fp != NULL)
    {
        printf("Unable to access bcc.txt at path: %s\n", BCC_Txt_Path);
        return NULL;
    }

    // This can be NULL. We don't check for that here.
    char *BCC_Path = Py_GetLine(fp);
    fclose(fp);
    return BCC_Path;
}

int Py_WriteByteCodes(void)
{
    char *path_str = Py_GetBCCPath();
    if(*path_str == NULL)
    {
        printf("Please specify a directorypath in BCC.txt to write the BCC files to.\n");
        printf("No files where written, dumping BCC's to terminal:\n");
        Py_PrintByteCodes();
        return 0;
    }

    char *filename = Py_GetFilename();
    // Calculate the size of the full path and allocate space for the full path.
    // Length of directory + length of filename +  4 (".csv") + 1 for null terminator.
    size_t path_len = strlen(path_str) + strlen(filename) + 4 + 1;
    path_str = (char*)realloc(path_str, path_len * sizeof(char));
    if(path_str == NULL)
    {
        printf("Unable to allocate memory to create path string: %s\n", path_str);
        free(path_str);
        return 0;
    }

    // Concatenate the directory path, file name and ".csv".
    strcat(path_str, filename);
    strcat(path_str, ".csv");

    FILE *fp; 
    fp = fopen(path_str, "w");
    if(fp != NULL)
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

