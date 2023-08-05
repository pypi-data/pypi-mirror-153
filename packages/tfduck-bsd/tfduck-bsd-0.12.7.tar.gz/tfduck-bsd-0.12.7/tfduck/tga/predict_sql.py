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
from tfduck.tga.train_sql import PredictFeatureSql

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
    # 特征值名称--第一项固定填写---
    feature_names = {
        self.base_user_table: '用户属性和标签',  # 此属性固定sql，不需要拼接
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
from tfduck.tga.base_tga import BaseTga
import arrow


class PredictFeatureSql(BaseTga):
    """
    @des:sql批量转换模板基类
    """

    def __init__(self,
                 ctx=None,
                 gconf=None,
                 need_events=None,
                 need_event_attrs=None,
                 feature_names=None,
                 sub_sql_fs=None,
                 **kwargs):
        """
        @des: 参数说明看上面的文档说明
        """
        self.gconf = gconf
        self.ctx = ctx
        # 基础属性
        self.label_col = "is_rd"
        self.base_event_table = 'all_need_event'
        self.base_user_table = 'a'
        self.base_feature_table = 'features_t'
        self.nav_neg_multi = 2  # 负正样本比例
        # 项目属性
        self.need_events = need_events
        self.need_event_attrs = need_event_attrs
        self.feature_names = feature_names
        self.sub_sql_fs = sub_sql_fs
        # 其他属性
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_real_feature_names(self, mode='d'):
        """
        @des: 获取真正的特征值列表
        """
        real_features_names = {}
        sub_len = len(self.gconf.level_durs)
        for k, v in self.feature_names.items():
            if k != self.base_user_table:
                for i in range(sub_len):
                    if mode == 'h':
                        rv = f"{v}_{int(self.gconf.level_durs[i]/3600)}h"
                    else:
                        js = self.gconf.level_durs[i]/86400
                        if js == int(js):
                            js = int(js)
                        else:
                            js = round(js, 1)
                        rv = f"{v}_{js}d"
                    real_features_names[f"{k}_{i}_v"] = rv
        return real_features_names

    def get_threshold_sql(self, col_name):
        """
        @des: 根据col_name例如 g_1_v获取特征值计算的sql
        """
        first_col_name, second_col_index = col_name.split(
            "_")[0], col_name.split("_")[1]
        sub_field_name = "%s_%s_v" % (first_col_name, second_col_index)
        level_dur = self.gconf.level_durs[int(second_col_index)]
        real_des = "%s %s" % (
            self.feature_names.get(first_col_name), level_dur)
        f_sub_sql = self.sub_sql_fs.get(first_col_name)
        if not f_sub_sql:
            raise Et(2, f"error first_col_name {first_col_name}")
        sub_sql = f_sub_sql % {
            "real_des": real_des, "level_dur": level_dur, 'sub_field_name': sub_field_name}
        return sub_sql

    def get_sql_config(self):
        """
        @des: 计算各种时间间隔和配置，统一从一个方法读取，后面方便改
        """
        gconf = self.gconf
        #
        part_date_start = gconf.part_date_start
        part_date_end = gconf.part_date_end
        days = (arrow.get(part_date_end)-arrow.get(part_date_start)).days
        # 取用户新增后的N天作为事件池数据来取特征值，比如7日预测14日，就取8-9比较合适，根据level_durs[-1]决定
        after_feature_day = int(gconf.level_durs[-1]/86400)+2  # 多取两天即可
        feature_date_end = arrow.get(part_date_end).shift(days=after_feature_day).format(
            "YYYY-MM-DD")  # 增加到8天的事件数据，因为现在有7日预测30日
        # label_durs = gconf.label_durs
        # label_date_start = arrow.get(part_date_start).shift(
        #     days=int(label_durs[0]/86400)-2).format("YYYY-MM-DD")
        # label_date_end = arrow.get(part_date_end).shift(
        #     days=int(label_durs[1]/86400)+2).format("YYYY-MM-DD")
        #
        new_device_start = arrow.get(part_date_start).format("YYYY-MM-DD")
        new_device_end = arrow.get(part_date_end).shift(
            days=1).format("YYYY-MM-DD")
        return {
            "days": days,
            'part_date_start': part_date_start,
            'part_date_end': part_date_end,
            'feature_date_end': feature_date_end,
            # 'label_date_start': label_date_start,
            # 'label_date_end': label_date_end,
            'new_device_start':  new_device_start,
            'new_device_end':  new_device_end
        }

    def get_event_sql(self):
        """
        @des: 获取N日留存用户的事件
        """
        gconf = self.gconf
        comm_cc = self.get_sql_config()
        #
        sql = f"""
    -- des: add by yuanxiao for machine learn predict
    with new_user as (
        -- 获取指定日期的注册用户 连接 这些用户在7-10天后的触发的事件
        SELECT
            a1.user_register_time as user_register_time,
            a1."#user_id" as user_user_id
        FROM
        (
            -- 获取指定日期的注册用户,以防万一，使用窗口函数去个重
            SELECT
                *
            FROM
            (
                SELECT
                    *,
                    row_number()  OVER  (PARTITION  BY  "#user_id") AS  row_no
                FROM
                (
                    SELECT
                        b.event_time_utc as user_register_time, a."#user_id"
                    FROM
                    (
                        SELECT
                            "#user_id"
                        FROM
                            {gconf.tga_user_table}
                    ) a
                    INNER JOIN
                    (
                        SELECT
                            *
                        FROM (
                            SELECT
                                "#user_id",
                                {self.tran_dt_by_zone("#event_time", "#zone_offset", 0)} as event_time_utc,
                                "$part_event"
                            FROM
                                {gconf.tga_event_table}
                            WHERE
                                "$part_event" = 'new_device'
                                AND "$part_date" >= '{arrow.get(comm_cc["new_device_start"]).shift(days=-2).format("YYYY-MM-DD")}'
                                AND "$part_date" <= '{arrow.get(comm_cc["new_device_end"]).shift(days=2).format("YYYY-MM-DD")}'
                        )
                        WHERE
                            event_time_utc >= timestamp '{comm_cc["new_device_start"]}'
                            AND event_time_utc < timestamp '{comm_cc["new_device_end"]}'
                    ) b
                    ON a."#user_id" = b."#user_id"
                )
            )
            WHERE row_no=1
        ) a1
    )
    , all_need_event as (
        SELECT
            *
        FROM (
            -- 获取正负标签样本需要的事件
            select 
                a5.user_register_time,
                a5.user_user_id,
                floor(to_unixtime(b5.event_time_utc))-floor(to_unixtime(a5.user_register_time)) as rt_dur,
                c5."afrawip__meida_source" as "afrawip__meida_source_ikfdssausercommonend",
                c5."#account_id" as "#account_id_ikfdssausercommonend",
                c5."#distinct_id" as "#distinct_id_ikfdssausercommonend",
                b5.*,
                b5.event_time_utc as "#event_time"
            from 
                new_user a5
            INNER JOIN
            (
                SELECT
                    *
                FROM (
                    SELECT
                        -- *
                        {','.join(['"%s"'%x for x in self.need_event_attrs])},
                        {self.tran_dt_by_zone("#event_time", "#zone_offset", 0)} as event_time_utc
                    FROM
                        {gconf.tga_event_table}
                    WHERE
                        "$part_date" >= '{arrow.get(comm_cc["part_date_start"]).shift(days=-2).format("YYYY-MM-DD")}'
                        AND "$part_date" <= '{arrow.get(comm_cc["feature_date_end"]).shift(days=2).format("YYYY-MM-DD")}'
                        AND "$part_event" in ({','.join(["'%s'"%x for x in self.need_events])})
                )
                WHERE
                    event_time_utc >= timestamp '{comm_cc["part_date_start"]}'
                    AND event_time_utc <= timestamp '{comm_cc["feature_date_end"]}'    
            )
            as b5
            ON a5.user_user_id = b5."#user_id"
            INNER JOIN
            (
                SELECT
                    "#user_id","afrawip__meida_source","#account_id","#distinct_id"
                FROM
                    {gconf.tga_user_table}
            )
            as c5
            ON a5.user_user_id = c5."#user_id"
        )  a6
        WHERE
        rt_dur<={gconf.level_durs[-1]}  -- N小时内的事件
    ) 
    """
        return sql

    def get_sub_sql_i(self, sub_sql_f, col_name, col_des, base_event_table='all_need_event', base_user_table='a'):
        """
        @des: 内部调用
        """
        gconf = self.gconf
        sub_field_f = "%(col)s_%(dur_i)s"
        real_des_f = "%(des)s %(dur_i)s"
        sub_field_names = []
        sub_sqls = []
        for _dur_i, level_dur in enumerate(gconf.level_durs):
            real_des = real_des_f % {'des': col_des, 'dur_i': _dur_i}
            sub_field_name = sub_field_f % {'col': col_name, 'dur_i': _dur_i}
            sub_field_names.append(sub_field_name)
            # sub_sql_f格式如下
            # sub_sql_f = """
            #     --%(real_des)s
            #     sum(
            #         if(
            #             "$part_event"=='act_level_path' and object_type='normal' and act='win' and rt_dur<%(level_dur)s,
            #             1,
            #             0)
            #     ) as %(sub_field_name)s
            # """
            sub_sql = sub_sql_f % {
                'real_des': real_des,
                'level_dur': level_dur,
                'sub_field_name': sub_field_name
            }
            sub_sqls.append(sub_sql)
        return sub_field_names, sub_sqls

    def get_feature_sql(self):
        """
        @des: 提取特征值的sql
        """
        gconf = self.gconf
        """
        构建level_durs的sql
        """
        base_event_table = self.base_event_table
        base_user_table = self.base_user_table
        base_feature_table = self.base_feature_table
        feature_names = self.feature_names
        #
        sub_sqls = []
        sub_field_names = []

        for col_name, col_des in feature_names.items():
            sub_sql_f = ""
            if col_name == 'a':
                continue
            else:
                sub_sql_f = self.sub_sql_fs.get(col_name)
                if not sub_sql_f:
                    raise Et(2, f"error col_name: {col_name} ")
            # 拼接结果
            if sub_sql_f:
                _sub_field_names, _sub_sqls = self.get_sub_sql_i(
                    sub_sql_f, col_name, col_des)
                sub_sqls.extend(_sub_sqls)
                sub_field_names.extend(_sub_field_names)

        """
        构建select选项
        """
        # 带表名的字段 表名.field
        base_user_table_fields = ["user_user_id", "#account_id_ikfdssausercommonend", "#distinct_id_ikfdssausercommonend",
                                  "afrawip__meida_source_ikfdssausercommonend", "#lib", "#country_code", "user_register_time"]
        sub_selects = ",".join(
            [f"{base_feature_table}.{item} as {item}_v" for item in sub_field_names])
        sub_selects = f"""{",".join(['%s."%s"'%(base_user_table, ptf) for ptf in base_user_table_fields])},{sub_selects}"""
        # 不带表名的字段
        # sub_selects_unique = ",".join(
        #     [f'"{item}_v"' for item in sub_field_names])
        # sub_selects_unique = f"""{",".join(['"%s"'%ptf for ptf in base_user_table_fields])},{sub_selects_unique}"""
        """
        构建sub_sqls
        """
        sub_join_sqls = ",".join(sub_sqls)
        """
        拼接最后的sql
        """
        sql = f"""
    , user_tzz as (
        select 
            {sub_selects}
        from (
                --用户属性和标签
                select 
                    {",".join(['"%s"'%ptf for ptf in base_user_table_fields])}
                from
                (
                    select
                        {",".join(['"%s"'%ptf for ptf in base_user_table_fields])},
                        row_number()  OVER  (PARTITION  BY  user_user_id ORDER  BY  "#event_time" asc) AS  row_no 
                    from 
                        {base_event_table} 
                )
                where
                    row_no=1
        ) {base_user_table} 
        left join
        (   --- 特征值计算
            select
                user_user_id,
                {sub_join_sqls}
            from
                {base_event_table}
            group by user_user_id
        ) {base_feature_table}
        on {base_user_table}.user_user_id={base_feature_table}.user_user_id
    )
    --with语句结束是没有逗号的
    select 
        *
    from 
        user_tzz
    """
        return sql

    def get_sql(self):
        # print("---------------------------------")
        event_sql = self.get_event_sql()
        feature_sql = self.get_feature_sql()
        sql = f"""
    {event_sql}
    {feature_sql} 
    """
        return sql
