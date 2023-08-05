'''
@des: tga获取批量转换特征值数据拉取的sql基类


准备工作: 
--------------------------------------
gconf的属性有这些:
########
   part_date_start  # 特征值取新增用户的开始日期, 例如"2022-05-20", 字符串类型
   part_date_end    # 特征值取新增用户的结束日期, 例如"2022-05-25", 字符串类型
   level_durs       # 特征取值段，由小到大排列, 例如 [43200, 43200*2], 这里是秒为单位，整型数组；多少时间段发生事件作为特征值
   tga_user_table   # tga用户表名, 例如 "v_user_7", 字符串
   tga_event_table  # tga用户表名, 例如 "v_user_7", 字符串 
########

如何使用(需要自己定义一个子类继承这个类， 代码如下): 
#######
from magic_number_train_tf_2.src.common.config import Config as GAConfig # 这里换成你自己的项目
from tfduck.tga.predict_sql_yh import PredictFeatureSql

def call_method(self, ctx=None, **kwargs):
    """
    @des: 每个具体项目的训练特征数据拉取 
    """
    gconf = GAConfig.getInstance()  # 保证gconf有上面准备工作的属性
    """
    设置项目属性-----下面的都需要自己配置------
    """
    # 需要的事件
    need_events = (
        'new_device', 'new_session', 'act_level_path'
    )
    # 需要的属性
    need_event_attrs = (
        "#lib", "#country_code", "$part_event", "#user_id",  "sdk_session_time",
        "object_type", "act", "object_number", "act_object",
    )
    # 特征值名称(不要用字母a作为key)---
    feature_names = {
        'b': '常规关卡通关',
        'c': '冒险关卡通关'
    }
    # 特征值sql---模板保持不变，变里面的内容即可---
    sub_sql_fs = {
        'b':            """
                        --%(real_des)s
                        sum(
                            if(
                            "$part_event"='act_level_path' and object_type='normal' and act='win' and rt_dur<%(level_dur)s,
                            1, 
                            0)
                        ) as %(sub_field_name)s
                        """,
        'c':            """
                        --%(real_des)s
                        sum(
                            if(
                            "$part_event"='act_level_path' and object_type='adventure' and act='win' and rt_dur<%(level_dur)s,
                            1, 
                            0)
                        ) as %(sub_field_name)s
                        """
    }        
    """
    创建调用实例---最好通过dict创建实例
    """         
    pf_sql_obj = PredictFeatureSql(
            ctx = ctx, 
            gconf = gconf, 
            need_events = need_events, 
            need_event_attrs = need_event_attrs, 
            feature_names = feature_names,
            sub_sql_fs = sub_sql_fs
    )  
    sql = pf_sql_obj.get_sql() # 这个sql就是拉取特征值的sql
#######
'''
from tfduck.common.defines import BMOBJ, Et
from tfduck.tga.predict_sql_retain import PredictFeatureSql as BasePredictFeatureSql
import arrow


class PredictFeatureSql(BasePredictFeatureSql):
    """
    @des:sql批量转换模板基类
    """
    pass