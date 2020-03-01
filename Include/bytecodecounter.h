#ifndef BYTECODECOUNTER_H
#define BYTECODECOUNTER_H

#define COUNTER_ARRAY_SIZE 258
#define OP_CODE_NAME_MAX_SIZE 100
#define OP_CODE_VAL_MAX_SIZE 4 //Three characters for the opcode and one for the null terminator.
#define OP_CODE_COUNT_MAX_SIZE 12 //Allow for 10^12 sized numbers.
typedef struct {
    int *OpCodeCounts; //Each entry is a counter for a bytecode.
                                          //Some bytecodes values are not used, so their values are 0.
} ByteCodeCounter;

char* getopcodename(int opcode);
char* byte_code_name_mapper(ByteCodeCounter bcc);
ByteCodeCounter newByteCodeCounter();
#endif