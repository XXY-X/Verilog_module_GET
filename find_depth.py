# File name : find_depth
# Time      : 2026-02-11
# Aothor    : Novan
# CopyRight : ZhaoPeng
import os, sys, glob, re, shutil
from datetime import datetime

DEBUG = False

# define the global varible need
all_file_list = []
cur_sep = os.path.sep
rtl_folder = 'e203_cpu_top' + cur_sep
sub_module_folder = ''
# 正则表达式的含义
# 匹配所有类似 ： xxxx #(...) xxxxx (
#                   xxxx
#                );
# 的字符段，并返回其中匹配到第一个类型
verilog_module_pattern=r"(\w+)\s*(?:#\s*\([\s\S]*?\))?\s*\w+\s*\([\s\S]*?\)\s*;"

# depth_file = 'module_depth.txt'
depth_file = 'module_depth_debug.txt'
depth_f = open(depth_file, 'w', encoding='utf-8')


def getSubModule(in_file):
    global verilog_module_pattern
    global all_file_list
    match_path = ''
    count = 0
    sub_module_list = []
    with open(in_file, 'r', encoding='utf-8') as f:
        verilog_code = f.read()
    sub_module_matches = re.findall(verilog_module_pattern, verilog_code)
    if DEBUG:
        print('debug:符合正则化表达式的值')
        print(sub_module_matches)
    for match in sub_module_matches:
        if DEBUG:
            print('debug:match')
            print(match)
        count = count + 1
        if (count == 1):
            continue
        match_path = rtl_folder + match + '.v'
        if (match == 'begin'):
            continue
        elif (match == 'module'):
            continue
        elif (match == 'else'):
            continue
        elif (match == 'STOD_COND'):
            continue
        elif (match == 'PRINTF_COND'):
            continue
        elif not os.path.exists(match_path):
            if DEBUG:
                print('debug:文件不存在')
            continue
        sub_module_list.append(match)
        all_file_list.append(match)
    return sub_module_list


def getAllModule(in_file, depth=1):
    global depth_f
    in_file_tmp = in_file
    if DEBUG:
        print('debug:提取的文件')
        print(in_file_tmp)
    sub_list = getSubModule(in_file_tmp)
    if DEBUG:
        print('debug:处理后得到的子模块列表')
        print(sub_list)
        if depth > 1:
            return
    if sub_list == []:
        return
    for index_f in sub_list:
        #子模块文件夹路径
        in_f = rtl_folder + index_f + '.v'
        sepss = '---|' * (depth - 1)
        strs = '[' + str(depth) + ']' + '  *' + sepss + str(index_f)
        print(strs)
        strs = strs + '\n'
        depth_f.write(strs)
        getAllModule(in_f, depth + 1)


def main():
    global all_file_list
    global rtl_folder
    global sub_module_folder
    global top_module
    global depth_f
    print('===========================寻找子模块层次结构脚本===========================')
    arg_count = len(sys.argv)
    if (arg_count == 1):
        print('太少参数')
        print('方式一：python find_depth.py 子模块顶层文件名')
        print('方式二：pyhton find_depth.py 子模块所在文件夹 子模块顶层文件名')
        print('=============END==============')
        return
    elif (arg_count == 2):
        print('您使用默认文件夹')
        m_f = sys.argv[1]
    elif (arg_count == 3):
        print('您使用自定义文件夹')
        rtl_folder = sys.argv[1] + cur_sep
        m_f = sys.argv[2]
    else:
        print('太多参数')
        print('方式一：python find_depth.py 子模块顶层文件名')
        print('方式二：pyhton find_depth.py 子模块所在文件夹 子模块顶层文件名')
        print('=============END==============')
        return
    #顶层文件路径
    in_module_f = rtl_folder + m_f
    #顶层模块名称
    top_module = m_f.split('.')[0]
    all_file_list.append(top_module)
    depth_f.write('# 模块引用层次结构图\n')
    depth_f.write(top_module + '\r\n')
    print('顶层模块:', top_module)
    getAllModule(in_module_f)
    depth_f.write('\r\n')
    depth_f.write('\r\n')
    depth_f.write('\r\n')
    depth_f.write('\r\n')

    depth_f.write('# 涉及子模块文件名\n')
    inc = 0
    all_file_list = list(set(all_file_list))
    all_file_list.sort()
    for i in all_file_list:
        inc = inc + 1
        a_str = str(inc) + ':' + i
        print(a_str)
        a_str = a_str + '\n'
        depth_f.write(a_str)
    print('=============END==============')
    depth_f.close()
    return 0


if __name__ == '__main__':
    main()