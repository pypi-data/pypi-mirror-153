# coding=utf-8
import gzip
import io
import json
import time
import urllib

import requests
import requests.adapters
import six

from tfduck.common.defines import BMOBJ

# class BM(object):
#     def log_error(self, *args, **kwargs):
#         try:
#             if args:
#                 print(args)
#             if kwargs:
#                 print(kwargs)
#         except:
#             pass
# BMOBJ = BM()

# opends_api_url_prefix = 'https://open.bdp.cn'
opends_api_url_prefix = 'http://172.22.129.1:8361' # 李波搭建的bdp传输后台 外网http://47.89.187.14:8361 内网：http://172.22.129.1:8361
# yx_socks5_proxy = {"http": "socks5://127.0.0.1:1080",
#                    "https": "socks5://127.0.0.1:1080"}
yx_socks5_proxy = {
    "http": "http://bdp-proxy:okbdp@161.117.59.90:80",  # "http://47.101.168.174:8899",
    "https": "http://bdp-proxy:okbdp@161.117.59.90:80",  # "http://47.101.168.174:8899"
}
# 走[国内代理]的好处，因为[BDP服务器]在北京，[BDP服务器]本身有超时机制，传输数据超时就触发连接中断错误，导致各种connection abort,ssl oef,enconet等错误
# 数据从[美东]->[国内代理]，因为[国内代理]自己设置的，不存在[美东]->[国内代理]有数据超时的问题
# 如果是[国内代理]-->[BDP服务器]，因为国内传输很快，所以就不会触发BDP的超时机制
use_socks5_proxy = False
need_redirect = False
VERSION = "1.0.3"


class OpenDSException(Exception):
    pass


