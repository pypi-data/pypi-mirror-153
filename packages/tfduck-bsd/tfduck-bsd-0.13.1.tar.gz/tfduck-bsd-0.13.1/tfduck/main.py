import sys
import getopt
import requests
import zipfile
import os
import shutil
import base64
import uuid
import importlib
from tfduck.common.defines import BMOBJ


def remove_file(file_path):
    try:
        os.remove(file_path)
    except:
        pass

def set_host(host):
    """
    @des: 将host存入文件
    """
    if host != "del":
        if host.find("http://") == -1 and host.find("https://") == -1:
            print("设置失败: host 应该带有http或者https头")
            return
        if not host.endswith("/"):
            host = f"{host}/"
    base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck/")
    apihost_file = os.path.join(base_dir, "apihost_file")
    if host != 'del':
        remove_file(apihost_file)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        with open(apihost_file, 'w') as f:
            f.write(BMOBJ.jsondumps({'host': host}))
        print("sethost成功")
    else:
        remove_file(apihost_file)
        print("删除host成功")


def get_host():
    base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck/")
    apihost_file = os.path.join(base_dir, "apihost_file")
    if os.path.exists(apihost_file):
        with open(apihost_file, 'r') as f:
            data = BMOBJ.jsonloads(f.read())
        host = data['host']
        return f"{host}"
    else:
        return f"http://tfduck.talefun.com/"


def get_combin_host(rpath):
    host = get_host()
    return f"{host}{rpath}"


# def get_project_id():
#     current_path = os.path.abspath("./")
#     parent_path = os.path.dirname(current_path)
#     project_id = check_project(current_path)
#     return project_id

def find_package_name(project_path):
    """
    @des: 寻找包
    """
    project_path = os.path.abspath(project_path)
    top_package_name = os.path.basename(project_path)
    sub_package_name = None
    for sub_file in os.listdir(project_path):
        if os.path.isdir(sub_file) and sub_file.startswith(top_package_name):
            sub_package_name = sub_file
            break
    if sub_package_name is None:
        raise Exception("同步路径错误, 子包不存在，同步路径应该在工程文件夹内")
    return (top_package_name, sub_package_name)


def check_project(project_path):
    #
    _, sub_package_name = find_package_name(project_path)
    #
    config_path = os.path.join(project_path, f"{sub_package_name}/config.py")
    dag_path = os.path.join(project_path, f"{sub_package_name}/dag.py")
    if not os.path.exists(dag_path) or not os.path.exists(config_path):
        raise Exception("同步路径错误，同步路径应该在工程文件夹内")
    # 获取 uuid
    config_path = os.path.join(project_path, f"{sub_package_name}/config.py")
    with open(config_path, 'rb') as r:
        compile_obj = compile(r.read(), "", 'exec')
    ns = {}
    exec(compile_obj, ns, ns)
    config = ns["config"]
    project_id = config.get("pid", None)
    if not project_id:
        raise Exception("工程配置pid不存在")
    return project_id


def compress(folder_path="./"):
    """
    @des:-------------------------------------------------------
    import shutil
    shutil.make_archive(base_name, format, root_dir, base_dir)
    base_name : 创建的目标文件名，包括路径，减去任何特定格式的扩展。
    format : 压缩包格式。”zip”, “tar”, “bztar”或”gztar”中的一个。
    root_dir : 打包时切换到的根路径。也就是说，开始打包前，会先执行路径切换，切换到root_dir所指定的路径。默认值为当前路径
    base_dir : 开始打包的路径。也就是说，该命令会对base_dir所指定的路径进行打包，默认值为 root_dir ，即打包切换后的当前目录。亦可指定某一特定子目录，从而实现打包的文件包含此统一的前缀路径
    owner 和 group 为创建tar包时使用，默认为用户当前的 owner & group
    @des:----------------------------------
    unpack_archive(filename, extract_dir=None, format=None)： 解压操作。Python3新增方法
    filename：文件路径
    extract_dir：解压至的文件夹路径。文件夹可以不存在，会自动生成
    format：解压格式，默认为None，会根据扩展名自动选择解压格式
    """
    # 目录验证
    current_path = os.path.abspath(folder_path)
    parent_path = os.path.dirname(current_path)
    project_id = check_project(current_path)
    #
    project_name = os.path.basename(current_path)
    zip_file_path = os.path.join(parent_path, f"{project_name}")
    if 0:
        # 这样即可实现目录下所有文件，但不打包目录，
        # 一般配合shutil.unpack_archive(filename, "/你指定的解压目录", "zip") 来使用
        real_file_path = shutil.make_archive(
            zip_file_path, "zip", current_path, f"./")
    else:
        # 这样即可实现打包目录，解压后会生成目录
        # 一般配合shutil.unpack_archive(filename, "/你指定的解压目录的父目录", "zip") 来使用
        real_file_path = shutil.make_archive(
            zip_file_path, "zip", parent_path, f"./{project_name}")
    # print(real_file_path)
    return real_file_path, project_id


