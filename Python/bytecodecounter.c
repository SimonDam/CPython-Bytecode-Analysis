#include <Python.h>
#include <opcode.h>
#include <stdbool.h>
#include "bytecodecounter.h"

char* byte_code_name_mapper(ByteCodeCounter bcc){
    char *return_string = (char*)calloc(COUNTER_ARRAY_SIZE * OP_CODE_NAME_MAX_SIZE, sizeof(char));
    char *tmp_opcode;
    char opcode[OP_CODE_NAME_MAX_SIZE];
    char opcode_str[OP_CODE_VAL_MAX_SIZE];
    char opcode_count_str[OP_CODE_COUNT_MAX_SIZE];

    for (int opcode_int = 0; opcode_int < COUNTER_ARRAY_SIZE; opcode_int++) {
        tmp_opcode = getopcodename(opcode_int);
        if (tmp_opcode) {
            strcpy(opcode, tmp_opcode);
            snprintf(opcode_str, OP_CODE_VAL_MAX_SIZE, "%d ", opcode_int);
            strcat(opcode_str, opcode);
            snprintf(opcode_count_str, OP_CODE_COUNT_MAX_SIZE, " %d\n", bcc.OpCodeCounts[opcode_int]);
            strcat(opcode_str, opcode_count_str);
            strcat(return_string, opcode_str);
        }
    }

    return return_string;
}

