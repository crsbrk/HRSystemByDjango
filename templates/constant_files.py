# 员工名单不再写死，改为从注册用户动态生成。
# 业务录入的人员下拉见 accounts.workers.worker_name_choices；
# scores 排名见 scores.views.collect_worker_names / get_worker_profiles；
# 民主测评见 scores.models.DemocracyRating（测评人/被测评人均关联注册用户）。

FAULTY_SCORE_LIST=(
    (0,0),(1,1),(2,2)

)

ROUTINE_SCORE_LIST=(
    (0,0),(1,1),(2,2),(3,3),

)

ORDER_SCORE_LIST=(
    (0,0),(1,1),

)

DEMOCRACY_LIST =(
(100,100),(90,90),(80,80),(70,70),(60,60),(50,50),(40,40),(30,30),(20,20),(10,10),(0,0),
)

ORDER_TYPES = (
        ('行业', '行业'),
        ('物联网', '物联网'),
        ('内容计费', '内容计费'),
        ('DNS', 'DNS'),
        ('PCRF/PCF', 'PCRF/PCF'),
        ('国际漫游', '国际漫游'),
        ('SGSN/MME局数据', 'SGSN/MME局数据'),
        ('SGW/PGW局数据', 'SGW/PGW局数据'),
        ('AMF', 'AMF'),
        ('SMF', 'SMF'),
        ('NRF', 'NRF'),
        ('UPF', 'UPF'),
        ('数通', '数通'),
        ('网管', '网管'),
        ('I层', 'I层'),
        ('其他', '其他'),
    )
FAULTY_TYPES =(
        ('硬件', '硬件'),
        ('软件', '软件'),
        ('投诉', '投诉'),
        ('其他', '其他'),
    )

JOB_TYPES =(
        ('物联网', '物联网'),
        ('公众', '公众'),
        ('数通', '数通'),
        ('其他', '其他'),
    )
MANUFA_TYPES = (
        ('华为', '华为'),
        ('中兴', '中兴'),
        ('诺基亚', '诺基亚'),        
        ('思科', '思科'),
        ('神州数码', '神州数码'),
        ('恒安嘉新', '恒安嘉新'),
        ('其他', '其他'),
    
)
POST_SCORE_FLAG = 1
CUTOVER_SCORE_FLAG = 2
ORDERS_SCORE_FLAG = 3
BONUSES_SCORE_FLAG = 4
FAULTY_SCORE_FLAG = 5
ROUTINE_SCORE_FLAG = 6

POST_LAMADA = 0.05
ORDER_LAMADA = 0.05
CUTOVER_LAMADA = 0.1
BONUS_LAMADA = 0
FAULTY_LAMADA = 0.05
ROUTINE_LAMADA = 0.01

POST_SHARE = 11.525
ORDER_SHARE = 15.5
CUTOVER_SHARE = 15.5
BONUS_SHARE = 15.5
ROUTINE_SHARE = 15.5
FAULTY_SHARE = 11.525

SEASON_LIST = ('第一季度','第二季度','第三季度','第四季度')
MONTH_LIST = ('第十二月','第一月','第二月','第三月','第四月','第五月','第六月','第七月','第八月','第九月','第十月','第十一月','第十二月')
