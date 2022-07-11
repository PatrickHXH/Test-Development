def get_replace_string(s):
    if  "^{" and "}$" in s:
        s_left = s.split("^{")[0]
        s_right = s.split("^{")[1]
        print(s_right)
        s2_left = s_right.split("}$")[0]
        s2_right = s_right.split("}$")[1]
        print(s2_left)
        url = "www.baidu.com"
        s_string = s_left + url + s2_right
        print(s_string)

get_replace_string("^{token}$")