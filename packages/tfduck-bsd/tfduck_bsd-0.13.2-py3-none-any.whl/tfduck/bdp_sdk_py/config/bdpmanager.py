# coding=utf-8
"""
@des: bdp管理器
bdpmananger = BdpManager.getInstance(BDPTOKEN, "openAPI", BDPTABDEFINE, ISTEST, MAX_DATA_LENGTH)
"""
from tfduck.bdp_sdk_py.opends.opends import OpenDSException
from tfduck.bdp_sdk_py.opends.sdk import BDPClient


def mmlog(*args, **kwargs):
    try:
        if args:
            print(args)
        if kwargs:
            print(kwargs)
    except:
        pass


mlog = mmlog


def getbdpOutputDefine(BDPTABDEFINE):
    bdpOutputDefine = {}
    for obj in BDPTABDEFINE:
        bdpOutputDefine[obj['bdpTbName']] = {
            "headers": obj['headers']
        }
        bdpOutputDefine["test_%s" % obj['bdpTbName']] = {
            "headers": obj['headers']
        }
    return bdpOutputDefine


class BdpManager(object):
    """
    @des
    """

    def __init__(self, bdp_token, bdp_rd, BDPTABDEFINE, ISTEST, MAX_DATA_LENGTH):
        self.client = None
        self.dsData = None
        self.outputHeaders = None
        self.ISTEST = ISTEST
        self.MAX_DATA_LENGTH = MAX_DATA_LENGTH
        self.init(bdp_token, bdp_rd, BDPTABDEFINE)

    @classmethod
    def getInstance(cls, *args, **kwargs):
        return BdpManager(*args, **kwargs)

    def init(self, bdp_token, bdp_rd, BDPTABDEFINE):
        self.outputHeaders = getbdpOutputDefine(BDPTABDEFINE)
        self.client = BDPClient(bdp_token, "*")
        mlog("all ds------------------", self.client.get_all_ds())
        try:
            self.dsData = self.client.get_ds(bdp_rd)
            mlog("bdp init completed")
        except Exception as e:
            mlog("bdp init failed", e)

    def updateTable(self, tableNames):
        """
        @des:触发级联更新，使对该工作表数据进行的操作，对其他由该工作表生成的其他工作表生效。支持批量操作，可同时更新多张工作表。
        @param tableNames 需要被刷新的工作表队列
        """
        tableIds = []
        for tableName in tableNames:
            tableIds.append(self.getTableId(tableName))
        mlog("update TableNames = ", tableNames)
        mlog("update TableIds = ", tableIds)
        result = self.dsData.update(tableIds)
        return result

    def revertTable(self, tableName):
        """
        @des:回滚工作表未提交数据
        将工作表数据回滚到上一次commit的版本。
        @param tableName 工作表名称
        """
        table = self.getTable(tableName)
        result = table.revert()
        mlog("revert table = ", tableName)
        return result

    def insertData(self, tableName, data):
        """
        @des:数据插入的接口
        写入数据须与对应字段一致，包括字段类型和数量；
        数据超过5000行，会做分段发送处理。
        @param tableName 工作表的名称
        @param data 插入的数据格式，数据结构为二维数组 '[["2016-01-12 12:00:22","marry","1"]]'
        """
        MAX_DATA_LENGTH = self.MAX_DATA_LENGTH
        if not isinstance(data, list):
            raise Exception(u"%s需要发送的数据不是数组形式" % tableName)
        dataLength = len(data)
        table = self.getTable(tableName)
        fields = [v[0] for v in self.outputHeaders[tableName]["headers"]]
        if dataLength < 1:
            mlog(u"%s没有数据需要发送" % tableName)
        elif dataLength > MAX_DATA_LENGTH:
            send_count = int(len(data) / MAX_DATA_LENGTH) + 1
            mlog(tableName, u"的数据共,", dataLength,
                 u"超过", MAX_DATA_LENGTH, u"条数据,被拆分成", send_count, u"条来向BDP发送")
            for i in range(send_count):
                _start = i * MAX_DATA_LENGTH
                _end = (i+1) * MAX_DATA_LENGTH
                real_data = data[_start:_end]
                # mlog(tableName, u"分批发送，数据长度 %s"%len(real_data))
                if real_data:
                    table.insert_data_by_name(fields, data[_start:_end])
        else:
            mlog(tableName, u"发送的数据长度", dataLength)
            table.insert_data_by_name(fields, data)

    def commitTable(self, tableName):
        """
        @des:提交工作表的数据
        最近写入数据的操作被保存在缓存文件中，调用该接口可以使操作生效。
        @param tableName 工作表名称
        """
        table = self.getTable(tableName)
        mlog("commit tableName start = ", tableName)
        result = table.commit()
        return result

    def bulkdeleteTable(self, tableName, dateQuery, otherQuery=None):
        """
        @des:
        条件删除
        根据条件删除工作表中数据。
        删除操作将匹配所有符合条件的数据后进行删除，性能不如直接删除，如是根据主键值删除时建议采用直接删除。支持SQL；
        @param tableName 工作表名称
        @param dateQuery BdpQueryDate数据结构，传入开始日期和结束日期，以及索引表头
        @params: dateQuery--{
                              "dateUniqKey": string; // 唯一索引key 'date'
                              "begin": string; // 开始时间"YYYY-MM-DD"
                              "end?": string; // 结束时间"YYYY-MM-DD""
                            }
        """
        table = self.getTable(tableName)
        where = self.createDateWhereQuery(dateQuery)
        if otherQuery is not None:
            where = "%s AND %s" % (where, otherQuery)
        mlog(tableName, "createDateWhereQuery= ", where)
        result = table.bulk_delete_yx(where)
        mlog(tableName, "bulkdeleteTable: ", result, where)
        if result[0] == "success":
            return True
        else:
            return False

    def createDateWhereQuery(self, dateQuery):
        where1 = """ `%s` >= '%s 00:00:00' """ % (
            dateQuery['dateUniqKey'], dateQuery['begin'])
        where2 = """ `%s` < '%s 00:00:00' """ % (
            dateQuery['dateUniqKey'], dateQuery['end'])
        where = "%s AND %s" % (where1, where2)
        return where

    def getTable(self, tableName):
        ISTEST = self.ISTEST
        if ISTEST:
            tableName = "test_%s" % tableName
        if not self.outputHeaders.get(tableName, None):
            # mlog(self.outputHeaders)
            mlog("unkonw tableName1", tableName)
        mlog("opr------------", tableName)
        try:
            table = self.dsData.get_table(tableName)
        except OpenDSException as _:
            headers = self.outputHeaders[tableName]["headers"]
            schema = list(map(lambda header: {
                "name": header[0], "type": header[1]}, headers))
            table = self.dsData.create_table(tableName, schema, uniq_key=None)
        return table

    def getTableId(self, tableName):
        return self.getTable(tableName).get_id()

    def deleteTable(self, tableName):
        ISTEST = self.ISTEST
        if ISTEST:
            tableName = "test_%s" % tableName
            # 只有test才能删除表，如果正式要删除表，需要把下面代码的和if平级
            if not self.outputHeaders.get(tableName, None):
                mlog("unkonw tableName2", tableName)
            try:
                self.dsData.delete_table(tableName)
                mlog("delete table success", tableName)
            except Exception as e:
                mlog("table not exists", tableName, e)
