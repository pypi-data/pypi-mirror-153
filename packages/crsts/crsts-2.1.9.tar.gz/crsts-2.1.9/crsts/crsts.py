import os
import time
import hashlib
import shutil
import pickle
import base64
from multiprocessing import Process, JoinableQueue, Manager
import subprocess
from collections import Counter
import configparser
config = configparser.ConfigParser()
import csv
import random
import json
import glob
import math
import tempfile
import threading
import queue
import re
from pathlib import Path

def write2path(lines,path='',encoding='utf-8',method='lines',append='w',wrap=True):
    """ 写入数组到本地文件
        lines - 字符串数组
        path - 本地文件路径
        encoding - 编码格式
        method - 写入类型 (lines-多行数据写入 line-写入字符串)
        append - 操作模式 (w-覆盖写入 a-追加)
        wrap - 自动换行 (数组中每条数据后加换行符)
    """
    if not path: path=getTime()+'.txt'
    with open(path,append,encoding=encoding) as fw:
        if method=='lines':
            lines = [str(f) for f in lines]
            if wrap: lines = [f+'\n' for f in lines]
            fw.writelines(lines)
        else:
            fw.write(lines)

def append2path(line,path,encoding='utf-8',method='line',append='a'):
    """ 文件末尾追加内容
            line - 追加的内容，自动在内容后加换行
            path - 本地文件路径
            encoding - 编码格式
            method - 写入类型 (lines-多行数据写入 line-写入字符串)
            append - 操作模式 (a-追加 w-覆盖写入)
    """
    with open(path,append,encoding=encoding) as fw:
        if method=='line':
            fw.write(line+'\n')
        else:
            fw.writelines(line)

def read_path(path,method='lines',encoding='utf-8',errors='strict',strip=True):
    """ 读取文件
            path - 本地文件路径
            method - 读取类型 (lines-以多行数据读取 line-以单个字符串读取)
            encoding - 编码格式
            errors - 编码错误处理 (strict-严格模式，错误报异常 ignore-忽略错误的内容)
            strip - 是否去除每条数据后面的换行符
    """
    with open(path,'r',encoding=encoding,errors=errors) as fr:
        if method == "lines":
            all_lines = fr.readlines()
            if strip:
                all_lines = [l.strip() for l in all_lines]
        else:
            all_lines = fr.read()
        return all_lines

def print_list(array,index=False):
    """ 打印list内容
            index - 是否打印索引
    """
    if index:
        for i,val in enumerate(array):
            print(i,val)
    else:
        for val in array:
            print(val)
    print(f"length:{len(array)}")

def get_top_n_files(folder_path,n):
    """ 获取文件夹中前n个文件路径 """
    if not os.path.exists(folder_path):
        return []
    if folder_path[-1] != '/':
        folder_path=folder_path+'/'
    top_n_files = [folder_path+f for f in os.listdir(folder_path)[:n]]
    return top_n_files

def copy_top_n_file(folder_path,n,dst_folder):
    """ 复制文件夹中前n个文件到指定路径 """
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    top_n_files = get_top_n_files(folder_path,n)
    for f in top_n_files:
        copyfile(f,dst_folder)

def save2pkl(obj,path,protocol=-1):
    """ 存储python对象 """
    with open(path,'wb') as fw:
        pickle.dump(obj,fw,protocol=protocol)

def read_pkl(path):
    """ 读取python对象 """
    with open(path, 'rb') as fr:
        obj = pickle.load(fr)
        return obj

def getTime(timestamp='',format='y'):
    """ 获取当前时间 """
    if format=='y':
        format_str="%y-%m-%d %H:%M:%S"
    else:
        format_str="%Y-%m-%d %H:%M:%S"
    if timestamp:
        return time.strftime(format_str, time.localtime(timestamp))
    else:
        return time.strftime(format_str, time.localtime())

def getTimestamp(is_ms=False):
    """ 获取当前时间戳
            is_ms - 毫秒时间戳
    """
    ts=time.time()
    if is_ms:
        return int(ts * 1000)
    return int(time.time())

