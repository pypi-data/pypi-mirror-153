import oss2
import os
import uuid
import time
from django.conf import settings
from tfduck.common.defines import BMOBJ, Et
import base64
import pathlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, FIRST_COMPLETED
import gzip
import random
import requests


class OssSession(oss2.Session):
    def __init__(self, pool_connections=10, pool_maxsize=10):
        """
        @param pool_connections:  同一个域名(host)的连接不会关闭，第二次访问这个域名(host)还是用这个连接。 可以理解为host数量
        @param pool_maxsize:  仅当你在多线程环境下使用session，你才应该关心pool_maxsize
                                针对于每个host保存连接的集合, 且 pool_maxsize 是这个集合的最大值. 如果你运行你的代码在同一个线程，它是不可能针对多个host创建多个连接的，因为requests库是阻塞的, 因此HTTP请求总是一个接着一个发送.

        最后:   pool_connections的数量由host决定（并且这个值不会引起Connection pool is full, discarding connection pool_conn的警告）；  
                pool_maxsize由当前的并发线程数量决定，比如ThreadPoolExecutor或者gevent的pool的数量（这个一定要设置对，否则会引起Connection pool is full, discarding connection pool_conn的警告）；
        """

        self.session = requests.Session()
        self.session.mount(
            'http://', requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize))
        self.session.mount(
            'https://', requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize))


