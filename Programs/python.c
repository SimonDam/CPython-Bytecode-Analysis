/* Minimal main program -- everything is loaded from the library */

#include "Python.h"
#include "pycore_pylifecycle.h"
#include <locale.h>

#ifdef MS_WINDOWS
int
wmain(int argc, wchar_t **argv)
{
    setlocale(LC_ALL, "");
    printf("wmain argc: %d\n", argc);
    printf("wmain argv: %ls\n", *(argv+1));
    return Py_Main(argc, argv);
}
#else
int
main(int argc, char **argv)
{
    return Py_BytesMain(argc, argv);
}
#endif
