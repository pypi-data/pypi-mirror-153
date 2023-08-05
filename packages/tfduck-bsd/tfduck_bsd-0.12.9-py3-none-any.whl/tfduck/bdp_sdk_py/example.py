# coding=utf-8
import datetime
from tfduck.bdp_sdk_py.config.bdpmanager import BdpManager
mlog = print


ISTEST = True  # 为True就是测试模式
BDPTOKEN = 'your token'  # 需要自己填写bdp_token，找相关人员索要
MAX_DATA_LENGTH = 5000
# 定义上传的表的结构
PUBLIC_ACTIVATE_HEADER = (
    ("app_name", "string"),
    ("date", "date"),
    ("country", "string"),
    ("active_count", "number"),
)

PUBLIC_ACTIVATE_HEADER1 = (
    ("app_name", "string"),
    ("date", "date"),
    ("country", "string"),
    ("active_count", "number"),
)

# 定义表名
HEADERDEFINE = {
    "af_active": PUBLIC_ACTIVATE_HEADER,
    "af_active1": PUBLIC_ACTIVATE_HEADER1,
}
# 定义表和表结构映射关系
BDPTABDEFINE = [
    {
        'headers': HEADERDEFINE['af_active'],
        'bdpTbName': "af_active",
    },
    {
        'headers': HEADERDEFINE['af_active1'],
        'bdpTbName': "af_active1",
    },
]


def sync():
    """
    @des: 同步数据
    """
    # 我们进行一个完整的同步到af_active表的操作
    table_name = "af_active"
    # 获取bdp操作实例
    bdpmananger = BdpManager.getInstance(
        BDPTOKEN, "openAPI", BDPTABDEFINE, ISTEST, MAX_DATA_LENGTH)
    # revert 需要操作的表
    bdpmananger.revertTable(table_name)
    # 删除需要更新的数据--避免重复
    dateQuery = {
        "dateUniqKey": "date",
        "begin": "2020-03-25",
        "end": "2020-03-26"
    }
    result = bdpmananger.bulkdeleteTable(
        "af_active", dateQuery, None)
    if not result:
        raise("delete error")
    # 插入数据
    _datas = [["app1", "2020-03-25", "us", 10],
              ["app2", "2020-03-25", "CA", 15]]
    bdpmananger.insertData(table_name, _datas)
    # commit --- commit有时间限制，1个小时只能不能重复commit(可以删除测试表，进行重复commit)
    bdpmananger.commitTable(table_name)
    # update 到 关联表
    bdpmananger.updateTable([table_name])
    # 结束
    print("sync end")


def view_table():
    """
    @des: 预览bdp表里的数据
    """
    table_name = "af_active"
    # 获取bdp操作实例
    bdpmananger = BdpManager.getInstance(
        BDPTOKEN, "openAPI", BDPTABDEFINE, ISTEST, MAX_DATA_LENGTH)
    table = bdpmananger.getTable(table_name)
    data = table.preview()
    data = data["data"]
    data.sort(key=lambda x: x[1])
    mlog(len(data))
    mlog(data)
    # mlog([d for d in data][-10:])
    # mlog([d for d in data][0:10])
    print("view end")


def delete_table():
    """
    @des: 删除bdp的表--小心操作
    """
    table_name = "af_active"
    # 获取bdp操作实例
    bdpmananger = BdpManager.getInstance(
        BDPTOKEN, "openAPI", BDPTABDEFINE, ISTEST, MAX_DATA_LENGTH)
    bdpmananger.deleteTable(table_name)
    print("delete end")


if __name__ == "__main__":
    sync()
    # view_table()
    # delete_table()
