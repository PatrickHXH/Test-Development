from  cases.models import TestExtract

def get_replace_string(s):
    if  "^{" and "}$" in s:
        s_left = s.split("^{")[0]
        s_right = s.split("^{")[1]
        print(s_right)
        s2_left = s_right.split("}$")[0]
        s2_right = s_right.split("}$")[1]
        print(s2_left)
        extract = TestExtract.objects.get(name=s2_left)
        ss=extract.vlue
        s_string = f"{s_left}{ss}{s2_right}"
        return s_string
    else:
        return s

# get_replace_string("http://^{Host}$")