def sync():
    auth_info = get_auth_info()
    username = auth_info.get("username", '')
    password = auth_info.get('password', '')
    if not username or not password:
        print("你还未进行认证，请先执行[tfduck login -uUSERNAME -pPASSWORD]命令")
        return
    real_file_path, project_id = compress("./")
    try:
        with open(real_file_path, "rb") as r:
            b64_content = base64.b64encode(r.read()).decode()
            # content = base64.b64decode(b64_content) # django view 通过这个解码即可得到二进制数据
    finally:
        remove_file(real_file_path)
    #
    _, sub_package_name = find_package_name("./")
    with open(f"./{sub_package_name}/config.py", 'rb') as r:
        compile_obj = compile(r.read(), "", 'exec')
    ns = {}
    exec(compile_obj, ns, ns)
    _config = ns["config"]
    #
    ptype = _config.get("ptype", None)
    if ptype == "retask":
        rurl = get_combin_host("syncreproject")
    elif ptype == "sptask":
        rurl = get_combin_host("syncspproject")
    else:
        raise Exception("ptype not in retask, sptask")
    #
    data = {"username": username, "password": password, "is_clean": False,
            "project": b64_content, "project_id": project_id}
    res = requests.post(url=rurl,
                        data=data, timeout=(10, 300))
    try:
        print(res.json()['result'])
    except:
        print(res.text)


def init():
    auth_info = get_auth_info()
    username = auth_info.get("username", '')
    password = auth_info.get('password', '')
    if not username or not password:
        print("你还未进行认证，请先执行[tfduck login -uUSERNAME -pPASSWORD]命令")
        return
    real_file_path, project_id = compress("./")
    try:
        with open(real_file_path, "rb") as r:
            b64_content = base64.b64encode(r.read()).decode()
            # content = base64.b64decode(b64_content) # django view 通过这个解码即可得到二进制数据
    finally:
        remove_file(real_file_path)
    #
    _, sub_package_name = find_package_name("./")
    with open(f"./{sub_package_name}/config.py", 'rb') as r:
        compile_obj = compile(r.read(), "", 'exec')
    ns = {}
    exec(compile_obj, ns, ns)
    _config = ns["config"]
    #
    ptype = _config.get("ptype", None)
    if ptype == "retask":
        rurl = get_combin_host("syncreproject")
    elif ptype == "sptask":
        rurl = get_combin_host("syncspproject")
    else:
        raise Exception("ptype not in retask, sptask")
    #
    data = {"username": username, "password": password, "is_init": True,
            "project": b64_content, "project_id": project_id}
    res = requests.post(url=rurl,
                        data=data, timeout=(10, 300))
    try:
        print(res.json()['result'])
    except:
        print(res.text)


def create_project(create_project_type, package_name):
    """
    @des: 创建工程模板
    """
    auth_info = get_auth_info()
    username = auth_info.get("username", '')
    password = auth_info.get('password', '')
    if not username or not password:
        print("你还未进行认证，请先执行[tfduck login -uUSERNAME -pPASSWORD]命令")
        return
    # 判断工程是否存在
    if os.path.exists(f"./{package_name}"):
        print(f"工程名: {package_name} 已经存在, 请确认删除后再创建！")
        return
    #
    if create_project_type == "retask":
        rurl = get_combin_host("create_re_project")
    elif create_project_type == "sptask":
        rurl = get_combin_host("create_sp_project")
    else:
        raise Exception("create_project_type not in retask, sptask")
    data = {"username": username, "password": password,
            "package_name": package_name}
    res = requests.post(url=rurl,
                        data=data, timeout=(10, 60))
    res_data = res.json()
    if res_data.get("s", 2) == 1:
        # res_package_name = res_data["package_name"]
        file_data = res_data["file_data"]
        file_content = base64.b64decode(file_data)
        #
        try:
            tmp_file_path = f"./{BMOBJ.get_unique_id2()}.zip"
            with open(tmp_file_path, "wb") as f:
                f.write(file_content)
            project_path = f"./{package_name}"
            shutil.unpack_archive(
                tmp_file_path, extract_dir=project_path, format='zip')
        finally:
            remove_file(tmp_file_path)
        print("create project success")
    else:
        print(res_data.get('msg', "未知错误"))


