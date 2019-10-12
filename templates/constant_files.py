WORKERS_NAMES = (
    ('陈立栋', '陈立栋'),
    ('常晓波', '常晓波'),
    ('刘江', '刘江'),
    ('刘雷', '刘雷'),
    ('刘峰', '刘峰'),
    # ('冯庆', '冯庆'),
    ('郭少钏', '郭少钏'),
    ('于秋思', '于秋思'),
    ('苏飓', '苏飓'),
    ('苏伟衡', '苏伟衡'),
    ('杨晓', '杨晓'),
    ('霍晓歌', '霍晓歌'),
    ('李晓昕', '李晓昕'),
    ('张晨', '张晨'),
)

JIXIAO11 = {
    '陈立栋': {'scoreAll':0,'jx':0},
    '常晓波': {'scoreAll':0,'jx':0},
    '刘江': {'scoreAll':0,'jx':0},
    '刘雷': {'scoreAll':0,'jx':0},
    '刘峰': {'scoreAll':0,'jx':0},
    '冯庆': {'scoreAll':0,'jx':0},
    '郭少钏': {'scoreAll':0,'jx':0},
    '于秋思': {'scoreAll':0,'jx':0},
    '苏飓': {'scoreAll':0,'jx':0},
    '苏伟衡': {'scoreAll':0,'jx':0},
    '杨晓': {'scoreAll':0,'jx':0},
    '霍晓歌': {'scoreAll':0,'jx':0},
    '李晓昕': {'scoreAll':0,'jx':0},
    '韦国锐': {'scoreAll':0,'jx':0},
    '张晨': {'scoreAll':0,'jx':0},
}

JIXIAO= {
    '陈立栋': [0,0],
    '常晓波': [0,0],
    '刘江': [0,0],
    '刘雷': [0,0],
    '刘峰': [0,0],
    '冯庆': [0,0],
    '郭少钏': [0,0],
    '于秋思': [0,0],
    '苏飓': [0,0],
    '苏伟衡': [0,0],
    '杨晓': [0,0],
    '霍晓歌': [0,0],
    '李晓昕': [0,0],
    '韦国锐': [0,0],
    '张晨': [0,0],

}

FAULTY_SCORE_LIST=(
    (1,1),(2,2)

)

ROUTINE_SCORE_LIST=(
    (1,1),

)

ORDER_SCORE_LIST=(
    (1,1),

)
ORDER_TYPES = (
        ('行业', '行业'),
        ('物联网', '物联网'),
        ('内容计费', '内容计费'),
        ('DNS', 'DNS'),
        ('PCRF', 'PCRF'),
        ('国际漫游', '国际漫游'),
        ('SGSN/MME局数据', 'SGSN/MME局数据'),
        ('SGW/PGW局数据', 'SGW/PGW局数据'),
        ('其他', '其他'),
    )
FAULTY_TYPES =(
        ('硬件', '硬件'),
        ('投诉', '投诉'),
        ('软件', '软件'),
        ('其他', '其他'),
    )

scoreOfAllWorkers = {
   '陈立栋': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
   '常晓波': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '刘江': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '刘雷': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '刘峰': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '冯庆': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '郭少钏': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '于秋思': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '苏飓': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '苏伟衡': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '杨晓': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '霍晓歌': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
    '李晓昕': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
   '韦国锐': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
   '张晨': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0},
}

POST_SCORE_FLAG = 1
CUTOVER_SCORE_FLAG = 2
ORDERS_SCORE_FLAG = 3
BONUSES_SCORE_FLAG = 4
FAULTY_SCORE_FLAG = 5
ROUTINE_SCORE_FLAG = 6

WLW_NUMBERS = 4 #物联网组：刘雷，刘江，刘峰,yangxiao
SHUTONG_NUMBERS = 3 #数通组：常晓波，于秋思，苏伟衡
GONGZHONG_NUMBERS = 5 #公众组：杨晓，霍晓歌，苏飓，张晨，李晓昕，郭少钏
OTHERS_NUMBERS = 8 #非物联网
ALL_WORKER_NUMBERS = 12 #all