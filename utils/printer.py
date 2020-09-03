import sys

def ow_print(*args, sep=' ', file = sys.stdout, flush = False):
    # TODO if the line goes beyond the size of the terminal size, the cariage return causes is only to go back to the beginning on the line, not the beginning of the previous string.
    print_str = ""
    for arg in args[:-1]:
        print_str += str(arg) + sep
    print_str += str(args[-1])
    new_len = len(print_str)
    whitespace_len = ow_print.ow_len - new_len
    if whitespace_len > 0 :
        print(print_str, " " * whitespace_len, sep = sep, end = '\r', file = file, flush = flush)
    else:
        print(print_str, sep = sep, end = '\r', file = file, flush = flush)
    ow_print.ow_len = new_len

ow_print.ow_len = 0