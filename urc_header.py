from sys import stdin, stdout, stderr

urc_headers = {}
urc_headers["`byte_to_hexstr"] = "DEF_BYTE_TO_HEXSTR"
urc_headers["`char_code_at"] = "DEF_CHAR_CODE_AT"
urc_headers["`chr_cr"] = "DEF_CHR_CR"
urc_headers["`chr_lf"] = "DEF_CHR_LF"
urc_headers["`chr_quote"] = "DEF_CHR_QUOTE"
urc_headers["`chr_tab"] = "DEF_CHR_TAB"
urc_headers["`concat"] = "DEF_CONCAT"
urc_headers["`delete"] = "DEF_DELETE"
urc_headers["`endswith"] = "DEF_ENDSWITH"
urc_headers["`get_type"] = "DEF_GET_TYPE"
urc_headers["`indexof"] = "DEF_INDEXOF"
urc_headers["`isnull"] = "DEF_ISNULL"
urc_headers["`is_type_bool"] = "DEF_IS_TYPE_BOOL"
urc_headers["`is_type_dict"] = "DEF_IS_TYPE_DICT"
urc_headers["`is_type_list"] = "DEF_IS_TYPE_LIST"
urc_headers["`is_type_null"] = "DEF_IS_TYPE_NULL"
urc_headers["`is_type_num"] = "DEF_IS_TYPE_NUM"
urc_headers["`is_type_str"] = "DEF_IS_TYPE_STR"
urc_headers["`length"] = "DEF_LENGTH"
urc_headers["`lowercase"] = "DEF_LOWERCASE"
urc_headers["`math_atan2"] = "DEF_MATH_ATAN2"
urc_headers["`math_cos"] = "DEF_MATH_COS"
urc_headers["`math_log10"] = "DEF_MATH_LOG10"
urc_headers["`math_pi"] = "DEF_MATH_PI"
urc_headers["`math_sin"] = "DEF_MATH_SIN"
urc_headers["`math_sqrt"] = "DEF_MATH_SQRT"
urc_headers["`not"] = "DEF_NOT"
urc_headers["`parse_int"] = "DEF_PARSE_INT"
urc_headers["`pick"] = "DEF_PICK"
urc_headers["`poke"] = "DEF_POKE"
urc_headers["`pop"] = "DEF_POP"
urc_headers["`push"] = "DEF_PUSH"
urc_headers["`queue"] = "DEF_QUEUE"
urc_headers["`random"] = "DEF_RANDOM"
urc_headers["`int32"] = "DEF_SIGNED_32BITS"
urc_headers["`uint32"] = "DEF_UNSIGNED_32BITS"
urc_headers["`split"] = "DEF_SPLIT"
urc_headers["`startswith"] = "DEF_STARTSWITH"
urc_headers["`str"] = "DEF_STR"
urc_headers["`strip"] = "DEF_STRIP"
urc_headers["`str_constants"] = "DEF_STR_CONSTANTS"
urc_headers["`substring"] = "DEF_SUBSTRING"
urc_headers["`ternary"] = "DEF_TERNARY"
urc_headers["`trunc"] = "DEF_TRUNC"
urc_headers["`unqueue"] = "DEF_UNQUEUE"
urc_headers["`uppercase"] = "DEF_UPPERCASE"
urc_headers["`warning"] = "DEF_WARNING"

if __name__ == '__main__':
    headers = []
    headers_missing = []
    for k in urc_headers:
        headers_missing.append(k)
    lines = []
    line = stdin.readline()
    while len(line) > 0:
        lines.append(line)
        line = stdin.readline()
    for line in lines:
        headers_found = []
        for h in headers_missing:
            sps = line.split(h)
            for j in range(1, len(sps)):
                if (len(sps[j]) > 0) and sps[j][0].isalnum(): continue
                headers_found.append(h)
                break
        if ("`str_constants" in headers_missing) and (line.count('"') > 0):
            headers_found.append("`str_constants")
        elif len(headers_found) == 0: continue
        for h in headers_found:
            headers.append(h)
            headers_missing.remove(h)
        if len(headers_missing) == 0: break
    for h in headers:
        print(urc_headers[h]+" "+h, file=stdout)
