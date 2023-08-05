"""
封装一些基础方法
"""


class BaseTga(object):
    def __init__(self):
        pass

    def tran_dt_by_zone(self, field_name, field_zone_offset, target_offset=0):
        """
        @des: 调用
        tran_zone_sql = cobj.tran_zone_sql(a."#event_time", a."#zone_offset", 0)  # 统一转为utc
        例如：
            # 加载
            from hv_user_predit_tf_2.src.common.config import Config as GAConfig
            gconf = GAConfig.getInstance()
            # 日期分为part_date的范围和event_time的范围， part_date的范围适当取大
            part_date = '2020-12-01'
            et_start = arrow.get(part_date).format("YYYY-MM-DD")
            et_end = arrow.get(part_date).shift(days=1).format("YYYY-MM-DD")
            #---------------
            SELECT
                *
            FROM (
                SELECT
                    "#user_id",
                    {gconf.tran_dt_by_zone("#event_time", "#zone_offset", 0)} as event_time_utc,
                    "$part_event"
                FROM
                    v_event_64
                WHERE
                    "$part_event" = 'new_device'
                    ---- "$part_date"的取值必须比event_time的范围大2天，因为有时区的问题
                    AND "$part_date" >= '{arrow.get(et_start).shift(days=-2).format("YYYY-MM-DD")}'
                    AND "$part_date" <= '{arrow.get(et_end).shift(days=2).format("YYYY-MM-DD")}'
            )
            WHERE
                event_time_utc >= timestamp '{et_start}'
                AND event_time_utc < timestamp '{et_end}'
                -- AND to_unixtime(current_timestamp)-to_unixtime(event_time_utc) >= 43200 --注册时间必须大于12小时【可选，模型会根据数据去判断是否是优质用户，如果第一次预测不是，可能第二次预测就是了】
        """
        sql = f"""
if(
    "{field_zone_offset}" is not null,
    date_add(
        'second',
        cast((0 - "{field_zone_offset}") * 3600 + {target_offset*3600}  as integer),
        "{field_name}"
    ),
    "{field_name}"
) 
"""
        return sql