def getTimeSpan(begin_time, end_time, format='minute'):
    """ 获取2个时间的时间间隔 """
    begin_time = time.strptime(begin_time, "%y-%m-%d %H:%M:%S")
    end_time = time.strptime(end_time, "%y-%m-%d %H:%M:%S")

    begin_timeStamp = int(time.mktime(begin_time))
    end_timeStamp = int(time.mktime(end_time))
    span_seconds = abs(end_timeStamp - begin_timeStamp)

    if format == 'second':
        return int(round(span_seconds, 2))
    elif format == 'minute':
        return int(round(span_seconds / 60, 2))
    elif format == 'hour':
        return int(round(span_seconds / 3600, 2))
    elif format == 'day':
        return int(round(span_seconds / 86400, 2))
    else:
        return int(round(span_seconds, 2))

def get_tmp_dir():
    return tempfile.gettempdir()

def get_file_md5(file_path):
    """ 获取文件md5 """
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5

def get_file_sha256(file_path):
    """ 获取文件sha256 """
    sha256obj = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        f.close()
        sha256obj = str(hash_value).lower()
    return sha256obj

def get_file_chardet(file_path):
    import chardet
    f = open(file_path, "rb")
    data = f.read()
    f.close()
    return chardet.detect(data)

def get_str_md5(parmStr):
    """ 获取字符串的md5 """
    if isinstance(parmStr, str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()

def getfilesize(filePath):
    """ 获取文件大小 """
    fsize = os.path.getsize(filePath)
    fsize = fsize / (1000 * 1000)
    return round(fsize, 2)

def listDir(rootDir,only_file=False,only_folder=False,recursive=False,sort=True):
    """ 获取文件夹中的文件列表 """
    list_filepath = []
    if recursive:
        all_file=glob.glob(os.path.join(rootDir, '**'), recursive=True)
        for pathname in all_file:
            filename = os.path.basename(pathname)
            if filename == '.DS_Store':
                continue
            if only_file:
                if os.path.isfile(pathname):
                    list_filepath.append(pathname)
                continue
            if only_folder:
                if os.path.isdir(pathname):
                    list_filepath.append(pathname)
                continue
            list_filepath.append(pathname)
    else:
        for filename in os.listdir(rootDir):
            pathname = os.path.join(rootDir, filename)
            if filename == '.DS_Store':
                continue
            if only_file:
                if os.path.isfile(pathname):
                    list_filepath.append(pathname)
                continue
            if only_folder:
                if os.path.isdir(pathname):
                    list_filepath.append(pathname)
                continue
            list_filepath.append(pathname)
    if sort:
        return list(sorted(list_filepath))
    else:
        return list_filepath

def globInDir(rootDir,search_regular):
    """rootDir搜索目录  search_regular搜索关键字 **代表所有目录 *代表所有文件和目录"""
    list_filepath = []
    for filename in Path(rootDir).rglob(search_regular):
        list_filepath.append(str(filename))
    list_filepath = [f for f in list_filepath if '.DS_Store' not in f]
    return list_filepath

def globFile(search_regular,recursive=True):
    """search_regular搜索关键字 **代表所有目录 *代表所有文件和目录
       /Volumes/Data/PycharmProjects/algorithms/datasets/**/*.jpg
    """
    list_filepath = glob.glob(search_regular,recursive=recursive)
    list_filepath = [f for f in list_filepath if '.DS_Store' not in f]
    return list_filepath

def makedir(dir_path,delete_exists=False):
    """ 创建文件夹 """
    if os.path.exists(dir_path):
        if delete_exists:
            rmfolder(dir_path)
            os.makedirs(dir_path)
        else:
            print("--------创建文件夹失败:" + dir_path + ",路径已存在--------")
    else:
        os.makedirs(dir_path)

def touchfile(path):
    """ 创建文件 """
    if not os.path.exists(path):
        f = open(path,'w')
        f.close()

def counter(lst,sort=False,reverse=False):
    """ 统计list数组内容 """
    if sort:
        sorted_lst=sorted(Counter(lst).items(),key=lambda f:f[1],reverse=reverse)
        return dict(sorted_lst)
    else:
        return dict(Counter(lst))

def copyfile(origin_path, target_path):
    """ 复制文件 """
    if os.path.isfile(origin_path):
        shutil.copy(origin_path, target_path)
    else:
        print("--------复制文件失败:" + origin_path + ",路径不存在--------")

def movefile(origin_path, target_path):
    """ 移动文件 """
    if os.path.exists(origin_path):
        shutil.move(origin_path, target_path)
    else:
        print("--------移动文件失败:" + origin_path + ",路径不存在--------")

def copyfolder(origin_folder, target_folder, *args):
    """ 复制文件夹 """
    # 目标文件夹名为 target_path，不能已经存在；方法会自动创建目标文件夹。
    if os.path.isdir(origin_folder):
        shutil.copytree(origin_folder, target_folder, ignore=shutil.ignore_patterns(*args))
    else:
        print("--------复制文件夹失败:" + origin_folder + ",路径不存在--------")

def rmfile(del_file):
    """ 删除文件 """
    if os.path.isfile(del_file):
        os.remove(del_file)
    else:
        print("--------删除文件失败:" + del_file + ",路径不存在--------")

def rmfolder(del_folder):
    """ 删除文件夹 """
    if os.path.isdir(del_folder):
        shutil.rmtree(del_folder)
    else:
        print("--------删除文件夹失败:" + del_folder + ",路径不存在--------")

def base64decode(strings,encoding='utf-8'):
    """ base64解码 """
    try:
        base64_decrypt = base64.b64decode(strings.encode('utf-8'))
        return str(base64_decrypt, encoding)
    except:
        return ''

def base64encode(strings,encoding='utf-8'):
    """ base64编码 """
    try:
        base64_encrypt = base64.b64encode(strings.encode('utf-8'))
        return str(base64_encrypt, encoding)
    except:
        return ''

def run_cmd(cmd,with_output=False):
    """ 调用系统命令 """
    if with_output:
        return subprocess.getstatusoutput(cmd)
    else:
        return subprocess.call(cmd, shell=True)

def func_time(func):
    """ 获取方法运行时间 """
    begin_time= time.time()
    func()
    end_time= time.time()
    print(f'{func.__name__} 耗时:{int(end_time-begin_time)}')

def run_multi_task_in_large(all_items, user_func, cpu_num=os.cpu_count(), by_order=False):
    result = []
    if len(all_items) > 32000:
        for i in range(0, len(all_items), 32000):
            if by_order:
                result.extend(list(sorted(run_multi_task_in_order(all_items[i: i + 32000], user_func, cpu_num=cpu_num).items(),key=lambda f:f[0])))
            else:
                result.extend(run_multi_task(all_items[i: i + 32000], user_func, cpu_num=cpu_num))
    else:
        if by_order:
            result.extend(run_multi_task_in_order(all_items, user_func, cpu_num=cpu_num))
        else:
            result.extend(run_multi_task(all_items, user_func, cpu_num=cpu_num))
    return result

def run_multi_task(all_items, user_func, cpu_num=os.cpu_count()):
    """ 多进程执行方法 """
    print(f'检测到全部:{len(all_items)}个')
    print(f'启动{cpu_num}个进程,开始运行')

    if len(all_items)>32000:
        print('数组个数大于32000，无法运行')
        return []
    else:
        begin_time = time.time()
        q = JoinableQueue()
        for item in all_items:
            q.put(item)

        def func_task(q, res_list):
            while True:
                item = q.get()
                res_list.append(user_func(item))
                q.task_done()

        res_list = Manager().list()
        for i in range(cpu_num):
            p = Process(target=func_task, args=(q, res_list))
            p.daemon = True
            p.start()
        q.join()
        print(f'全部已完成，用时:{float(time.time() - begin_time)}')
        return list(res_list)

def run_multi_task_in_order(all_items, user_func, cpu_num=os.cpu_count()):
    """ 多进程按顺序执行方法 """
    print(f'检测到全部:{len(all_items)}个')
    print(f'启动{cpu_num}个进程,开始运行')

    if len(all_items)>32000:
        print('数组个数大于32000，无法运行')
        return {}
    else:
        begin_time = time.time()
        q = JoinableQueue()
        for index,data in enumerate(all_items):
            q.put((index,data))

        def func_task(q, res_dict):
            while True:
                item = q.get()
                res_dict[item[0]] = user_func(item[1])
                q.task_done()

        res_dict = Manager().dict()
        for i in range(cpu_num):
            p = Process(target=func_task, args=(q, res_dict))
            p.daemon = True
            p.start()
        q.join()
        print(f'全部已完成，用时:{float(time.time() - begin_time)}')
        return dict(res_dict)

def run_multi_thread_task(all_items, user_func, thread_num=os.cpu_count()+1):
    """ 多线程执行方法 """
    print(f'检测到全部:{len(all_items)}个')
    print(f'启动{thread_num}个线程,开始运行')

    res_list = []
    begin_time = time.time()
    q = queue.Queue()
    for item in all_items:
        q.put(item)

    def func_task(q):
        while True:
            item = q.get()
            res_list.append(user_func(item))
            q.task_done()

    for i in range(thread_num):
        t = threading.Thread(target=func_task, args=(q, ))
        t.daemon = True
        t.start()
    q.join()
    print(f'全部已完成，用时:{float(time.time() - begin_time)}')
    return res_list

def run_multi_thread_task_in_order(all_items, user_func, thread_num=os.cpu_count()+1):
    """ 多线程按顺序执行方法 """
    print(f'检测到全部:{len(all_items)}个')
    print(f'启动{thread_num}个线程,开始运行')

    res_dict = {}
    begin_time = time.time()
    q = queue.Queue()
    for index,data in enumerate(all_items):
        q.put((index,data))

    def func_task(q):
        while True:
            item = q.get()
            res_dict[item[0]] = user_func(item[1])
            q.task_done()

    for i in range(thread_num):
        t = threading.Thread(target=func_task, args=(q, ))
        t.daemon = True
        t.start()
    q.join()
    print(f'全部已完成，用时:{float(time.time() - begin_time)}')
    return res_dict

def read_config(config_path,config_name,section='default',type='str'):
    """ 读取配置文件 """
    config = configparser.ConfigParser()
    config.read(config_path)
    if section in config.sections():
        if config_name in config.options(section):
            if type=='str':
                return config.get(section, config_name)
            elif type=='float':
                return config.getfloat(section, config_name)
            elif type=='int':
                return config.getint(section, config_name)
            elif type=='bool':
                return config.getboolean(section, config_name)
    return ''

def write_config(config_path,config_name,config_value,section='default'):
    """ 写入配置文件 """
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section(section): config.add_section(section)
    config.set(section, config_name, config_value)

    with open(config_path, 'w') as configfile:
        config.write(configfile)

def read_csv(csv_path,method="list",encoding='utf-8',header=False):
    '''
    读取csv文件
    :param method: list or dict
    :param return: [[1, 'chen', 'male']]  or [[('age', '1'), ('name', 'chen'), ('sex', 'male')]]
    '''
    csv_cnts=[]
    headers=[]
    with open(csv_path, encoding=encoding) as f:
        if method=="list":
            reader = csv.reader(f)
            headers.extend(next(reader))
            for row in reader:
                csv_cnts.append(row)
        else:
            reader = csv.DictReader(f)
            headers.extend(list(next(reader).keys()))
            for row in reader:
                csv_cnts.append(row)
    if header:
        return headers,csv_cnts
    else:
        return csv_cnts

def write_csv(csv_path,header=[],rows=[],method="list",encoding='utf-8',append='w'):
    '''
    写入csv文件
    :param header: ['name', 'age', 'sex']
    :param rows: [{'age': 1, 'name': 'chen', 'sex': 'male'}] or [[1, 'chen', 'male']]
    :param method: list or dict
    '''
    with open(csv_path, append, encoding=encoding, newline='') as f:
        if method=="list":
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        else:
            writer = csv.DictWriter(f, header)
            writer.writeheader()
            writer.writerows(rows)

def rand_int(min,max):
    """ 获取随机数 """
    return random.randint(min, max)

def rand_choice(lst):
    """ 随机选取1个数据 """
    result=random.choice(lst)
    return result

def rand_choices(lst,k=1):
    """ 随机有放回选取k个数据 """
    result=random.choices(lst,k=k)
    return result

def rand_sample(lst, k=1):
    """ 随机抓取k个数据 """
    result=random.sample(lst, k)
    return result

def rand_shuffle(lst):
    """ 打乱list """
    random.shuffle(lst)
    return lst

def json_load(fp):
    """ 加载json文件 """
    return json.load(open(fp,encoding="utf-8"))

def json_loads(json_str):
    """ 加载json """
    return json.loads(json_str)

def json_dump(json_data, fp):
    """ 写入json文件 """
    return json.dump(json_data, open(fp,mode='w',encoding="utf-8"))

def json_dumps(json_data):
    """ 转换json """
    return json.dumps(json_data)

def sleep(secs):
    """ 休眠 """
    time.sleep(secs)

def rename_file_md5(folder,over_write=True):
    """ 将文件夹下的文件用文件的md5来重命名 """
    all_files=listDir(folder,only_file=True)
    all_md5_name=[]
    for f in all_files:
        md5_name=get_file_md5(f)
        new_file_path=os.path.dirname(f)+"/"+md5_name
        if not over_write:
            if md5_name in set(all_md5_name):
                print(new_file_path)
                new_file_path = os.path.join(os.path.dirname(f),md5_name+"_"+str(rand_int(1,100000)))
        all_md5_name.append(md5_name)
        movefile(f,new_file_path)

def format_file_name(file_name,pattern="[a-zA-Z0-9_\\.]"):
    new_file_name="".join(search_by_regular(pattern,file_name))
    new_file_name=new_file_name.replace(".","_")
    return new_file_name

def change_venv(old_project_path,new_project_path):
    '''
        解决venv修改位置后失效问题
    '''
    activate_path1=os.path.join(new_project_path,"venv/bin/activate")
    activate_path2=os.path.join(new_project_path,"venv/bin/activate.csh")
    activate_path3=os.path.join(new_project_path,"venv/bin/activate.fish")

    pip_path1=os.path.join(new_project_path,"venv/bin/pip")
    pip_path2=os.path.join(new_project_path,"venv/bin/pip3")
    pip_path3=os.path.join(new_project_path,"venv/bin/pip3.6")

    for f in [activate_path1,activate_path2,activate_path3,pip_path1,pip_path2,pip_path3]:
        cnt=read_path(f,method="line")
        cnt=cnt.replace(old_project_path,new_project_path)
        write2path(cnt,f,method="line")

def calu_mean(lst,round_num=2):
    lst=[float(f) for f in lst]
    return round(sum(lst)/len(lst),round_num)

def calu_var(lst,round_num=2):
    total = 0
    avg = calu_mean(lst,round_num)
    for value in lst:
        total += (value - avg) ** 2
    variance = total / len(lst)
    return round(variance,round_num)

def calu_std(lst,round_num=2):
    total = 0
    avg = calu_mean(lst,round_num)
    for value in lst:
        total += (value - avg) ** 2
    std = math.sqrt(total / len(lst))
    return round(std,round_num)

def split_path(file_path):
    file_name=os.path.basename(file_path)
    folder_path=os.path.dirname(file_path)
    return folder_path,file_name

def dirname(file_path,depth=1,root=None):
    folder_path, file_name = os.path.split(file_path)
    if root:
        for i in range(10):
            folder_path,file_name = os.path.split(folder_path)
            if folder_path.endswith(root):
                return folder_path
    else:
        if depth>1:
            for i in range(depth-1):
                folder_path=os.path.dirname(folder_path)
    return folder_path

def search_by_regular(pattern,content):
    regex = re.compile(pattern)
    return regex.findall(content)
