# coding=utf-8
from django.apps import apps
from tfduck.common.extendEncoder import DatetimeJSONEncoder
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib import admin
from django.conf import settings
import ast
import hashlib
import json
import logging
import sys
import shutil
import time
import traceback
import random
import requests
import os
import uuid
import arrow


class Et(Exception):
    """
    @author: yuanxiao
    @date: 2010-6-10
    @des: 自定义事物中的错误
    """

    def __init__(self, state=95635, v="default error", *args, **kwas):
        """
        """
        super(Et, self).__init__(*args, **kwas)
        self._msg = v
        self.state = state

    @property
    def msg(self):
        return json.dumps(self._msg)

    def getmsg(self):
        return self._msg


class CeleryRetryError(Et):
    pass


class BaseMethod(object):
    """
    @des:一些基础方法
    """

    def __init__(self):
        """
        @des:保持一些全局变量
        """
        self.logger_django = logging.getLogger('django')
        self.logger_dadian = logging.getLogger('dadian')
        self.http_api = Dj44HttpApi()
    
    def get_unique_id(self):
        unique_id = (uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).hex
        return unique_id
    
    def get_unique_id2(self):
        unique_id = (uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).hex
        return unique_id

    def get_current_env(self):
        current_env = 'server'
        try:
            ddd = settings.DEBUG
        except:
            current_env = "local"
        return current_env

    def remove_file(self, file_path):
        """
        @des: 删除文件
        """
        try:
            os.remove(file_path)
        except:
            pass

    def remove_folder(self, folder_path):
        """
        @des: 删除文件夹
        """
        try:
            shutil.rmtree(folder_path)
        except:
            pass

    def get_file_path(self, path):
        """
        @des: 文件的真实路径
        """
        try:
            return os.path.join(settings.BASE_DIR, os.path.join("dags/sptasks/p_code", path))
        except:
            local_path = os.path.normpath(path)
            paths = local_path.split("/")
            if paths[0] == ".":
                real_path = "/".join(paths[2:])
            else:
                real_path = "/".join(paths[1:])
            return real_path

    def gen_local_unique_file(self, pre_path="", pre_name="", ext="csv"):
        """
        @des:生成本地文件唯一路径
        """
        # media_root = settings.MEDIA_ROOT
        media_root = "/mydata/media"
        base_dir = os.path.join(media_root, "docs", pre_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s_%s.%s" % (pre_name, uuid.uuid1(
        ).hex, arrow.now().format("YYYYMMDD_HHmmSS"), ext)
        file_path = os.path.join(base_dir, real_name)
        return file_path

    def gen_local_unique_path(self, pre_path="", pre_name="", is_create=False):
        """
        @des:生成本地目录唯一路径
        """
        # media_root = settings.MEDIA_ROOT
        media_root = "/mydata/media"
        base_dir = os.path.join(media_root, "docs", pre_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s_%s" % (pre_name, uuid.uuid1(
        ).hex, arrow.now().format("YYYYMMDD_HHmmSS"))
        folder_path = os.path.join(base_dir, real_name)
        if is_create:
            os.makedirs(folder_path)
        return folder_path

    def get_var(self, name):
        """
        @des: 获取变量
        """
        if self.get_current_env() == "local":
            return None
        else:
            VarConfig = apps.get_model("gconfig", 'VarConfig')
            try:
                obj = VarConfig.objects.get(name=name)
                return obj.contents
            except:
                return None

    def clog(self, ctx, *log_values):
        """
        @des: 向数据库中记录日志
        """
        try:
            pd_logs = [str(item) for item in log_values]
            pd_logs = "".join(pd_logs)
            if len(pd_logs) > 1024*1024*50:  # 大于5M
                log_values = ["log data too long"]
        except:
            pass
        if self.get_current_env() == "local":
            #
            real_values = []
            for log_value in log_values:
                try:
                    value = str(log_value)
                    real_values.append(value)
                except:
                    value = "log value must be string"
                    real_values.append(value)
            print(*real_values)
        else:
            task_type = ctx['task_type']
            trid = ctx['trid']
            index = ctx['index']
            #
            real_values = []
            for log_value in log_values:
                try:
                    value = str(log_value)
                    real_values.append(value)
                except:
                    value = "log value must be string"
                    real_values.append(value)

            Record = None
            if task_type == "dtask":
                Record = apps.get_model("dtask", 'RunRecord')
            elif task_type == "retask":
                Record = apps.get_model("retask", 'RETaskRecord')
            elif task_type == "sptask":
                Record = apps.get_model("sptask", 'DPTaskRecord')
            if Record is not None:
                try:
                    Record.objects.add_records(
                        lock_id=trid, task_index=index, recs=real_values)
                except Exception as e:
                    self.log_error("clog error ----- :")
                    self.logerr(e)
        # 防止过度写入日志
        time.sleep(0.2)

    def get_record_now(self, ctx={}, tz="UTC"):
        """
        @des: 获取执行任务记录的创建时间，方便dag里面取根据现在时间去执行part_date
        start = arrow.now(tz="Asia/Shanghai")
        @ return: datetime 带时区
        """
        if self.get_current_env() == "local":
            root_create_time = arrow.now(tz=tz)
        else:
            # 如果是查看任务，而不是任务记录，是不会有这两个参数的
            task_type = ctx.get('task_type', None)
            trid = ctx.get('trid', None)
            if trid is None:
                root_create_time = arrow.now(tz=tz)
            else:
                Record = None
                if task_type == "dtask":
                    Record = apps.get_model("dtask", 'RunRecord')
                elif task_type == "retask":
                    Record = apps.get_model("retask", 'RETaskRecord')
                elif task_type == "sptask":
                    Record = apps.get_model("sptask", 'DPTaskRecord')
                if Record is not None:
                    obj = Record.objects.get(id=trid)
                    #
                    root_create_time = obj.extras.get("root_create_time", None)
                    if root_create_time is None:  # 如果拿不到，那么obj肯定是根节点
                        root_create_time = arrow.get(obj.create_time).to(tz)
                    else:  # 读取extra的信息，即根节点
                        # root_create_time带有时区信息，可以直接get
                        root_create_time = arrow.get(root_create_time).to(tz)
        # 返回
        return root_create_time.datetime

    def jsonloads(self, data):
        """
        @des: 自动jsonload
        """
        try:
            data = json.loads(data)
        except Exception as e:
            try:
                data = ast.literal_eval(data)
            except Exception as e:
                raise Et(2, u"参数格式不正确")
        return data

    def jsondumps(self, data, mode=1, sort_keys=False):
        """
        @des:返回值dumps
        """
        #data = json.dumps(data, ensure_ascii=False, cls=DatetimeJSONEncoder)
        data = json.dumps(data, separators=(',', ':'), cls=DatetimeJSONEncoder)
        return data

    def text_tran_html(self, text):
        """
        @des:将文本转换为html,比如help_text
        """
        text = text.replace("\n", "<br/>")
        text = text.replace(" ", "&nbsp")
        return text

    def tran(self, text):
        """
        @des:翻译
        """
        tran_text = _("%s" % text)
        return tran_text

    # 日志记录
    def logerr(self, e):
        errorMeg = ''
        try:
            for file, lineno, function, text in traceback.extract_tb(sys.exc_info()[2]):
                errorMeg += '%s\n%s, in %s\n%s:                %s!' % (
                    str(e), file, function, lineno, text)
            self.log_error("error"+"*"*50)
            for error in errorMeg.split("\n"):
                self.log_error(error, "error")
            try:
                self.log_error(getattr(e, '_msg', 'exception'))
            except Exception as e1:
                self.log_error(getattr(e, 'msg', 'exception'))
        except Exception as e2:
            self.log_error(e2)

    def geterr(self, e):
        result = []
        errorMeg = ''
        try:
            for file, lineno, function, text in traceback.extract_tb(sys.exc_info()[2]):
                errorMeg += '%s\n%s, in %s\n%s:                %s!' % (
                    str(e), file, function, lineno, text)
            result.append("error"+"*"*50)
            for error in errorMeg.split("\n"):
                result.append(error)
                result.append('error')
            try:
                result.append(getattr(e, '_msg', 'exception'))
            except Exception as e1:
                result.append(getattr(e, 'msg', 'exception'))
        except Exception as e2:
            result.append(str(e2))
        return "\n".join(result)

    def get_log_str(self, *msgs):
        try:
            msg_str = " ".join([str(msg) for msg in msgs])
        except Exception as _:
            msg_str = msgs
        return msg_str

    def log_debug(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        self.logger_django.debug(msg_str)

    def log_info(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        self.logger_django.info(msg_str)

    def log_error(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        self.logger_django.error(msg_str)

    def log_warning(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        self.logger_django.warning(msg_str)
    # end--日志记录


class Dj44HttpApi(object):
    """
    @des: 外部api
    """

    def get_current_env(self):
        current_env = 'server'
        try:
            ddd = settings.DEBUG
        except:
            current_env = "local"
        return current_env

    def get_host_name(self):
        if self.get_current_env() == "local":
            return {'s': 13, 'msg': 'local'}
        else:
            GConfig = apps.get_model("gconfig", 'GConfig')
            try:
                obj = GConfig.objects.get(name='host_name')
                host_name = obj.contents['value']
            except:
                return {'s': 13, 'msg': 'host_name error'}
        return {'s': 1, 'v': host_name}

    # start----tfduck的外部接口调用
    def run_sptasks_by_taskname(self, user_token, task_names):
        """
        @des: http外部接口运行非定时的任务
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token[必填]: tfduck的用户token
               task_names[必填]: 运行的sptask任务(不是任务工程，也不是任务记录)的全名的列表, 比如 ["同步任务_3",...]
        @return: 
               成功---{"s":1,  'value':[任务名称]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.run_sptasks_by_taskname('xxxxx', ['helloworld_end_tf_2_0'])
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'run_sptasks_by_taskname')
        data = {
            'user_token': user_token,
            'task_names': json.dumps(task_names),
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    def run_sptasks_by_projectname(self, user_token, project_names):
        """
        @des: http外部接口运行非定时的任务
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token   [必填]: tfduck的用户token
               project_names[必填]: 运行的sptask任务工程的名称(不是任务，也不是任务记录)的全名的列表, 比如 ["同步任务工程名",...]
        @return: 
               成功---{"s":1,  'value':[任务名称]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.run_sptasks_by_projectname('xxxxx', ['helloworld_end_tf_2_0'])
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'run_sptasks_by_projectname')
        data = {
            'user_token': user_token,
            'project_names': json.dumps(project_names)
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    def get_sptasks_info_by_taskname(self, user_token, task_names, start_time, end_time):
        """
        @des: http外部接口查询任务的信息，根据任务名称查询
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token[必填]: tfduck的用户token
               task_names[必填]: 运行的sptask任务(不是任务工程，也不是任务记录)的全名的列表, 比如 ["同步任务_3",...]
               start_time[选填]: 任务的create_time的查询时间范围的开始时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 14:23:44
               end_time  [选填]: 任务的create_time的查询时间范围的结束时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 18:23:44
        @return: 
               成功---{"s":1,  'value':[{'task__name': '任务名称', 'task__id': 109, 'id': 78, 'state': 3, 'revoke_state': 1},...]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.get_sptasks_info_by_taskname('xxxxx', ['helloworld_end_tf_2_0'], '2022-02-15 14:23:44', '2022-02-15 18:23:44')
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'get_sptasks_info_by_taskname')
        data = {
            'user_token': user_token,
            'task_names': json.dumps(task_names),
            'start_time': start_time,
            'end_time': end_time,
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    def get_sptasks_info_by_projectname(self, user_token, project_names, start_time, end_time):
        """
        @des: http外部接口查询任务的信息，根据任务工程名称查询
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token[必填]: tfduck的用户token
               project_names[必填]: 运行的sptask任务(不是任务工程，也不是任务记录)的全名的列表, 比如 ["同步任务_3",...]
               start_time[选填]: 任务的create_time的查询时间范围的开始时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 14:23:44
               end_time  [选填]: 任务的create_time的查询时间范围的结束时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 18:23:44
        @return: 
               成功---{"s":1,  'value':[{'task__name': '任务名称', 'task__id': 109, 'id': 78, 'state': 3, 'revoke_state': 1},...]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.get_sptasks_info_by_projectname('xxxxx', ['helloworld_end_tf_2_0'], '2022-02-15 14:23:44', '2022-02-15 18:23:44')
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'get_sptasks_info_by_projectname')
        data = {
            'user_token': user_token,
            'project_names': json.dumps(project_names),
            'start_time': start_time,
            'end_time': end_time,
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    # end----tfduck的外部接口调用


BMOBJ = BaseMethod()
