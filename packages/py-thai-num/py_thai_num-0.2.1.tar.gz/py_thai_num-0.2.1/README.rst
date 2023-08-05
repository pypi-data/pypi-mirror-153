Project
===============
python lib for conversion Thai numerical to global numerical

Installing
============

    pip install py_thai_num

Usage
=====

    >>> from thai_to_int import py_thai_num
    >>> thai_to_int("1234")
    1234

Function list
=====

py_thai_num:

    int_ret = to_int(str_in)
    str_ret = to_str(str_in)
    ch_ret = to_char(ch_in)

file_thai_num:

    str_ret = to_str(file_in)
    to_char(file_in, file_out)