char* getopcodename(int opcode) {
    switch (opcode) {
        case POP_TOP:
            return "POP_TOP";
        
        case ROT_TWO:
            return "ROT_TWO";
        
        case ROT_THREE:
            return "ROT_THREE";
        
        case DUP_TOP:
            return "DUP_TOP";
        
        case DUP_TOP_TWO:
            return "DUP_TOP_TWO";
        
        case ROT_FOUR:
            return "ROT_FOUR";
        
        case NOP:
            return "NOP";
        
        case UNARY_POSITIVE:
            return "UNARY_POSITIVE";
        
        case UNARY_NEGATIVE:
            return "UNARY_NEGATIVE";
        
        case UNARY_NOT:
            return "UNARY_NOT";
        
        case UNARY_INVERT:
            return "UNARY_INVERT";
        
        case BINARY_MATRIX_MULTIPLY:
            return "BINARY_MATRIX_MULTIPLY";
        
        case INPLACE_MATRIX_MULTIPLY:
            return "INPLACE_MATRIX_MULTIPLY";
        
        case BINARY_POWER:
            return "BINARY_POWER";
        
        case BINARY_MULTIPLY:
            return "BINARY_MULTIPLY";
        
        case BINARY_MODULO:
            return "BINARY_MODULO";
        
        case BINARY_ADD:
            return "BINARY_ADD";
        
        case BINARY_SUBTRACT:
            return "BINARY_SUBTRACT";
        
        case BINARY_SUBSCR:
            return "BINARY_SUBSCR";
        
        case BINARY_FLOOR_DIVIDE:
            return "BINARY_FLOOR_DIVIDE";
        
        case BINARY_TRUE_DIVIDE:
            return "BINARY_TRUE_DIVIDE";
        
        case INPLACE_FLOOR_DIVIDE:
            return "INPLACE_FLOOR_DIVIDE";
        
        case INPLACE_TRUE_DIVIDE:
            return "INPLACE_TRUE_DIVIDE";
        
        case GET_AITER:
            return "GET_AITER";
        
        case GET_ANEXT:
            return "GET_ANEXT";
        
        case BEFORE_ASYNC_WITH:
            return "BEFORE_ASYNC_WITH";
        
        case BEGIN_FINALLY:
            return "BEGIN_FINALLY";
        
        case END_ASYNC_FOR:
            return "END_ASYNC_FOR";
        
        case INPLACE_ADD:
            return "INPLACE_ADD";
        
        case INPLACE_SUBTRACT:
            return "INPLACE_SUBTRACT";
        
        case INPLACE_MULTIPLY:
            return "INPLACE_MULTIPLY";
        
        case INPLACE_MODULO:
            return "INPLACE_MODULO";
        
        case STORE_SUBSCR:
            return "STORE_SUBSCR";
        
        case DELETE_SUBSCR:
            return "DELETE_SUBSCR";
        
        case BINARY_LSHIFT:
            return "BINARY_LSHIFT";
        
        case BINARY_RSHIFT:
            return "BINARY_RSHIFT";
        
        case BINARY_AND:
            return "BINARY_AND";
        
        case BINARY_XOR:
            return "BINARY_XOR";
        
        case BINARY_OR:
            return "BINARY_OR";
        
        case INPLACE_POWER:
            return "INPLACE_POWER";
        
        case GET_ITER:
            return "GET_ITER";
        
        case GET_YIELD_FROM_ITER:
            return "GET_YIELD_FROM_ITER";
        
        case PRINT_EXPR:
            return "PRINT_EXPR";
        
        case LOAD_BUILD_CLASS:
            return "LOAD_BUILD_CLASS";
        
        case YIELD_FROM:
            return "YIELD_FROM";
        
        case GET_AWAITABLE:
            return "GET_AWAITABLE";
        
        case INPLACE_LSHIFT:
            return "INPLACE_LSHIFT";
        
        case INPLACE_RSHIFT:
            return "INPLACE_RSHIFT";
        
        case INPLACE_AND:
            return "INPLACE_AND";
        
        case INPLACE_XOR:
            return "INPLACE_XOR";
        
        case INPLACE_OR:
            return "INPLACE_OR";
        
        case WITH_CLEANUP_START:
            return "WITH_CLEANUP_START";
        
        case WITH_CLEANUP_FINISH:
            return "WITH_CLEANUP_FINISH";
        
        case RETURN_VALUE:
            return "RETURN_VALUE";
        
        case IMPORT_STAR:
            return "IMPORT_STAR";
        
        case SETUP_ANNOTATIONS:
            return "SETUP_ANNOTATIONS";
        
        case YIELD_VALUE:
            return "YIELD_VALUE";
        
        case POP_BLOCK:
            return "POP_BLOCK";
        
        case END_FINALLY:
            return "END_FINALLY";
        
        case POP_EXCEPT:
            return "POP_EXCEPT";
        
        case STORE_NAME:            //STORE_NAME and HAVE_ARGUMENT use the same opcode
            return "HAVE_ARGUMENT STORE_NAME";    //Therefore return both.
        
        case DELETE_NAME:
            return "DELETE_NAME";
        
        case UNPACK_SEQUENCE:
            return "UNPACK_SEQUENCE";
        
        case FOR_ITER:
            return "FOR_ITER";
        
        case UNPACK_EX:
            return "UNPACK_EX";
        
        case STORE_ATTR:
            return "STORE_ATTR";
        
        case DELETE_ATTR:
            return "DELETE_ATTR";
        
        case STORE_GLOBAL:
            return "STORE_GLOBAL";
        
        case DELETE_GLOBAL:
            return "DELETE_GLOBAL";
        
        case LOAD_CONST:
            return "LOAD_CONST";
        
        case LOAD_NAME:
            return "LOAD_NAME";
        
        case BUILD_TUPLE:
            return "BUILD_TUPLE";
        
        case BUILD_LIST:
            return "BUILD_LIST";
        
        case BUILD_SET:
            return "BUILD_SET";
        
        case BUILD_MAP:
            return "BUILD_MAP";
        
        case LOAD_ATTR:
            return "LOAD_ATTR";
        
        case COMPARE_OP:
            return "COMPARE_OP";
        
        case IMPORT_NAME:
            return "IMPORT_NAME";
        
        case IMPORT_FROM:
            return "IMPORT_FROM";
        
        case JUMP_FORWARD:
            return "JUMP_FORWARD";
        
        case JUMP_IF_FALSE_OR_POP:
            return "JUMP_IF_FALSE_OR_POP";
        
        case JUMP_IF_TRUE_OR_POP:
            return "JUMP_IF_TRUE_OR_POP";
        
        case JUMP_ABSOLUTE:
            return "JUMP_ABSOLUTE";
        
        case POP_JUMP_IF_FALSE:
            return "POP_JUMP_IF_FALSE";
        
        case POP_JUMP_IF_TRUE:
            return "POP_JUMP_IF_TRUE";
        
        case LOAD_GLOBAL:
            return "LOAD_GLOBAL";
        
        case SETUP_FINALLY:
            return "SETUP_FINALLY";
        
        case LOAD_FAST:
            return "LOAD_FAST";
        
        case STORE_FAST:
            return "STORE_FAST";
        
        case DELETE_FAST:
            return "DELETE_FAST";
        
        case RAISE_VARARGS:
            return "RAISE_VARARGS";
        
        case CALL_FUNCTION:
            return "CALL_FUNCTION";
        
        case MAKE_FUNCTION:
            return "MAKE_FUNCTION";
        
        case BUILD_SLICE:
            return "BUILD_SLICE";
        
        case LOAD_CLOSURE:
            return "LOAD_CLOSURE";
        
        case LOAD_DEREF:
            return "LOAD_DEREF";
        
        case STORE_DEREF:
            return "STORE_DEREF";
        
        case DELETE_DEREF:
            return "DELETE_DEREF";
        
        case CALL_FUNCTION_KW:
            return "CALL_FUNCTION_KW";
        
        case CALL_FUNCTION_EX:
            return "CALL_FUNCTION_EX";
        
        case SETUP_WITH:
            return "SETUP_WITH";
        
        case EXTENDED_ARG:
            return "EXTENDED_ARG";
        
        case LIST_APPEND:
            return "LIST_APPEND";
        
        case SET_ADD:
            return "SET_ADD";
        
        case MAP_ADD:
            return "MAP_ADD";
        
        case LOAD_CLASSDEREF:
            return "LOAD_CLASSDEREF";
        
        case BUILD_LIST_UNPACK:
            return "BUILD_LIST_UNPACK";
        
        case BUILD_MAP_UNPACK:
            return "BUILD_MAP_UNPACK";
        
        case BUILD_MAP_UNPACK_WITH_CALL:
            return "BUILD_MAP_UNPACK_WITH_CALL";
        
        case BUILD_TUPLE_UNPACK:
            return "BUILD_TUPLE_UNPACK";
        
        case BUILD_SET_UNPACK:
            return "BUILD_SET_UNPACK";
        
        case SETUP_ASYNC_WITH:
            return "SETUP_ASYNC_WITH";
        
        case FORMAT_VALUE:
            return "FORMAT_VALUE";
        
        case BUILD_CONST_KEY_MAP:
            return "BUILD_CONST_KEY_MAP";
        
        case BUILD_STRING:
            return "BUILD_STRING";
        
        case BUILD_TUPLE_UNPACK_WITH_CALL:
            return "BUILD_TUPLE_UNPACK_WITH_CALL";
        
        case LOAD_METHOD:
            return "LOAD_METHOD";
        
        case CALL_METHOD:
            return "CALL_METHOD";
        
        case CALL_FINALLY:
            return "CALL_FINALLY";
        
        case POP_FINALLY:
            return "POP_FINALLY";
        
        case EXCEPT_HANDLER:
            return "EXCEPT_HANDLER";
        
        default:
            return NULL; 
    }
}

ByteCodeCounter newByteCodeCounter(){
    ByteCodeCounter bcc;
    bcc.OpCodeCounts = (int*) calloc(COUNTER_ARRAY_SIZE, sizeof(int));
    return bcc;
}
