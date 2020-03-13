#ifndef BYTE_CODE_COUNTER_H
#define BYTE_CODE_COUNTER_H

// TODO Find out how to include opcode.h and use it to determine the BCC arr size.
#define BCC_ARR_SIZE 258//EXCEPT_HANDLER+1
unsigned long long bcc_arr[];

void Py_PrintByteCodes();

int Py_WriteByteCodes(char *path);

//TODO add increment function or macro for opcode counting

#endif /* BYTE_CODE_COUNTER_H */