class AliyunOss(object):
    """
    @des: 阿里云oss的基本操作

    上传单个文件
    aoss = AliyunOss(self.gconf.oss_bucket, self.gconf.oss_access_id,
                             self.gconf.oss_access_key, self.gconf.oss_endpoint)
    oss_file_path = self.gconf.oss_result_key
    aoss.bucket.put_object_from_file(oss_file_path, local_file_path)
    """

    def __init__(self, bucket_name, aly_access_key_id, aly_access_key_secret,
                 aly_endpoint,
                 pool_connections=210, pool_maxsize=210, timeout=None, retry_time_sleep=None, 
                 print_files_info=False
                 ):
        """
        @des:初始化
        """
        self.access_key_id = aly_access_key_id
        self.access_key_secret = aly_access_key_secret
        self.bucket_name = bucket_name
        # oss-us-east-1.aliyuncs.com
        self.endpoint = aly_endpoint
        #
        oss_session = OssSession(pool_connections, pool_maxsize)
        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret),
                                  self.endpoint, self.bucket_name, session=oss_session,
                                  connect_timeout=timeout
                                  # connect_timeout = 60
                                  # connect_timeout=(30, 300)  # 这个参数可以用tuple，看了原来，是支持的，(connect_timeout, read_timeout)
                                  )
        self.retry_time_sleep = retry_time_sleep
        self.print_files_info = print_files_info

    def gen_local_unique_file(self, ext="csv"):
        """
        @des:生成本地文件唯一路径
        """
        if BMOBJ.get_current_env() == "server":
            media_root = settings.MEDIA_ROOT
            base_dir = os.path.join(media_root, "data")
        else:
            base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s.%s" % (BMOBJ.get_unique_id2(), BMOBJ.get_unique_id2(), ext)
        file_path = os.path.join(base_dir, real_name)
        return file_path

    def download(self, remote_filename):
        """
        @des:下载oss文件到本地---head_object
        """
        BMOBJ.log_error("download", remote_filename,  "start")
        #
        unique_path = self.gen_local_unique_file()
        tmp_unique_file = "%s.tmp.json" % unique_path
        #
        total_retry = 18
        for i in range(total_retry):
            try:
                self.bucket.restore_object(remote_filename)
            except Exception as _:
                pass

            try:
                oss2.resumable_download(
                    self.bucket, remote_filename, tmp_unique_file)
                break
            except Exception as e:
                BMOBJ.remove_file(tmp_unique_file)
                if i >= total_retry-1:
                    raise e
                else:
                    time.sleep(10)
        os.rename(tmp_unique_file, unique_path)
        #
        BMOBJ.log_error("download", remote_filename,  "end")
        #
        if 0:
            with open(unique_path, 'rb') as f:
                file_content = f.read()
            BMOBJ.remove_file(unique_path)
            file_base64_str = base64.b64encode(file_content).decode()
            return file_base64_str
        else:
            with open(unique_path, 'r') as f:
                file_content = f.read()
            BMOBJ.remove_file(unique_path)
            #
            return file_content

    def upload(self, file_content, remote_filename):
        """
        @des:上传文件
        @param file_content: 字符串
        @param remote_filename: 上传到远程oss的路径
        """
        BMOBJ.log_error("upload",  "start")
        if type(file_content) != str:
            raise Et(2, "file_content must be str")
        # local_filename = download_image_local(fid)
        unique_path = self.gen_local_unique_file()
        tmp_unique_file = "%s.tmp.json" % unique_path
        if 0:
            with open(tmp_unique_file, 'wb') as f:
                f.write(file_content)
        else:
            with open(tmp_unique_file, 'w') as f:
                f.write(file_content)
        os.rename(tmp_unique_file, unique_path)
        result = oss2.resumable_upload(
            self.bucket, remote_filename, unique_path)
        BMOBJ.remote_filename(unique_path)
        #
        BMOBJ.log_error(result)
        BMOBJ.log_error("upload",  "end")
        return True

    def exists(self, remote_filename):
        """
        @des: 判断oss上面文件是否存在
        """
        exists = self.bucket.object_exists(remote_filename)
        return exists

    def delete_path(self, remote_path):
        """
        废弃
        @des: 删除一个远程path，和下面所有的文件---废弃，用下面的delete_prefix_oss
        """
        oss_file_list = self.find_prefix_oss({}, remote_path, isrm=False)
        for exist_file_path in oss_file_list:
            self.bucket.delete_object(exist_file_path)
        return True

    def find_prefix_oss(self, ctx, oss_file_path, isrm=False, ftype='file'):
        """
        @des: 遍历oss文件夹，找到所有文件路径列表
        @params: isrm ------是否递归删除子目录下的文件
                 ftype -----返回的文件类型 file--表示文件， folder--表示文件夹, all---表示文件和文件夹都返回
        """
        bucket = self.bucket
        oss_file_list = []
        # 目录必须以/结尾
        if oss_file_path[-1] != "/":
            oss_file_path += "/"
        # delimiter='/' 是只找本层目录的； 去掉这个，是递归找所有子目录下的文件
        if not isrm:
            file_iter = oss2.ObjectIterator(
                bucket, prefix=oss_file_path, delimiter='/')
        else:
            file_iter = oss2.ObjectIterator(bucket, prefix=oss_file_path)
        # 循环遍历即可
        for obj in file_iter:
            exist_file_path = obj.key
            if ftype == "file":
                if not exist_file_path.endswith("/"):
                    oss_file_list.append(exist_file_path)
            elif ftype == "folder":
                if exist_file_path.endswith("/"):
                    oss_file_list.append(exist_file_path)
            elif ftype == "all":
                oss_file_list.append(exist_file_path)
        #
        return oss_file_list

    def delete_prefix_oss(self, ctx, oss_file_path, isrm=False):
        """
        @des: 删除oss的文件夹
        @params: isrm ------是否递归删除子目录下的文件
        """
        bucket = self.bucket
        oss_file_list = self.find_prefix_oss(ctx, oss_file_path, isrm)
        # 循环删除即可
        for exist_file_path in oss_file_list:
            bucket.delete_object(exist_file_path)

    def _download_oss(self, ctx, td_file, local_file):
        bucket = self.bucket
        retry_count = 3
        for i in range(retry_count):  # 最多重试三次，由于网络不稳定等问题
            try:
                _s = time.time()
                result = bucket.get_object_to_file(td_file, local_file)
                _e = time.time()
                if self.print_files_info:
                    BMOBJ.clog(
                        ctx, f"{local_file} download status {result.status}, sub time {_e-_s}", )
                break
            except Exception as e:
                BMOBJ.clog(
                    ctx, f"{local_file} download oss fail, repeat {i}, error: {e}")
                if i < retry_count-1:
                    if self.retry_time_sleep is None:
                        sleep_time = random.randint(60, 120)
                    else:
                        sleep_time = self.retry_time_sleep
                    time.sleep(sleep_time)
                    continue
                else:
                    BMOBJ.clog(
                        ctx, f"{local_file} download oss finally fail: {e}")
                    raise Et(2, f"download fail {td_file} {local_file}")

    def download_oss(self, ctx, local_file_path, oss_file_path, max_workers=200, isrm=False, isdel=True):
        """
        @des: 下载到oss---多线程下载---下载文件夹--下载后删除oss的文件
        auth = oss2.Auth(self.oss_access_id_i, self.oss_access_key_i)
        bucket = oss2.Bucket(auth, self.oss_endpoint_i, self.oss_bucket_i)
        """
        # bucket = self.bucket
        s = time.time()
        # 删除本地已经存在的文件,重新创建本地路径
        BMOBJ.remove_folder(local_file_path)
        os.makedirs(local_file_path)
        # 下载
        subfiles = self.find_prefix_oss(ctx, oss_file_path, isrm=isrm)
        if subfiles:
            executor = ThreadPoolExecutor(max_workers=max_workers)
            all_tasks = []
            for subfile in subfiles:
                td_file = subfile
                subfile_name = pathlib.PurePath(td_file).name
                if not isrm:
                    local_file = f"{local_file_path}/{subfile_name}"
                else:
                    l_name = str(pathlib.PurePath(td_file)
                                 ).replace(oss_file_path, "")
                    if l_name.startswith("/"):
                        l_name = l_name[1:]
                    local_file = os.path.join(local_file_path, l_name)
                    os.makedirs(os.path.dirname(local_file),
                                exist_ok=True)  # 创建不存在的子文件夹
                # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
                task_i = executor.submit(
                    self._download_oss, *(ctx, td_file, local_file))
                all_tasks.append(task_i)
            # 等待所有任务完成后
            # wait(all_tasks, timeout=timeout, return_when=ALL_COMPLETED)
            for future in as_completed(all_tasks):  # 这个子线程出错会抛出来
                _ = future.result()

            # if 0:
            #     tds = []
            #     for subfile in subfiles:
            #         td_file = subfile
            #         subfile_name = pathlib.PurePath(td_file).name
            #         local_file = f"{local_file_path}/{subfile_name}"
            #         t = threading.Thread(target=self._download_oss,
            #                             args=(ctx, bucket, td_file, local_file))
            #         tds.append(t)
            #     for td in tds:
            #         # 表示该线程是不重要bai的,进程退出时不需要等待这个线程执行完成。
            #         # 这样做的意义在于：避免子线程无限死循环，导致退不出程序，也就是避免楼上说的孤儿进程。
            #         # thread.setDaemon（）设置为True, 则设为true的话 则主线程执行完毕后会将子线程回收掉,
            #         # 设置为false,主进程执行结束时不会回收子线程
            #         td.setDaemon(True)
            #         td.start()
            #     for td in tds:
            #         td.join()
        e = time.time()
        # 删除oss已经存在的part_date的文件---内网端
        if isdel:
            self.delete_prefix_oss(ctx, oss_file_path)
        #
        BMOBJ.clog(
            ctx, f"{oss_file_path} download oss all time", e-s)

    def _upload_oss(self, ctx, td_file, local_file):
        # BMOBJ.clog(ctx, f"sub upload start {td_file} {local_file}")
        bucket = self.bucket
        retry_count = 3
        for i in range(retry_count):  # 最多重试三次，由于网络不稳定等问题
            try:
                _s = time.time()
                result = bucket.put_object_from_file(td_file, local_file)
                _e = time.time()
                if self.print_files_info:
                    BMOBJ.clog(
                        ctx, f"{local_file} upload status {result.status}, sub time {_e-_s}", )
                break
            except Exception as e:
                BMOBJ.clog(
                    ctx, f"{local_file} upload oss fail, repeat {i}, error: {e}")
                #
                if i < retry_count-1:
                    if self.retry_time_sleep is None:
                        sleep_time = random.randint(60, 120)
                    else:
                        sleep_time = self.retry_time_sleep
                    time.sleep(sleep_time)
                    continue
                else:
                    BMOBJ.clog(
                        ctx, f"{local_file} upload oss finally fail: {e}")
                    raise Et(2, f"upload fail {td_file} {local_file}")

    def upload_oss(self, ctx, local_file_path, oss_file_path, add_success=False, add_empty=False, max_workers=200, isrm=False, isdel=True):
        """
        @des: 上传到oss---多线程上传---上传文件夹
        auth = oss2.Auth(self.oss_access_id, self.oss_access_key)
        bucket = oss2.Bucket(auth, self.oss_endpoint, self.oss_bucket)
        """
        s = time.time()
        # 删除oss已经存在的part_date的文件
        self.delete_prefix_oss(ctx, oss_file_path)
        # 上传
        if isrm:  # 遍历文件夹和子文件夹
            subobjs = list(pathlib.Path(local_file_path).rglob("*"))
        else:  # 只遍历当前文件夹
            subobjs = list(pathlib.Path(local_file_path).glob("*"))
        subfiles = [subobj for subobj in subobjs if subobj.is_dir() == False]
        # 打印文件信息
        total_files = []
        total_size = 0
        for subfile in subfiles:
            size = round(subfile.stat().st_size/1024/1024, 4)
            total_size += size
            name = subfile.name
            total_files.append(f"{size}M {name}")
        _infos = '\n'.join(total_files)
        #
        if self.print_files_info:
            BMOBJ.clog(
                ctx, f"""upload file info *  file total count {len(subfiles)}  file total size {total_size}M""", _infos)
        else:
            BMOBJ.clog(
                ctx, f"""upload file info *  file total count {len(subfiles)}  file total size {total_size}M""")

        # 参考 https://www.jianshu.com/p/b9b3d66aa0be
        # 控制最大队列数200，记得修改settings.py的redis队列数必须大于这个
        if subfiles:
            executor = ThreadPoolExecutor(max_workers=max_workers)
            all_tasks = []
            for subfile in subfiles:
                if not isrm:
                    td_file = f'{oss_file_path}{subfile.name}'
                else:
                    l_name = str(subfile).replace(local_file_path, "")
                    if l_name.startswith("/"):
                        l_name = l_name[1:]
                    td_file = os.path.join(oss_file_path, l_name)
                local_file = str(subfile)
                # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
                task_i = executor.submit(
                    self._upload_oss, *(ctx, td_file, local_file))
                all_tasks.append(task_i)
            # 等待所有任务完成后
            # wait(all_tasks, timeout=timeout, return_when=ALL_COMPLETED)
            for future in as_completed(all_tasks):  # 这个子线程出错会抛出来
                _ = future.result()
            # 判断是否上传一个成功的文件
            if add_success:
                # 上传成功后，上传一个空文件代表成功
                success_file = "/mydata/_SUCCESS"
                with gzip.open(success_file, 'wb') as r:
                    r.write(b'')
                self._upload_oss(
                    ctx, f'{oss_file_path}_SUCCESS', success_file)
            #
            # if 0:
            #     tds = []
            #     for subfile in subfiles:
            #         td_file = f'{oss_file_path}{subfile.name}'
            #         local_file = str(subfile)
            #         t = threading.Thread(target=self._upload_oss,
            #                             args=(ctx, bucket, td_file, local_file))
            #         tds.append(t)
            #     for td in tds:
            #         # 表示该线程是不重要bai的,进程退出时不需要等待这个线程执行完成。
            #         # 这样做的意义在于：避免子线程无限死循环，导致退不出程序，也就是避免楼上说的孤儿进程。
            #         # thread.setDaemon（）设置为True, 则设为true的话 则主线程执行完毕后会将子线程回收掉,
            #         # 设置为false,主进程执行结束时不会回收子线程
            #         td.setDaemon(True)
            #         td.start()
            #     for td in tds:
            #         td.join()
            #     if add_success:
            #         # 上传成功后，上传一个空文件代表成功
            #         success_file = "/mydata/_SUCCESS"
            #         with gzip.open(success_file, 'wb') as r:
            #             r.write(b'')
            #         self._upload_oss(
            #             ctx, bucket, f'{oss_file_path}_SUCCESS', success_file)
        else:
            if add_empty:
                # 上传一个empty文件，代表没有数据
                empty_file = "/mydata/_EMPTY"
                with gzip.open(empty_file, 'wb') as r:
                    r.write(b'')
                self._upload_oss(
                    ctx, f'{oss_file_path}_EMPTY', empty_file)
        e = time.time()
        # 删除所有本地文件
        if isdel:
            BMOBJ.remove_folder(local_file_path)
        #
        BMOBJ.clog(
            ctx, f"{oss_file_path} upload oss all time", e-s)
