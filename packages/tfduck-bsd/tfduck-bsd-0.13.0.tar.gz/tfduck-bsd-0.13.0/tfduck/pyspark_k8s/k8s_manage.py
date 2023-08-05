"""
auhtor: yuanxiao
datetime: 20210423
python3.8
pyspark 提交阿里云ask集群管理器
pip install kubernetes==12.0.1
"""
import json
from tfduck.common.defines import BMOBJ, Et
from tfduck.oss.oss import AliyunOss
from kubernetes import client, config
import uuid
import arrow
import os
import base64
import subprocess


class K8sManage(object):
    """
    """

    def __init__(self, ctx, k8s_conn_config="~/.kube/config"):
        """
        """
        """
        全局初始化
        """
        self.ctx = ctx
        self.k8s_conn_config = k8s_conn_config
        """
        生成k8s客户端
        """
        self.get_k8s_client()

    def get_k8s_client(self):
        """
        @des: 获取k8s操作客户端
        例子  https://github.com/kubernetes-client/python/tree/master/examples
        api文档 https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
        """
        config.load_kube_config(self.k8s_conn_config)
        v1 = client.CoreV1Api()
        self.k8s_client = v1
        # print("Listing pods with their IPs:")
        # ret = v1.list_pod_for_all_namespaces(watch=False)
        # for i in ret.items:
        #     print("%s\t%s\t%s" %
        #           (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def get_all_pods(self):
        """
        @des: 获取所有的k8s的pod, 默认命名空间的
        """
        # print("Listing pods with their IPs:")
        ret = self.k8s_client.list_pod_for_all_namespaces(watch=False)
        pod_infos = []
        for i in ret.items:
            if i.metadata.namespace == "default":
                pod_infos.append({'name': i.metadata.name,
                                  'status': i.status.phase,
                                  'create_time': i.metadata.creation_timestamp})
        return pod_infos

    def get_pod_info(self, pod_name):
        """
        @des: 获取pod的基础信息，状态等信息
        """
        # resp = self.k8s_client.read_namespaced_pod_status(
        #     name="tfspark-test-7200-driver-1e5ab8f2a41d11eb93c3acde48001122", namespace='default')
        # resp = self.k8s_client.read_namespaced_pod(
        #     name="tfspark-test-7200-driver-1e5ab8f2a41d11eb93c3acde48001122", namespace='default')
        pod_obj = self.k8s_client.read_namespaced_pod(
            name=pod_name, namespace='default')
        # print(resp)
        # print(resp.metadata.name, resp.status.phase)
        # return resp.status.phase # Pending,Succeeded, Running, Failed
        return pod_obj

    def get_pod_log(self, pod_name, lines_count=1000):
        """
        @des: 获取pod的日志--测试成功
        """
        # print(help(self.k8s_client.read_namespaced_pod_log))
        # log_content = self.k8s_client.read_namespaced_pod_log(
        #     'tfspark-test-7200-driver-c697aadea41d11eb9d2bacde48001122', 'default', pretty=True, tail_lines=1)  # container='spark-kubernetes-driver'
        log_content = self.k8s_client.read_namespaced_pod_log(
            pod_name, 'default', pretty=True, tail_lines=lines_count)  # tail_lines 表示从结尾开始获取日志的行数
        # print(log_content)
        return log_content

    # def patch_pod_info(self, pod_name):
    #     """
    #     @des: 修改pod的信息，包括状态
    #     """
    #     pod_obj = self.get_pod_info(pod_name)
    #     pod_obj.status.phase = ""
    #     # print(help(self.k8s_client.patch_namespaced_pod))
    #     self.k8s_client.patch_namespaced_pod(pod_name, 'default', pod_obj)

    def delete_pod(self, pod_name):
        """
        @des: 删除pod
        delete是删除---
        delete_namespaced_pod
        """
        # print(help(self.k8s_client.delete_namespaced_pod))
        # pod_obj = self.get_pod_info(pod_name)
        # print(pod_obj.metadata.name, pod_obj.metadata.creation_timestamp, pod_obj.status.phase)
        # pod_create = pod_obj.metadata.creation_timestamp
        # status = pod_obj.status.phase
        r = self.k8s_client.delete_namespaced_pod(pod_name, 'default')
        return r


if __name__ == "__main__":
    sm = K8sManage(ctx={}, k8s_conn_config="~/.kube/config")
    print(sm.get_pod_info("tfspark-test111-7200-driver-d883cda4a63411ebb0e70242ac110002").status.phase)
    # sm.get_pod_log("tfspark-test-7200-driver-3b7d45b8a57011eb8accacde48001122")
    # print(sm.delete_pod("tfspark-test-7200-driver-d4d431fea57511eb86e3acde48001122"))
    # print(sm.get_all_pods())