def login(username, password):
    rurl = get_combin_host("tf_authentication")
    data = {'username': username, 'password': password}
    res = requests.post(url=rurl,
                        data=data, timeout=(10, 60))
    res_data = res.json()
    if res_data['s'] == 1:
        base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck/auth")
        session_file = os.path.join(base_dir, "session_file")
        remove_file(session_file)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        with open(session_file, 'w') as f:
            f.write(BMOBJ.jsondumps(data))
        print("认证成功")
    else:
        print(f"认证失败: {res_data.get('msg', '')}")


def logout():
    base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck/auth")
    session_file = os.path.join(base_dir, "session_file")
    remove_file(session_file)
    print(f"退出登录成功")


def get_auth_info():
    base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck/auth")
    session_file = os.path.join(base_dir, "session_file")
    try:
        with open(session_file, 'r') as f:
            data = f.read()
    except:
        data = "{}"
    real_data = BMOBJ.jsonloads(data)
    return real_data


def main(*args, **kwargs):
    help_doc = """
    -h 查看帮助文件
    -v 查看版本
    -m 配合create命令使用，有该参数则是创建retask，否则都是sptask,测试用，用户可以不用管这个
    { -u 用户名 -p 密码 login }     认证
    { info }                      查看当前登录用户
    { create [project name]  }    创建工程(不要取和系统工程同名的名称，比如pandas，django等名称)
    { sync }                      cd到工程目录内执行该命令,同步工程到服务器
    { init }                      cd到工程目录内执行该命令, 同步工程到服务器； 删除原来的dags,执行记录和作业调度并重新创建
    { sethost [api的host地址或者del]}     执行该命令，可以切换 host地址；如果是del，则删除host文件，使用默认；管理员使用，用户可以不用管这个
    ##################################################
    example:
    认证:
    tfduck -uUSERNAE -pPASSWORD login 
    创建工程
    tfduck create helloworld
    初始化当前工程
    tfduck init
    如果工程只修改了src源码，并没有修改dag.py，则可执行
    tfduck sync
    """
    # print(1111)
    # print(args)
    # print(kwargs)
    #
    opts, args = getopt.getopt(
        args, "hvu:p:d:m", ["sync", "create=", "help", "login", "logout", "info", "sethost="])
    # print(opts, args)
    try:
        username = None
        password = None
        is_sync = False
        is_init = False
        is_create = False
        is_login = False
        is_logout = False
        is_info = False
        is_sethost = False
        create_project_type = "sptask"
        for op, value in opts:
            if op == "-h":
                print(help_doc)
            elif op == "-v":
                import tfduck
                print(tfduck.__version__)
            elif op == "-u":
                username = value
            elif op == "-p":
                password = value
            elif op == "-m":
                create_project_type = 'retask'
        try:
            arg = args[0]
        except:
            arg = None
        try:
            arg_value = args[1]
        except:
            arg_value = None
        #
        if arg == "sync":
            is_sync = True
        elif arg == "init":
            is_init = True
        elif arg == "create":
            is_create = True
            if not arg_value:
                raise Exception("create命令必须有一个工程名参数")
        elif arg == "login":
            is_login = True
        elif arg == "logout":
            is_logout = True
        elif arg == "info":
            is_info = True
        elif arg == "sethost":
            is_sethost = True
            if not arg_value:
                raise Exception("sethost命令必须有一个参数")
        #
        if is_login:
            login(username, password)
        elif is_logout:
            logout()
        elif is_create:
            create_project(create_project_type, arg_value)
        elif is_sync:
            sync()
        elif is_init:
            init()
        elif is_sethost:
            set_host(arg_value)
        elif is_info:
            auth_info = get_auth_info()
            username = auth_info.get("username", '')
            host = get_host()
            info = f"""
当前登录用户: {username if username else "未认证"}
当前host: {host}
            """
            print(info)
    except Exception as e:
        print(e)
        print(help_doc)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)
