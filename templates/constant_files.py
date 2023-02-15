WORKERS_NAMES = (
    ('陈立栋', '陈立栋'),
    ('陈浚标', '陈浚标'),
    ('黄铭贤', '黄铭贤'),
    ('陆天洋', '陆天洋'),
    ('许海鹏', '许海鹏'),
    ('马梦阳', '马梦阳'),
    ('郭少钏', '郭少钏'),
    ('于秋思', '于秋思'),
    ('苏飓', '苏飓'),
    ('苏伟衡', '苏伟衡'),
    ('彭俊霖', '彭俊霖'),
    ('霍晓歌', '霍晓歌'),
    ('李晓昕', '李晓昕'),
    ('张晨', '张晨'),
    ('汪志武', '汪志武'),
)
NAMES = ('张晨','陈浚标','陈立栋','韦国锐','马梦阳','汪志武','苏飓','霍晓歌','李晓昕','郭少钏','于秋思','苏伟衡','彭俊霖','许海鹏','黄铭贤','陆天洋')

JIXIAO11 = {
    '马梦阳': {'scoreAll':0,'jx':0},
    '陈浚标': {'scoreAll':0,'jx':0},
    '黄铭贤': {'scoreAll':0,'jx':0},
    '陆天洋': {'scoreAll':0,'jx':0},
    '许海鹏': {'scoreAll':0,'jx':0},
    '汪志武': {'scoreAll':0,'jx':0},
    '郭少钏': {'scoreAll':0,'jx':0},
    '于秋思': {'scoreAll':0,'jx':0},
    '苏飓': {'scoreAll':0,'jx':0},
    '苏伟衡': {'scoreAll':0,'jx':0},
    '彭俊霖': {'scoreAll':0,'jx':0},
    '霍晓歌': {'scoreAll':0,'jx':0},
    '李晓昕': {'scoreAll':0,'jx':0},
    '韦国锐': {'scoreAll':0,'jx':0},
    '张晨': {'scoreAll':0,'jx':0},
}

JIXIAO= {
    '马梦阳': [0,0,0],
    '陈浚标': [0,0,0],
    '黄铭贤': [0,0,0],
    '陆天洋': [0,0,0],
    '许海鹏': [0,0,0],
    '汪志武': [0,0,0],
    '郭少钏': [0,0,0],
    '于秋思': [0,0,0],
    '苏飓': [0,0,0],
    '苏伟衡': [0,0,0],
    '彭俊霖': [0,0,0],
    '霍晓歌': [0,0,0],
    '李晓昕': [0,0,0],
    '韦国锐': [0,0,0],
    '张晨': [0,0,0],
    '陈立栋': [0,0,0],

}

NAME_INTERPRETER= {
    '马梦阳': 'mamengyang',
    '陈浚标': 'chenjunbiao',
    '黄铭贤': 'huangmingxian',
    '陆天洋': 'lutianyang',
    '许海鹏': 'xuhaipeng',
    '汪志武': 'wangzhiwu',
    '郭少钏': 'guoshaochuan',
    '于秋思': 'yuqiusi',
    '苏飓': 'suju',
    '苏伟衡': 'suweiheng',
    '彭俊霖': 'pengjunlin',
    '霍晓歌': 'huoxiaoge',
    '李晓昕': 'lixiaoxin',
    '韦国锐': 'weiguorui',
    '张晨': 'zhangchen',
    '陈立栋': 'chenlidong',

}

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

scoreOfAllWorkers = {
   '陈立栋': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
   '陈浚标': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '黄铭贤': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '陆天洋': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '许海鹏': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '汪志武': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '郭少钏': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '于秋思': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '苏飓': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '苏伟衡': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '彭俊霖': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '霍晓歌': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '李晓昕': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '韦国锐': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '张晨': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '马梦阳': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
}


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

WLW_NUMBERS = 4 #物联网组：0
SHUTONG_NUMBERS = 3 #数通组：陈浚标，于秋思，苏伟衡
GONGZHONG_NUMBERS = 5 #公众组：彭俊霖，霍晓歌，苏飓，张晨，李晓昕，郭少钏
OTHERS_NUMBERS = 8 #非物联网
ALL_WORKER_NUMBERS = 12 #all

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
