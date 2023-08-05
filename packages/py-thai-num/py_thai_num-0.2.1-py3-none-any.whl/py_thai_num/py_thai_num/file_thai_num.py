from py_thai_num import py_thai_num

def to_str(file_name):
    tmp_str = ""
    tmp_f = open(file_name, "r")
    while 1:
    
        # read by character
        tmp_ch = tmp_f.read(1)         
        if not tmp_ch:
            break
        tmp_str = tmp_str + py_thai_num.to_char(tmp_ch)
        
    tmp_f.close()

    return tmp_str

def to_file(file_in, file_out):
    
    tmp_f = open(file_in, "r")
    tmp_fo = open(file_out, "w")
    while 1:
    
        # read by character
        tmp_ch = tmp_f.read(1)         
        if not tmp_ch:
            break
        tmp_ch = py_thai_num.to_char(tmp_ch)
        tmp_fo.write(tmp_ch)
    
    tmp_f.close()
    tmp_fo.close()

    return 0;


