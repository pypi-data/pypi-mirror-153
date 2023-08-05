

def to_char(char_in):
    if(char_in == '๐'):
        return "0"
    if(char_in == '๑'):
        return "1"
    if(char_in == '๒'):
        return "2"
    if(char_in == '๓'):
        return "3"
    if(char_in == '๔'):
        return "4"
    if(char_in == '๕'):
        return "5"
    if(char_in == '๖'):
        return "6"
    if(char_in == '๗'):
        return "7"
    if(char_in == '๘'):
        return "8"
    if(char_in == '๙'):
        return "9"
    return char_in

def to_str(str_in):
    tmp_str = ""
    for tmp_ch in str_in:
       tmp_str = tmp_str + to_char(tmp_ch)
    return tmp_str


def to_int(str_in):
    try:
        tmp_eng = to_str(str_in)
        return int(tmp_eng)
    except:
        return 0
    



