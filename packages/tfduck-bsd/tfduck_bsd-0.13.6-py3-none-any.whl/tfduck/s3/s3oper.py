"""
s3的公共操作
版本号见setup.py
"""
# coding=utf-8
import boto3
import time
import random
import pathlib
import os
import shutil
import uuid
import gzip
import pprint
from tfduck.common.defines import BMOBJ, Et
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, FIRST_COMPLETED
from io import StringIO, BytesIO
from botocore.client import Config


class S3Oper(object):
    """
    @des: S3的公共操作, 上传文件
    """

    def __init__(self, ctx={}, ak="", sk="", bucket="", region_name="", print_files_info=False):
        """
        @des: 初始化
        """
        self.ctx = ctx
        self.print_files_info = print_files_info
        """
        aws key
        """
        self.access_key = ak
        self.secret_key = sk
        """
        aws s3
        """
        self.bucket = bucket
        self.region_name = region_name
        """
        初始化client
        """
        self.set_s3_client()
        

    def get_s3_config(self):
        """
        @des: 设置上传文件下载文件，超时的一些设置
        """
        # connect_timeout 和 read_timeout默认值都是60秒
        # max_pool_connections 最大的连接池，默认10
        config = Config(connect_timeout=60,
                        read_timeout=600,
                        retries={'max_attempts': 0},  # 将默认重试次数设为0，不重试
                        # 如果是多线程共享client, upload_foler的max_workers必须比这个值小;  目前是每个线程一个client，所以这里不受影响
                        max_pool_connections=10)
        # s3 = boto3.client('s3', config=config)
        return config

    def get_s3_session(self):
        """
        @des: 初始化session
        """
        s3_session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )
        return s3_session

    def get_s3_resource(self):
        """
        @des: 初始化resource
        """
        s3_session = self.get_s3_session()
        config = self.get_s3_config()
        s3_resource = s3_session.resource('s3')
        # s3_resource = s3_session.resource('s3', config=config)
        return s3_resource

    def get_s3_bucket(self):
        """
        @des: 初始化bucket
        #####
        bucket = self.get_bucket()
        res = bucket.upload_file(Filename=local_path, Key=remote_path)
        #
        bucket = self.get_bucket()
        bucket.download_file(remote_path, local_path)
        ####
        """
        s3_resource = self.get_s3_resource()
        bucket = s3_resource.Bucket(self.bucket)
        return bucket

    def get_s3_client(self):
        """
        @des: 初始化client
        """
        s3_session = self.get_s3_session()
        config = self.get_s3_config()
        s3_client = s3_session.client("s3", config=config)
        return s3_client

    def set_s3_client(self):
        """
        @des: 初始化client
        """
        client = self.get_s3_client()
        self.s3_client = client

    def find_prefix(self, remote_path, isrm=True):
        """
        @des: 遍历s3文件夹，找到所有文件路径列表
        @params: isrm ------是否递归查找子目录下的文件
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        """
        ctx = self.ctx
        bucket = self.bucket
        file_list = []
        client = self.get_s3_client()
        """
        这种方式不能超过1000
        """
        # # print(help(client.list_objects_v2))
        # response = client.list_objects_v2(
        #         Bucket=self.bucket,
        #         Delimiter="",
        #         Prefix =remote_path,
        #         MaxKeys=1000
        #         ) # MaxKeys的最大值为1000， 不能超过1000,
        # print(response)
        # #
        # for obj in response['Contents']:
        #     key = obj['Key']
        #     file_list.append(key)
        #     print(key)
        # return file_list
        """
        可以超过1000
        """
        paginator = client.get_paginator(
            'list_objects_v2')  # MaxKeys的最大值为1000， 不能超过1000,
        # 所以用分页的方式，这样就可以通过分很多页超过1000
        pages = paginator.paginate(
            Bucket=self.bucket, Prefix=remote_path, MaxKeys=1000)
        remote_path_parents_count = len(pathlib.Path(remote_path).parents)
        for page in pages:
            for obj in page['Contents']:
                key = obj['Key']
                if not isrm:
                    if len(pathlib.Path(key).parents)-1 == remote_path_parents_count:
                        file_list.append(key)
                else:
                    file_list.append(key)
        # pprint.pprint(file_list)
        return file_list

    def list_folder(self, remote_path):
        """
        @des:指定路径下的文件夹列表
        """
        s3_client = self.get_s3_client()
        try:
            resp = s3_client.list_objects(
                Bucket=self.bucket, Delimiter='/', Prefix=remote_path+'/')
            return [d.get("Prefix") for d in resp.get("CommonPrefixes")]
        except ClientError as e:
            BMOBJ.clog(self.ctx, "get s3 folders error:", e)
            return []

    def upload_file(self, local_path, remote_path):
        """
        @des: 将本地文件上传到s3
        """
        s3_client = self.get_s3_client()
        try:
            _ = s3_client.upload_file(local_path, self.bucket, remote_path)
        except ClientError as e:
            BMOBJ.clog(self.ctx, "upload s3 file error:", e)
            return False
        return True

    def upload_fileobj(self, io_obj, remote_path):
        """
        @des: 将bytesIO上传到s3

        上传普通文件
        ########
        s3 = S3Oper(...)
        with BytesIO() as r:
            r.write(b'')
            r.seek(0)
            s3.upload_fileobj(r,
                        "sagemaker/yxtest/SUCCESS")
        ########

        上传压缩文件
        ########
        s3 = S3Oper(...)
        with BytesIO() as f:
            with gzip.open(f, 'wb') as r:
                r.write(b'')
            f.seek(0)
            s3.upload_fileobj(f,
                        "sagemaker/yxtest/SUCCESS")
        ########

        """
        s3_client = self.get_s3_client()
        try:
            _ = s3_client.upload_fileobj(io_obj, self.bucket, remote_path)
        except ClientError as e:
            BMOBJ.clog(self.ctx, "upload s3 file error:", e)
            return False
        return True

    def download_file(self, local_path, remote_path):
        """
        @des: 将文件下载到本地
        """
        s3_client = self.get_s3_client()
        try:
            _ = s3_client.download_file(self.bucket, remote_path, local_path)
            BMOBJ.clog(self.ctx, 111, _)
        except ClientError as e:
            BMOBJ.clog(self.ctx, "download s3 file error:", e)
            return False
        return True

    def is_exists(self, remote_path):
        """
        @des: 判断资源是否存在
        s3 = boto3.resource('s3')
        try:
            s3.head_object(Bucket=bucket, Key=key)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True
        或者
        try:
            s3.Object(bucket, key).load()
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True
        """
        s3_client = self.get_s3_client()
        try:
            s3_client.head_object(Bucket=self.bucket, Key=remote_path)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True

    def delete_file(self, remote_path):
        """
        @des: 删除文件
        """
        s3_client = self.get_s3_client()
        try:
            s3_client.delete_object(Bucket=self.bucket, Key=remote_path)
        except ClientError as e:
            BMOBJ.clog(self.ctx, "delete s3 file error:", e)
            return False
        return True

    def delete_folder(self, remote_path):
        """
        @des: 删除目录
        """
        bucket = self.get_s3_bucket()
        bucket.objects.filter(Prefix=remote_path).delete()
        return True

    def _upload_i(self,  remote_file, local_file, retry_count):
        """
        @des: 多线程批量上传
        """
        ctx = self.ctx
        s3_client = self.get_s3_client()  # 如果每个线程单开一个client
        # s3_client = self.s3_client   # 多个线程共享一个client
        """
        开始上传
        """
        for i in range(retry_count):  # 最多重试三次，由于网络不稳定等问题
            try:

                _s = time.time()
                _ = s3_client.upload_file(  # 这个方法本来就是分块多线程上传，所以开一个和多个在大文件来说上传速度区别不大
                    local_file, self.bucket, remote_file)  # 返回值为None
                _e = time.time()
                if self.print_files_info:
                    BMOBJ.clog(
                        ctx, f"{local_file} upload success, sub time {_e-_s}", )
                break
            except Exception as e:
                BMOBJ.clog(
                    ctx, f"{local_file} upload  fail, repeat {i}, error: {e}")
                #
                if i < retry_count-1:
                    sleep_time = random.randint(60, 120)
                    time.sleep(sleep_time)
                    continue
                else:
                    BMOBJ.clog(
                        ctx, f"{local_file} upload  finally fail: {e}")
                    raise Et(2, f"upload fail {remote_file} {local_file}")

    def upload_folder(self, local_path, remote_path,
                      add_success=False, add_empty=False,
                      max_workers=50, isrm=True,
                      isdel=True, retry_count=5
                      ):
        """
        @des: 上传到s3---多线程上传---上传文件夹
        """
        ctx = self.ctx
        s = time.time()
        # 删除已经存在的remote_folder
        self.delete_folder(remote_path)
        # 上传
        if isrm:  # 遍历文件夹和子文件夹
            subobjs = list(pathlib.Path(local_path).rglob("*"))
        else:  # 只遍历当前文件夹
            subobjs = list(pathlib.Path(local_path).glob("*"))
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
                    remote_file = os.path.join(remote_path, subfile.name)
                else:
                    l_name = str(subfile).replace(local_path, "")
                    l_name = l_name.lstrip("/")  # 去掉开始的全部斜杠
                    remote_file = os.path.join(remote_path, l_name)
                local_file = str(subfile)
                # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
                task_i = executor.submit(
                    self._upload_i, *(remote_file, local_file, retry_count))
                all_tasks.append(task_i)
            # 等待所有任务完成后
            # wait(all_tasks, timeout=timeout, return_when=ALL_COMPLETED)
            for future in as_completed(all_tasks):  # 这个子线程出错会抛出来
                _ = future.result()
            # 判断是否上传一个成功的文件
            if add_success:
                # 上传成功后，上传一个空文件代表成功
                with BytesIO() as f:
                    with gzip.open(f, 'wb') as r:
                        r.write(b'')
                    f.seek(0)
                    self.upload_fileobj(
                        f, os.path.join(remote_path, "_SUCCESS"))
        else:
            if add_empty:
                # 上传一个empty文件，代表没有数据
                with BytesIO() as f:
                    with gzip.open(f, 'wb') as r:
                        r.write(b'')
                    f.seek(0)
                    self.upload_fileobj(f, os.path.join(remote_path, "_EMPTY"))
        e = time.time()
        # 删除所有本地文件
        if isdel:
            if len(pathlib.Path(local_path).parents) == 0:
                raise Et(2, "cannt del root folder")
            BMOBJ.remove_folder(local_path)
        #
        BMOBJ.clog(
            ctx, f"{remote_path} upload all time", e-s)

    def _download_i(self, remote_file, local_file, retry_count):
        """
        @des: 多线程批量下载
        """
        ctx = self.ctx
        s3_client = self.get_s3_client()  # 如果每个线程单开一个client
        # s3_client = self.s3_client   # 多个线程共享一个client
        #
        for i in range(retry_count):  # 最多重试三次，由于网络不稳定等问题
            try:
                _s = time.time()
                _ = s3_client.download_file(
                    self.bucket, remote_file, local_file)  # 返回值为None
                _e = time.time()
                BMOBJ.clog(
                    ctx, f"{local_file} download success, sub time {_e-_s}", )
                break
            except Exception as e:
                BMOBJ.clog(
                    ctx, f"{local_file} download  fail, repeat {i}, error: {e}")
                if i < retry_count-1:
                    sleep_time = random.randint(60, 120)
                    time.sleep(sleep_time)
                    continue
                else:
                    BMOBJ.clog(
                        ctx, f"{local_file} download  finally fail: {e}")
                    raise Et(2, f"download fail {remote_file} {local_file}")

    def download_folder(self, local_path, remote_path,
                        max_workers=50, isrm=True,
                        isdel=True, retry_count=5):
        """
        @des: 下载到本地---多线程下载---下载文件夹--下载后删除s3的文件
        """
        ctx = self.ctx
        # bucket = self.bucket
        s = time.time()
        # 删除本地已经存在的文件,重新创建本地路径
        BMOBJ.remove_folder(local_path)
        os.makedirs(local_path, exist_ok=True)
        # 下载
        subfiles = self.find_prefix(remote_path, isrm=isrm)
        if subfiles:
            executor = ThreadPoolExecutor(max_workers=max_workers)
            all_tasks = []
            for subfile in subfiles:
                remote_file = subfile
                subfile_name = pathlib.PurePath(remote_file).name
                if not isrm:
                    local_file = os.path.join(local_path, subfile_name)
                else:
                    l_name = str(pathlib.PurePath(remote_file)
                                 ).replace(remote_path, "")
                    l_name = l_name.lstrip("/")
                    local_file = os.path.join(local_path, l_name)
                    os.makedirs(os.path.dirname(local_file),
                                exist_ok=True)  # 创建不存在的子文件夹
                # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
                task_i = executor.submit(
                    self._download_i, *(remote_file, local_file, retry_count))
                all_tasks.append(task_i)
            # 等待所有任务完成后
            # wait(all_tasks, timeout=timeout, return_when=ALL_COMPLETED)
            for future in as_completed(all_tasks):  # 这个子线程出错会抛出来
                _ = future.result()
        e = time.time()
        # 删除s3已经存在的part_date的文件---内网端
        print(remote_path)
        if isdel:
            if len(pathlib.Path(remote_path).parents) == 0:
                raise Et(2, "cannt del root folder")
            self.delete_folder(remote_path)
        #
        BMOBJ.clog(
            ctx, f"{remote_path} download all time", e-s)


if __name__ == '__main__':  # 打版本的时候一定记得记得脱敏
    pass
    # s3 = S3Oper(ctx = {}, ak="xx", sk="yy", bucket="xx", region_name="us-east-2")
    # s3.upload_folder(local_path="/Users/yuanxiao/Downloads/train/samples",
    #                  remote_path="sagemaker/yxtest/samples", isdel=False, add_empty=True, add_success=True, max_workers=50)
    # s3.find_prefix("sagemaker/yxtest", True)
    # s3.download_folder(local_path="/Users/yuanxiao/Downloads/train/samples",
    #                    remote_path="sagemaker/yxtest/samples", isdel=False, max_workers=50)