class OpenDS:
    token = None

    def __init__(self, token=None, domain=None):
        self.url_prefix = opends_api_url_prefix
        requests.packages.urllib3.disable_warnings()
        self.token = token
        if need_redirect:
            self.url_prefix = self.service_uri(domain)

    def public_request(self, url, payload=None, param=None):
        if not payload:
            payload = {}
        if not param:
            param = {}
        param['_t'] = time.time()
        param['access_token'] = self.token
        try_count = 0
        result = {}
        while True:
            try:
                params = u'%s' % urllib.parse.urlencode(param)
                _url = "%s?%s" % (url, params)
                # BMOBJ.log_error("requests default retry count: %s" %
                #                 requests.adapters.DEFAULT_RETRIES)
                if payload:
                    headers = {
                        'Content-type': 'text/html;charset=utf-8',
                        # 'Content-Encoding': 'gzip',
                        "User-Agent": "bdp-sdk-python, {version}".format(version=VERSION)
                    }
                    payload_str = u'%s' % json.dumps(payload)
                    # gzip
                    # s = io.StringIO() #only python2
                    # g = gzip.GzipFile(fileobj=s, mode='w')
                    if 0:
                        s = six.BytesIO()  # python 3
                        payload_str = payload_str.encode("utf8")
                        g = gzip.GzipFile(fileobj=s, mode='w')
                        g.write(payload_str)
                        g.close()
                    else:
                        payload_str = payload_str.encode("utf8") # 不用gzip的方式
                    if use_socks5_proxy:
                        res = requests.post(
                            _url, data=payload_str, headers=headers, verify=False, timeout=(60, 3600), proxies=yx_socks5_proxy).text  # 连接超时60秒，读取超时3600秒
                    else:
                        res = requests.post(
                            _url, data=payload_str, headers=headers, verify=False, timeout=(60, 3600)).text  # 连接超时60秒，读取超时3600秒
                else:
                    headers = {
                        'Content-type': 'text/html;charset=utf-8',
                        # 'Content-Encoding': 'gzip',
                        "User-Agent": "bdp-sdk-python, {version}".format(version=VERSION)
                    }
                    if use_socks5_proxy:
                        res = requests.get(
                            _url, headers=headers, verify=False, timeout=(60, 3600), proxies=yx_socks5_proxy).text  # 连接超时60秒，读取超时3600秒
                    else:
                        res = requests.get(
                            _url, headers=headers, verify=False, timeout=(60, 3600)).text  # 连接超时60秒，读取超时3600秒
                result = json.loads(res)

                break
            except requests.exceptions.ConnectTimeout as e:  # 连接超时，可以重试
                try_count += 1
                BMOBJ.log_error(
                    'can not connect to server, retry ... | reason: %s' % str(e))
                time.sleep(5)
                if try_count == 5:
                    raise e
            except requests.exceptions.ReadTimeout as e1:  # 读取错误，不要重试，否则会出现数据重复或者重复commit的现象
                raise e1
            # ECONNRESET错误不能重试
            # HttpServer默认设置了超时时间为2分钟，当一个请求的处理时间超过2分钟，HttpServer会自动将该请求的socket关闭掉，于是客户端便收到了 ECONNRESET 的错误信息了
            # 修改每次上传的最大条数可以减少这个ECONNRESET的出现问题
            # 例如: (Caused by SSLError(SSLError("bad handshake: SysCallError(104, 'ECONNRESET')",),))
            # except IOError as e3: # 有时候是其他IO错误
            #     try_count += 1
            #     BMOBJ.log_error(
            #         'can not connect to server, retry ... | reason: %s' % str(e3))
            #     time.sleep(5)
            #     if try_count == 5:
            #         raise e3
            except Exception as e2:
                raise e2

        try:
            BMOBJ.log_error(u'api:%s\t request_id:%s' % (
                '/'.join(url.split('/')[-2:]), result.get('request_id', '')))
        except Exception as e:
            BMOBJ.log_error("log_error error")
        if not result:
            error_msg = "\nstatus: {status}\nerror_str: {errstr}\nrequest_id: {req_id}".format(
                status="-1",
                errstr="connection failed",
                req_id=""
            )
            raise OpenDSException(error_msg)
        if result['status'] != '0':

            error_msg = "\nstatus: {status}\nerror_str: {errstr}\nrequest_id: {req_id}".format(
                status=result['status'],
                errstr=result['errstr'],
                req_id=result.get('request_id', '')
            )
            raise OpenDSException(error_msg)
        return result

    def _request(self, url, payload=None, param=None):
        result = self.public_request(url, payload, param)
        return result['result']

    def _request_yx(self, url, payload=None, param=None):
        result = self.public_request(url, payload, param)
        return (result['result'], result.get('request_id', 'no_request_id'))

    def ds_create(self, token, name):
        url = '%s/api/ds/create' % self.url_prefix
        params = {
            'access_token': token,
            'name': name,
            'type': 'opends'
        }
        return self._request(url, param=params)

    def ds_list(self, token):
        url = '%s/api/ds/list' % self.url_prefix
        params = {
            'access_token': token
        }
        return self._request(url, param=params)

    def ds_delete(self, token, ds_id):
        url = '%s/api/ds/delete' % self.url_prefix
        params = {
            'access_token': token,
            'ds_id': ds_id
        }
        return self._request(url, param=params)

    def tb_create(self, token, ds_id, name, schema, uniq_key, title=None):
        url = '%s/api/tb/create' % self.url_prefix
        params = {
            'access_token': token,
        }
        data = {
            'ds_id': ds_id,
            'name': name,
            'schema': schema,
            'uniq_key': uniq_key
        }
        if title:
            data['title'] = title

        return self._request(url, param=params, payload=data)

    def tb_name_modify(self, token, tb_id, alias_name):
        url = '%s/api/tb/modify' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': alias_name
        }
        return self._request(url, param=params)

    def tb_delete(self, token, tb_id):
        url = '%s/api/tb/delete' % self.url_prefix

        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def tb_list(self, token, ds_id):
        url = '%s/api/tb/list' % self.url_prefix
        params = {
            'access_token': token,
            'ds_id': ds_id
        }
        return self._request(url, param=params)

    def tb_info(self, token, tb_id):
        url = '%s/api/tb/info' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def tb_clean(self, token, tb_id):
        url = '%s/api/tb/clean' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def tb_commit(self, token, tb_id):
        url = '%s/api/tb/commit' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fast': 0
        }
        return self._request(url, param=params)

    def tb_merge(self, token, tb_id):
        url = '%s/api/tb/commit' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fast': 0
        }
        return self._request(url, param=params)

    def tb_update(self, token, tb_ids):
        url = '%s/api/tb/update' % self.url_prefix
        params = {
            'access_token': token,
            'tb_ids': json.dumps(tb_ids)
        }
        return self._request(url, param=params)

    def tb_insert(self, token, tb_id, fields, data):
        url = '%s/api/tb/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def tb_insert_by_id(self, token, tb_id, fields, data):
        url = '%s/api/tb/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def data_insert(self, token, tb_id, fields, data):
        url = '%s/api/data/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def data_insert_by_id(self, token, tb_id, fields, data):
        url = '%s/api/data/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def tb_preview(self, token, tb_id):
        url = '%s/api/tb/preview' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
        }
        return self._request(url, param=params)

    def tb_revert(self, token, tb_id):
        url = '%s/api/tb/revert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
        }
        return self._request(url, param=params)

    def field_list(self, token, tb_id):
        url = '%s/api/field/list' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def field_del(self, token, tb_id, name):
        url = '%s/api/field/delete' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': name
        }
        return self._request(url, param=params)

    def field_add(self, token, tb_id, name, type, uniq_index, title=None):
        url = '%s/api/field/add' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': name,
            'type': type,
            'uniq_index': uniq_index
        }
        if title is not None:
            params["title"] = title

        return self._request(url, param=params)

    def field_modify(self, token, tb_id, name, f_type, uniq_index, title=None):
        url = '%s/api/field/modify' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': name,
            'type': f_type,
            'uniq_index': uniq_index
        }
        if title is not None:
            params["title"] = title
        return self._request(url, param=params)

    def data_update(self, token, tb_id, fields, data):
        url = "%s/api/data/update" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_update_by_id(self, token, tb_id, fields, data):
        url = "%s/api/data/update" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_delete(self, token, tb_id, fields, data):
        url = "%s/api/data/delete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_delete_by_id(self, token, tb_id, fields, data):
        url = "%s/api/data/delete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_bulkdelete(self, token, tb_id, where):
        url = "%s/api/data/bulkdelete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'where': where
        }
        return self._request(url, param=params)

    def data_bulkdelete_yx(self, token, tb_id, where):
        url = "%s/api/data/bulkdelete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'where': where
        }
        return self._request_yx(url, param=params)

    def service_uri(self, domain):
        url = "%s/api/service/uri" % self.url_prefix
        params = {
            'domain': domain,
        }
        return self._request(url, param=params)

    def service_error(self):
        url = "%s/api/service/error" % self.url_prefix
        return self._request(url)
