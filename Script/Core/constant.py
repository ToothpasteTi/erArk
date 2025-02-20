from typing import Dict, List, Set
from types import FunctionType


class CharacterStatus:
    """角色状态id"""

    STATUS_ARDER = 0
    """ 休闲状态 """
    STATUS_MOVE = 1
    """ 移动状态 """
    STATUS_WAIT = 2
    """ 等待 """
    STATUS_CHANGE_CLOTH = 3
    """ 换衣服状态 """
    STATUS_CHAT = 101
    """ 聊天状态 """
    STATUS_CHAT_FAILED = 102
    """ 谈话次数过多的状态 """
    STATUS_STROKE = 103
    """ 身体接触 """
    STATUS_MAKE_COFFEE = 104
    """ 泡咖啡 """
    STATUS_MAKE_COFFEE_ADD = 105
    """ 泡咖啡（加料） """
    STATUS_ASK_MAKE_COFFEE = 106
    """ 让对方泡咖啡 """
    STATUS_MAKE_FOOD = 107
    """ 做饭 """
    STATUS_EAT = 108
    """ 进食状态 """
    STATUS_BUY_FOOD = 109
    """ 购买食物 """
    STATUS_REST = 110
    """ 休息状态 """
    STATUS_SLEEP = 111
    """ 睡觉 """
    STATUS_TAKE_SHOWER = 112
    """ 淋浴 """
    STATUS_FOLLOW = 115
    """ NPC跟随玩家 """
    STATUS_END_FOLLOW = 116
    """ NPC停止跟随玩家 """
    STATUS_APOLOGIZE = 117
    """ 道歉 """
    STATUS_APOLOGIZE_FAILED = 118
    """ 道歉失败 """
    STATUS_LISTEN_COMPLAINT = 119
    """ 听牢骚 """
    STATUS_CONFESSION = 121
    """ 告白 """
    STATUS_CONFESSION_FAILED = 122
    """ 告白失败 """
    STATUS_GIVE_NECKLACE = 123
    """ 戴上项圈 """
    STATUS_GIVE_NECKLACE_FAILED = 124
    """ 戴上项圈失败 """
    STATUS_H = 125
    """ 进入H状态 """
    STATUS_END_H = 126
    """ 结束H状态 """
    STATUS_DO_H_FAIL = 131
    """ 邀请H失败 """
    STATUS_H_HP_0 = 132
    """ H时博士体力为零中断 """
    STATUS_T_H_HP_0 = 133
    """ H时交互对象体力为零中断 """
    STATUS_H_INTERRUPT = 134
    """ H时被人目击闯入中断 """
    STATUS_PEE = 140
    """ 解手 """
    STATUS_CLOTH_OFF = 141
    """ 脱掉全部衣服 """
    STATUS_PUT_SHOWER_CLOTH = 142
    """ 换上浴帽和浴巾 """
    STATUS_PUT_SLEEP_CLOTH = 143
    """ 换上睡衣和内衣 """
    STATUS_WEAR_TO_LOCKER = 144
    """ 身上衣服脱到衣柜 """
    STATUS_LOCKER_TO_WEAR = 145
    """ 衣柜衣服穿回身上 """
    STATUS_SINGING = 151
    """ 唱歌 """
    STATUS_PLAY_INSTRUMENT = 152
    """ 演奏乐器 """
    STATUS_CHECK_LOCKER = 161
    """ 检查衣柜 """
    STATUS_SMELL_UNDERWEAR = 162
    """ 闻内衣 """
    STATUS_OFFICIAL_WORK = 201
    """ 处理公务 """
    STATUS_APPOINTED_ASSISTANT = 204
    """ 指派助理 """
    STATUS_TRAINING = 205
    """ 战斗训练 """
    STATUS_EXERCISE = 206
    """ 锻炼身体 """
    STATUS_CURE_PATIENT = 207
    """ 诊疗病人 """
    STATUS_RECRUIT = 208
    """ 招募干员 """
    STATUS_READ_BOOK = 210
    """ 读书 """
    STATUS_TOUCH_HEAD = 301
    """ 摸头 """
    STATUS_TOUCH_BREAST = 302
    """ 摸胸 """
    STATUS_TOUCH_BUTTOCKS = 303
    """ 摸屁股 """
    STATUS_TOUCH_EARS = 304
    """ 摸耳朵 """
    STATUS_TOUCH_HORN = 305
    """ 摸角 """
    STATUS_TOUCH_TAIL = 306
    """ 摸尾巴 """
    STATUS_TOUCH_RING = 307
    """ 摸光环 """
    STATUS_TOUCH_WING = 308
    """ 摸光翼 """
    STATUS_TOUCH_TENTACLE = 309
    """ 摸触手 """
    STATUS_TOUCH_CAR = 310
    """ 摸小车 """
    STATUS_HAND_IN_HAND = 311
    """ 牵手 """
    STATUS_EMBRACE = 312
    """ 拥抱 """
    STATUS_KISS = 313
    """ 亲吻 """
    STATUS_LAP_PILLOW = 314
    """ 膝枕 """
    STATUS_RAISE_SKIRT = 315
    """ 掀起裙子 """
    STATUS_ASK_FOR_PAN = 316
    """ 索要内裤 """
    STATUS_ASK_FOR_SOCKS = 317
    """ 索要袜子 """
    STATUS_TOUCH_CLITORIS = 331
    """ 阴蒂爱抚 """
    STATUS_TOUCH_VAGINA = 332
    """ 手指插入（V） """
    STATUS_TOUCH_ANUS = 333
    """ 手指插入（A） """
    STATUS_SEE_H = 396
    """ 目睹玩家与其他角色H """
    STATUS_KISS_FAIL = 397
    """ 亲吻失败 """
    STATUS_HIGH_OBSCENITY_ANUS = 398
    """ 重度猥亵失败 """
    STATUS_LOW_OBSCENITY_ANUS = 399
    """ 轻度猥亵失败 """
    STATUS_MAKING_OUT = 401
    """ 身体爱抚 """
    STATUS_KISS_H = 402
    """ 接吻 """
    STATUS_BREAST_CARESS = 403
    """ 胸爱抚 """
    STATUS_TWIDDLE_NIPPLES = 404
    """ 玩弄乳头 """
    STATUS_BREAST_SUCKING = 405
    """ 舔吸乳头 """
    STATUS_CLIT_CARESS = 406
    """ 阴蒂爱抚 """
    STATUS_OPEN_LABIA = 407
    """ 掰开阴唇 """
    STATUS_OPEN_ANUS = 408
    """ 掰开肛门 """
    STATUS_CUNNILINGUS = 409
    """ 舔阴 """
    STATUS_LICK_ANAL = 410
    """ 舔肛 """
    STATUS_FINGER_INSERTION = 411
    """ 手指插入(V) """
    STATUS_ANAL_CARESS = 412
    """ 手指插入(A) """
    STATUS_MAKE_MASTUREBATE = 413
    """ 命令对方自慰 """
    STATUS_MAKE_LICK_ANAL = 414
    """ 命令对方舔自己肛门 """
    STATUS_DO_NOTHING = 415
    """ 什么也不做 """
    STATUS_SEDECU = 416
    """ 诱惑对方 """
    STATUS_HANDJOB = 420
    """ 手交 """
    STATUS_BLOWJOB = 421
    """ 口交 """
    STATUS_PAIZURI = 422
    """ 乳交 """
    STATUS_FOOTJOB = 423
    """ 足交 """
    STATUS_HAIRJOB = 424
    """ 发交 """
    STATUS_AXILLAJOB = 425
    """ 腋交 """
    STATUS_RUB_BUTTOCK = 426
    """ 素股 """
    STATUS_HAND_BLOWJOB = 427
    """ 手交口交 """
    STATUS_TITS_BLOWJOB = 428
    """ 乳交口交 """
    STATUS_FOCUS_BLOWJOB = 429
    """ 真空口交 """
    STATUS_DEEP_THROAT = 430
    """ 深喉插入 """
    STATUS_SIXTY_NINE = 431
    """ 六九式 """
    STATUS_LEGJOB = 432
    """ 腿交 """
    STATUS_TAILJOB = 433
    """ 尾交 """
    STATUS_FACE_RUB = 434
    """ 阴茎蹭脸 """
    STATUS_HORN_RUB = 435
    """ 阴茎蹭角 """
    STATUS_EARS_RUB = 436
    """ 阴茎蹭耳朵 """
    STATUS_BODY_LUBRICANT = 451
    """ 润滑液 """
    STATUS_BIRTH_CONTROL_PILLS_BEFORE = 452
    """ 事前避孕药 """
    STATUS_BIRTH_CONTROL_PILLS_AFTER = 453
    """ 事后避孕药 """
    STATUS_PHILTER = 454
    """ 媚药 """
    STATUS_ENEMAS = 455
    """ 灌肠液 """
    STATUS_DIURETICS_ONCE = 456
    """ 一次性利尿剂 """
    STATUS_DIURETICS_PERSISTENT = 457
    """ 持续性利尿剂 """
    STATUS_SLEEPING_PILLS = 458
    """ 睡眠药 """
    STATUS_SLEEPING_PILLS = 459
    """ 排卵促进药 """
    STATUS_PUT_CONDOM = 471
    """ 戴上避孕套 """
    STATUS_SAFE_CANDLES = 472
    """ 低温蜡烛 """
    STATUS_URETHRAL_SWAB = 473
    """ 尿道棉棒 """
    STATUS_NIPPLES_LOVE_EGG = 481
    """ 乳头跳蛋 """
    STATUS_NIPPLE_CLAMP_ON = 482
    """ 戴上乳头夹 """
    STATUS_CLIT_LOVE_EGG = 483
    """ 阴蒂跳蛋 """
    STATUS_CLIT_CLAMP_ON = 484
    """ 戴上阴蒂夹 """
    STATUS_ELECTRIC_MESSAGE_STICK = 485
    """ 电动按摩棒 """
    STATUS_VIBRATOR_INSERTION = 486
    """ 震动棒 """
    STATUS_BIG_VIBRATOR_INSERTION = 487
    """ 加粗震动棒 """
    STATUS_HUGE_VIBRATOR_INSERTION = 488
    """ 巨型震动棒 """
    STATUS_VIBRATOR_INSERTION_ANAL = 489
    """ 肛门振动棒 """
    STATUS_BIG_VIBRATOR_INSERTION_ANAL = 490
    """ 加粗肛门震动棒 """
    STATUS_HUGE_VIBRATOR_INSERTION_ANAL = 491
    """ 巨型肛门震动棒 """
    STATUS_CLYSTER = 492
    """ 灌肠 """
    STATUS_ANAL_PLUG = 493
    """ 肛塞 """
    STATUS_ANAL_BEADS = 494
    """ 塞入肛门拉珠 """
    STATUS_CLYSTER_END = 495
    """ 拔出肛塞 """
    STATUS_NIPPLE_CLAMP_OFF = 496
    """ 取下乳头夹 """
    STATUS_CLIT_CLAMP_OFF = 497
    """ 取下阴蒂夹 """
    STATUS_VIBRATOR_INSERTION_OFF = 498
    """ 拔出振动棒 """
    STATUS_VIBRATOR_INSERTION_ANAL_OFF = 499
    """ 拔出肛门振动棒 """
    STATUS_ANAL_BEADS_OFF = 500
    """ 拔出肛门拉珠 """
    STATUS_NORMAL_SEX = 501
    """ 正常位 """
    STATUS_BACK_SEX = 502
    """ 背后位 """
    STATUS_RIDING_SEX = 503
    """ 骑乘位 """
    STATUS_FACE_SEAT_SEX = 504
    """ 对面座位 """
    STATUS_BACK_SEAT_SEX = 505
    """ 背面座位 """
    STATUS_FACE_STAND_SEX = 506
    """ 对面立位 """
    STATUS_BACK_STAND_SEX = 507
    """ 背面立位 """
    STATUS_STIMULATE_G_POINT = 511
    """ 刺激G点 """
    STATUS_WOMB_OS_CARESS = 512
    """ 玩弄子宫口 """
    STATUS_WOMB_INSERTION = 513
    """ 插入子宫 """
    STATUS_NORMAL_ANAL_SEX = 521
    """ 正常位肛交 """
    STATUS_BACK_ANAL_SEX = 522
    """ 后背位肛交 """
    STATUS_RIDING_ANAL_SEX = 523
    """ 骑乘位肛交 """
    STATUS_FACE_SEAT_ANAL_SEX = 524
    """ 对面座位肛交 """
    STATUS_BACK_SEAT_ANAL_SEX = 525
    """ 背面座位肛交 """
    STATUS_FACE_STAND_ANAL_SEX = 526
    """ 对面立位肛交 """
    STATUS_BACK_STAND_ANAL_SEX = 527
    """ 背面立位肛交 """
    STATUS_STIMULATE_SIGMOID_COLON = 530
    """ 玩弄s状结肠 """
    STATUS_STIMULATE_VAGINA = 531
    """ 隔着刺激阴道 """
    STATUS_MILKING_MACHINE = 601
    """ 搾乳机 """
    STATUS_URINE_COLLECTOR = 602
    """ 采尿器 """
    STATUS_BONDAGE = 603
    """ 绳子 """
    STATUS_PATCH = 604
    """ 眼罩 """
    STATUS_WHIP = 605
    """ 鞭子 """
    STATUS_NEEDLE = 606
    """ 针 """
    STATUS_UNDRESS = 701
    """ 脱衣服 """


class Behavior:
    """行为id"""

    SHARE_BLANKLY = 0
    """ 发呆 """
    MOVE = 1
    """ 移动 """
    WAIT = 2
    """ 等待 """
    CHANGE_CLOTH = 3
    """ 换衣服 """
    CHAT = 101
    """ 聊天 """
    CHAT_FAILED = 102
    """ 谈话次数过多而失败 """
    STROKE = 103
    """ 身体接触 """
    MAKE_COFFEE = 104
    """ 泡咖啡 """
    MAKE_COFFEE_ADD = 105
    """ 泡咖啡（加料） """
    ASK_MAKE_COFFEE = 106
    """ 让对方泡咖啡 """
    MAKE_FOOD = 107
    """ 做饭 """
    EAT = 108
    """ 进食 """
    BUY_FOOD = 109
    """ 购买食物 """
    REST = 110
    """ 休息 """
    SLEEP = 111
    """ 睡觉 """
    TAKE_SHOWER = 112
    """ 淋浴 """
    FOLLOW = 115
    """ 让NPC跟随玩家 """
    END_FOLLOW = 116
    """ 让NPC停止跟随玩家 """
    APOLOGIZE = 117
    """ 道歉 """
    APOLOGIZE_FAILED = 118
    """ 道歉失败 """
    LISTEN_COMPLAINT = 119
    """ 听牢骚 """
    CONFESSION = 121
    """ 告白 """
    CONFESSION_FAILED = 122
    """ 告白失败 """
    GIVE_NECKLACE = 123
    """ 戴上项圈 """
    GIVE_NECKLACE_FAILED = 124
    """ 戴上项圈失败 """
    H = 125
    """ 进入H状态 """
    END_H = 126
    """ 结束H """
    DO_H_FAIL = 131
    """ 邀请H失败 """
    H_HP_0 = 132
    """ H时博士体力为零中断 """
    T_H_HP_0 = 133
    """ H时交互对象体力为零中断 """
    H_INTERRUPT = 134
    """ H时被人目击闯入中断 """
    PEE = 140
    """ 解手 """
    CLOTH_OFF = 141
    """ 脱掉全部衣服 """
    PUT_SHOWER_CLOTH = 142
    """ 换上浴帽和浴巾 """
    PUT_SLEEP_CLOTH = 143
    """ 换上睡衣和内衣 """
    WEAR_TO_LOCKER = 144
    """ 身上衣服脱到衣柜 """
    LOCKER_TO_WEAR = 145
    """ 衣柜衣服穿回身上 """
    SINGING = 151
    """ 唱歌 """
    PLAY_INSTRUMENT = 152
    """ 演奏乐器 """
    CHECK_LOCKER = 161
    """ 检查衣柜 """
    OFFICIAL_WORK = 201
    """ 处理公务 """
    BATTLE_COMMAND = 202
    """ 指挥作战 """
    LISTEN_MISSION = 203
    """ 听取委托 """
    APPOINTED_ASSISTANT = 204
    """ 指派助理 """
    TRAINING = 205
    """ 战斗训练 """
    EXERCISE = 206
    """ 锻炼身体 """
    CURE_PATIENT = 207
    """ 诊疗病人 """
    RECRUIT = 208
    """ 招募干员 """
    READ_BOOK = 210
    """ 读书 """
    TOUCH_HEAD = 301
    """ 摸头 """
    TOUCH_BREAST = 302
    """ 摸胸 """
    TOUCH_BUTTOCKS = 303
    """ 摸屁股 """
    TOUCH_EARS = 304
    """ 摸耳朵 """
    TOUCH_HORN = 305
    """ 摸角 """
    TOUCH_TAIL = 306
    """ 摸尾巴 """
    TOUCH_RING = 307
    """ 摸光环 """
    TOUCH_WING = 308
    """ 摸光翼 """
    TOUCH_TENTACLE = 309
    """ 摸触手 """
    TOUCH_CAR = 310
    """ 摸小车 """
    HAND_IN_HAND = 311
    """ 牵手 """
    EMBRACE = 312
    """ 拥抱 """
    KISS = 313
    """ 亲吻 """
    LAP_PILLOW = 314
    """ 膝枕 """
    RAISE_SKIRT = 315
    """ 掀起裙子 """
    ASK_FOR_PAN = 316
    """ 索要内裤 """
    ASK_FOR_SOCKS = 317
    """ 索要袜子 """
    TOUCH_CLITORIS = 331
    """ 阴蒂爱抚 """
    TOUCH_VAGINA = 332
    """ 手指插入（V） """
    TOUCH_ANUS = 333
    """ 手指插入（A） """
    SMELL_UNDERWEAR = 341
    """ 闻内衣 """
    SEE_H = 396
    """ 目睹玩家与其他角色H """
    KISS_FAIL = 397
    """ 亲吻失败 """
    HIGH_OBSCENITY_ANUS = 398
    """ 重度猥亵失败 """
    LOW_OBSCENITY_ANUS = 399
    """ 轻度猥亵失败 """
    MAKING_OUT = 401
    """ 身体爱抚 """
    KISS_H = 402
    """ 接吻 """
    BREAST_CARESS = 403
    """ 胸爱抚 """
    TWIDDLE_NIPPLES = 404
    """ 玩弄乳头 """
    BREAST_SUCKING = 405
    """ 舔吸乳头 """
    CLIT_CARESS = 406
    """ 阴蒂爱抚 """
    OPEN_LABIA = 407
    """ 掰开阴唇观察 """
    OPEN_ANUS = 408
    """ 掰开肛门观察 """
    CUNNILINGUS = 409
    """ 舔阴 """
    LICK_ANAL = 410
    """ 舔肛 """
    FINGER_INSERTION = 411
    """ 手指插入(V) """
    ANAL_CARESS = 412
    """ 手指插入(A) """
    MAKE_MASTUREBATE = 413
    """ 命令对方自慰 """
    MAKE_LICK_ANAL = 414
    """ 命令对方舔自己肛门 """
    DO_NOTHING = 415
    """ 什么也不做 """
    SEDECU = 416
    """ 诱惑对方 """
    HANDJOB = 420
    """ 手交 """
    BLOWJOB = 421
    """ 口交 """
    PAIZURI = 422
    """ 乳交 """
    FOOTJOB = 423
    """ 足交 """
    HAIRJOB = 424
    """ 发交 """
    AXILLAJOB = 425
    """ 腋交 """
    RUB_BUTTOCK = 426
    """ 素股 """
    HAND_BLOWJOB = 427
    """ 手交口交 """
    TITS_BLOWJOB = 428
    """ 乳交口交 """
    FOCUS_BLOWJOB = 429
    """ 真空口交 """
    DEEP_THROAT = 430
    """ 深喉插入 """
    SIXTY_NINE = 431
    """ 六九式 """
    LEGJOB = 432
    """ 腿交 """
    TAILJOB = 433
    """ 尾交 """
    FACE_RUB = 434
    """ 阴茎蹭脸 """
    HORN_RUB = 435
    """ 阴茎蹭角 """
    EARS_RUB = 436
    """ 阴茎蹭耳朵 """
    BODY_LUBRICANT = 451
    """ 润滑液 """
    BIRTH_CONTROL_PILLS_BEFORE = 452
    """ 事前避孕药 """
    BIRTH_CONTROL_PILLS_AFTER = 453
    """ 事后避孕药 """
    PHILTER = 454
    """ 媚药 """
    ENEMAS = 455
    """ 灌肠液 """
    DIURETICS_ONCE = 456
    """ 一次性利尿剂 """
    DIURETICS_PERSISTENT = 457
    """ 持续性利尿剂 """
    SLEEPING_PILLS = 458
    """ 睡眠药 """
    SLEEPING_PILLS = 459
    """ 排卵促进药 """
    PUT_CONDOM = 471
    """ 戴上避孕套 """
    SAFE_CANDLES = 472
    """ 低温蜡烛 """
    URETHRAL_SWAB = 473
    """ 尿道棉棒 """
    NIPPLES_LOVE_EGG = 481
    """ 乳头跳蛋 """
    NIPPLE_CLAMP_ON = 482
    """ 戴上乳头夹 """
    CLIT_LOVE_EGG = 483
    """ 阴蒂跳蛋 """
    CLIT_CLAMP_ON = 484
    """ 戴上阴蒂夹 """
    ELECTRIC_MESSAGE_STICK = 485
    """ 电动按摩棒 """
    VIBRATOR_INSERTION = 486
    """ V插入震动棒 """
    BIG_VIBRATOR_INSERTION = 487
    """ 加粗震动棒 """
    HUGE_VIBRATOR_INSERTION = 488
    """ 巨型震动棒 """
    VIBRATOR_INSERTION_ANAL = 489
    """ A插入震动棒 """
    BIG_VIBRATOR_INSERTION_ANAL = 490
    """ 加粗肛门震动棒 """
    HUGE_VIBRATOR_INSERTION_ANAL = 491
    """ 巨型肛门震动棒 """
    CLYSTER = 492
    """ 灌肠 """
    ANAL_PLUG = 493
    """ 肛塞 """
    ANAL_BEADS = 494
    """ 塞入肛门拉珠 """
    CLYSTER_END = 495
    """ 拔出肛塞 """
    NIPPLE_CLAMP_OFF = 496
    """ 取下乳头夹 """
    CLIT_CLAMP_OFF = 497
    """ 取下阴蒂夹 """
    VIBRATOR_INSERTION_OFF = 498
    """ 拔出震动棒 """
    VIBRATOR_INSERTION_ANAL_OFF = 499
    """ 拔出肛门震动棒 """
    ANAL_BEADS_OFF = 500
    """ 拔出肛门拉珠 """
    NORMAL_SEX = 501
    """ 正常位 """
    BACK_SEX = 502
    """ 背后位 """
    RIDING_SEX = 503
    """ 骑乘位 """
    FACE_SEAT_SEX = 504
    """ 对面座位 """
    BACK_SEAT_SEX = 505
    """ 背面座位 """
    FACE_STAND_SEX = 506
    """ 对面立位 """
    BACK_STAND_SEX = 507
    """ 背面立位 """
    STIMULATE_G_POINT = 511
    """ 刺激G点 """
    WOMB_OS_CARESS = 512
    """ 玩弄子宫口 """
    WOMB_INSERTION = 513
    """ 插入子宫 """
    NORMAL_ANAL_SEX = 521
    """ 正常位肛交 """
    BACK_ANAL_SEX = 522
    """ 后背位肛交 """
    RIDING_ANAL_SEX = 523
    """ 骑乘位肛交 """
    FACE_SEAT_ANAL_SEX = 524
    """ 对面座位肛交 """
    BACK_SEAT_ANAL_SEX = 525
    """ 背面座位肛交 """
    FACE_STAND_ANAL_SEX = 526
    """ 对面立位肛交 """
    BACK_STAND_ANAL_SEX = 527
    """ 背面立位肛交 """
    STIMULATE_SIGMOID_COLON = 530
    """ 玩弄s状结肠 """
    STIMULATE_VAGINA = 531
    """ 隔着刺激阴道 """

    MILKING_MACHINE = 601
    """ 搾乳机 """
    URINE_COLLECTOR = 602
    """ 采尿器 """
    BONDAGE = 603
    """ 绳子 """
    PATCH = 604
    """ 眼罩 """
    WHIP = 605
    """ 鞭子 """
    NEEDLE = 606
    """ 针 """

    UNDRESS = 701
    """ 脱衣服 """


class StateMachine:
    """状态机id"""

    WAIT_5_MIN = 0
    """ 原地待机5分钟 """
    WAIT_10_MIN = 1
    """ 原地待机10分钟 """
    WAIT_30_MIN = 2
    """ 原地待机30分钟，并取消跟随状态 """
    FOLLOW = 6
    """ 跟随玩家 """
    MOVE_TO_RAND_SCENE = 10
    """ 移动至随机场景 """
    MOVE_TO_DORMITORY = 11
    """ 移动至所属宿舍 """
    MOVE_TO_TOILET = 12
    """ 去洗手间 """
    MOVE_TO_DR_OFFICE = 13
    """ 移动至博士办公室 """
    MOVE_TO_MODERN_MUSIC_ROOM = 14
    """ 移动至现代音乐室 """
    MOVE_TO_PLAYER = 15
    """ 移动至玩家位置 """
    MOVE_TO_FOODSHOP = 16
    """ 移动至食物商店（取餐区） """
    MOVE_TO_DINING_HALL = 17
    """ 移动至食堂 """
    MOVE_TO_REST_ROOM = 18
    """ 移动至休息室 """
    MOVE_TO_CLASSIC_MUSIC_ROOM = 19
    """ 移动至夕照区音乐室 """
    MOVE_TO_TRAINING_ROOM = 21
    """ 根据职业自动移动至对应训练室 """
    MOVE_TO_CLINIC = 22
    """ 随机移动到门诊室（含急诊室）（优先去当前没有人的） """
    MOVE_TO_HR_OFFICE = 23
    """ 移动到人事部办公室 """
    MOVE_TO_LIBRARY_OFFICE = 24
    """ 移动到图书馆办公室 """
    MOVE_TO_LIBRARY = 25
    """ 移动到图书馆 """
    MOVE_TO_BATHZONE_LOCKER_ROOM = 31
    """ 移动至大浴场的更衣室 """
    MOVE_TO_BATH_ROOM = 33
    """ 移动至淋浴室 """

    SEE_H_AND_MOVE_TO_DORMITORY = 40
    """ 目睹玩家和其他角色H，然后逃回自己宿舍 """
    BUY_RAND_FOOD_AT_FOODSHOP = 41
    """ 在取餐区购买随机食物 """
    EAT_BAG_RAND_FOOD = 42
    """ 食用背包内随机食物 """
    REST = 43
    """ 休息一会儿 """
    SLEEP = 44
    """ 睡觉 """
    SINGING = 45
    """ 唱歌 """
    PLAY_INSTRUMENT = 46
    """ 演奏乐器 """
    PEE = 50
    """ 解手 """
    TAKE_SHOWER = 51
    """ 淋浴 """

    WEAR_TO_LOCKER = 71
    """ 当前身上衣服转移到衣柜里 """
    GET_SHOWER_CLOTH = 72
    """ 换上浴帽和浴巾 """

    CHAT_TO_DR = 100
    """ 和玩家聊天 """
    STROKE_TO_DR = 101
    """ 和玩家身体接触 """
    MAKE_COFFEE_TO_DR = 102
    """ 给玩家泡咖啡 """
    MAKE_COFFEE_ADD_TO_DR = 103
    """ 给玩家泡咖啡（加料） """

    CHAT_RAND_CHARACTER = 200
    """ 和场景里随机对象聊天 """
    STROKE_RAND_CHARACTER = 201
    """ 和场景里随机对象身体接触 """
    SINGING_RAND_CHARACTER = 202
    """ 唱歌给房间里随机角色听 """
    PLAY_INSTRUMENT_RAND_CHARACTER = 203
    """ 演奏乐器给房间里随机角色听 """

    WORK_CURE_PATIENT = 301
    """ 工作：诊疗病人 """
    WORK_RECRUIT = 302
    """ 工作：招募干员 """

    ENTERTAIN_READ = 401
    """ 娱乐：读书 """
    ENTERTAIN_TRAINING = 402
    """ 娱乐：训练 """


    # MOVE_TO_CLASS = 0
    # """ 移动到所属教室 """
    # MOVE_TO_RAND_CAFETERIA = 1
    # """ 移动到随机取餐区 """
    # MOVE_TO_RAND_RESTAURANT = 3
    # """ 移动至随机就餐区 """
    # WEAR_CLEAN_UNDERWEAR = 6
    # """ 穿干净的上衣 """
    # WEAR_CLEAN_UNDERPANTS = 7
    # """ 穿干净的内裤 """
    # WEAR_CLEAN_BRA = 8
    # """ 穿干净的胸罩 """
    # WEAR_CLEAN_PANTS = 9
    # """ 穿干净的裤子 """
    # WEAR_CLEAN_SKIRT = 10
    # """ 穿干净的短裙 """
    # WEAR_CLEAN_SHOES = 11
    # """ 穿干净的鞋子 """
    # WEAR_CLEAN_SOCKS = 12
    # """ 穿干净的袜子 """
    # PLAY_PIANO = 13
    # """ 弹钢琴 """
    # SINGING = 15
    # """ 唱歌 """
    # SING_RAND_CHARACTER = 16
    # """ 唱歌给场景里随机对象听 """
    # PLAY_PIANO_RAND_CHARACTER = 17
    # """ 弹奏钢琴给场景里随机对象听 """
    # TOUCH_HEAD_TO_BEYOND_FRIENDSHIP_TARGET_IN_SCENE = 18
    # """ 对场景中抱有超越友谊想法的随机对象摸头 """
    # EMBRACE_TO_BEYOND_FRIENDSHIP_TARGET_IN_SCENE = 23
    # """ 对场景中抱有超越友谊想法的随机对象拥抱 """
    # KISS_TO_LIKE_TARGET_IN_SCENE = 24
    # """ 和场景中自己喜欢的随机对象接吻 """
    # MOVE_TO_LIKE_TARGET_SCENE = 25
    # """ 移动至随机某个自己喜欢的人所在场景 """
    # HAND_IN_HAND_TO_LIKE_TARGET_IN_SCENE = 26
    # """ 牵住场景中自己喜欢的随机对象的手 """
    # KISS_TO_NO_FIRST_KISS_TARGET_IN_SCENE = 27
    # """ 和场景中自己喜欢的还是初吻的随机对象接吻 """
    # MOVE_TO_NO_FIRST_KISS_LIKE_TARGET_SCENE = 28
    # """ 移动至喜欢的还是初吻的人所在的场景 """
    # DRINK_RAND_DRINKS = 29
    # """ 饮用背包内随机饮料 """
    # BUY_RAND_DRINKS_AT_CAFETERIA = 30
    # """ 在取餐区购买随机饮料 """
    # ATTEND_CLASS = 31
    # """ 在教室上课 """
    # TEACH_A_LESSON = 32
    # """ 在教室教课 """
    # MOVE_TO_GROVE = 33
    # """ 移动至加工站入口场景 """
    # MOVE_TO_ITEM_SHOP = 34
    # """ 移动至训练场入口场景 """
    # BUY_GUITAR = 35
    # """ 购买吉他 """
    # PLAY_GUITAR = 36
    # """ 弹吉他 """
    # SELF_STUDY = 37
    # """ 自习 """


class Panel:
    """面板id"""

    TITLE = 0
    """ 标题面板 """
    CREATOR_CHARACTER = 1
    """ 创建角色面板 """
    IN_SCENE = 2
    """ 场景互动面板 """
    SEE_MAP = 3
    """ 查看地图面板 """
    FOOD_SHOP = 4
    """ 食物商店面板 """
    FOOD_BAG = 5
    """ 食物背包面板 """
    ITEM_SHOP = 6
    """ 道具商店面板 """
    MAKE_FOOD = 7
    """ 做饭面板 """
    FIND_CALL = 8
    """ 查询与召集面板 """
    EJACULATION = 9
    """ 射精面板 """
    DIRTY = 10
    """ 脏污面板 """
    ITEM = 11
    """ 道具面板 """
    ASSISTANT = 12
    """ 助理面板 """
    COLLECTION = 13
    """ 收藏品面板 """
    UNDRESS = 14
    """ 脱衣服面板 """
    BUILDING = 15
    """ 基建面板 """
    DEPARTMENT = 16
    """ 部门运作情况面板 """
    INSTRUCT_FILTER = 17
    """ 指令过滤面板 """
    EVENT_OPTION = 18
    """ 事件选项面板 """
    CHECK_LOCKER = 19
    """ 检查衣柜面板 """
    BORROW_BOOK = 20
    """ 借阅书籍面板 """
    MANAGE_LIBRARY = 21
    """ 图书馆管理面板 """
    DEBUG_ADJUST = 22
    """ DEBUG面板 """


class SecondBehavior:
    """二段结算行为函数"""

    N_orgasm_small = 1000
    """ 结算N小绝顶 """
    N_orgasm_normal = 1001
    """ 结算N普绝顶 """
    N_orgasm_strong = 1002
    """ 结算N强绝顶 """
    B_orgasm_small = 1003
    """ 结算B小绝顶 """
    B_orgasm_normal = 1004
    """ 结算B普绝顶 """
    B_orgasm_strong = 1005
    """ 结算B强绝顶 """
    C_orgasm_small = 1006
    """ 结算C小绝顶 """
    C_orgasm_normal = 1007
    """ 结算C普绝顶 """
    C_orgasm_strong = 1008
    """ 结算C强绝顶 """
    P_orgasm_small = 1009
    """ 结算射精 """
    P_orgasm_normal = 1010
    """ 结算大量射精 """
    P_orgasm_strong = 1011
    """ 结算超大量射精 """
    V_orgasm_small = 1012
    """ 结算V小绝顶 """
    V_orgasm_normal = 1013
    """ 结算V普绝顶 """
    V_orgasm_strong = 1014
    """ 结算V强绝顶 """
    A_orgasm_small = 1015
    """ 结算A小绝顶 """
    A_orgasm_normal = 1016
    """ 结算A普绝顶 """
    A_orgasm_strong = 1017
    """ 结算A强绝顶 """
    U_orgasm_small = 1018
    """ 结算U小绝顶 """
    U_orgasm_normal = 1019
    """ 结算U普绝顶 """
    U_orgasm_strong = 1020
    """ 结算U强绝顶 """
    W_orgasm_small = 1021
    """ 结算W小绝顶 """
    W_orgasm_normal = 1022
    """ 结算W普绝顶 """
    W_orgasm_strong = 1023
    """ 结算W强绝顶 """
    HAPPY_MARK_1 = 1030
    """ 结算快乐刻印1 """
    HAPPY_MARK_2 = 1031
    """ 结算快乐刻印2 """
    HAPPY_MARK_3 = 1032
    """ 结算快乐刻印3 """
    YIELD_MARK_1 = 1033
    """ 结算屈服刻印1 """
    YIELD_MARK_2 = 1034
    """ 结算屈服刻印2 """
    YIELD_MARK_3 = 1035
    """ 结算屈服刻印3 """
    PAIN_MARK_1 = 1036
    """ 结算苦痛刻印1 """
    PAIN_MARK_2 = 1037
    """ 结算苦痛刻印2 """
    PAIN_MARK_3 = 1038
    """ 结算苦痛刻印3 """
    TIME_MARK_1 = 1039
    """ 结算时姦刻印1 """
    TIME_MARK_2 = 1040
    """ 结算时姦刻印2 """
    TIME_MARK_3 = 1041
    """ 结算时姦刻印3 """
    TERROR_MARK_1 = 1042
    """ 结算恐怖刻印1 """
    TERROR_MARK_2 = 1043
    """ 结算恐怖刻印2 """
    TERROR_MARK_3 = 1044
    """ 结算恐怖刻印3 """
    HATE_MARK_1 = 1045
    """ 结算反发刻印1 """
    HATE_MARK_2 = 1046
    """ 结算反发刻印2 """
    HATE_MARK_3 = 1047
    """ 结算反发刻印3 """
    FIRST_KISS = 1050
    """ 结算初吻 """
    FIRST_SEX = 1051
    """ 结算处女 """
    FIRST_A_SEX = 1052
    """ 结算A处女 """

    NIPPLE_CLAMP = 1100
    """ 结算乳头夹 """
    CLIT_CLAMP = 1101
    """ 结算阴蒂夹 """
    VIBRATOR_INSERTION = 1102
    """ 结算震动棒 """
    VIBRATOR_INSERTION_ANAL = 1103
    """ 结算肛门振动棒 """
    MILKING_MACHINE = 1104
    """ 结算搾乳机 """
    URINE_COLLECTOR = 1105
    """ 结算采尿器 """
    PATCH = 1106
    """ 结算眼罩 """
    ANAL_BEADS = 1107
    """ 结算肛门拉珠 """
    DIURETICS = 1108
    """ 结算利尿剂 """
    SLEEPING_PILLS = 1109
    """ 结算睡眠药 """

    PENIS_IN_HAIR = 1201
    """ 结算发交中 """
    PENIS_IN_FACE = 1202
    """ 结算阴茎蹭脸中 """
    PENIS_IN_MOUSE = 1203
    """ 结算口交中 """
    PENIS_IN_BREAST = 1204
    """ 结算乳交中 """
    PENIS_IN_AXILLA = 1205
    """ 结算腋交中 """
    PENIS_IN_HAND = 1206
    """ 结算手交中 """
    PENIS_IN_VAGINA = 1207
    """ 结算V插入中 """
    PENIS_IN_WOMB = 1208
    """ 结算W插入中 """
    PENIS_IN_ANAL = 1209
    """ 结算A插入中 """
    PENIS_IN_URETHRAL = 1210
    """ 结算U插入中 """
    PENIS_IN_LEG = 1211
    """ 结算腿交中 """
    PENIS_IN_FOOT = 1212
    """ 结算足交中 """
    PENIS_IN_TAIL = 1213
    """ 结算尾交中 """
    PENIS_IN_HORN = 1214
    """ 结算阴茎蹭角中 """
    PENIS_IN_EARS = 1215
    """ 结算阴茎蹭耳朵中 """
    PENIS_IN_RUB_BUTTOCK = 1216
    """ 结算素股中 """


class SecondEffect:
    """二段结算效果函数"""



    ADD_1_NClimax_EXPERIENCE = 210
    """ 增加1N绝顶经验 """
    ADD_1_BClimax_EXPERIENCE = 211
    """ 增加1B绝顶经验 """
    ADD_1_CClimax_EXPERIENCE = 212
    """ 增加1C绝顶经验 """
    # ADD_1_PClimax_EXPERIENCE = 213
    # """ 增加1P绝顶经验 """
    ADD_1_VClimax_EXPERIENCE = 214
    """ 增加1V绝顶经验 """
    ADD_1_AClimax_EXPERIENCE = 215
    """ 增加1A绝顶经验 """
    ADD_1_UClimax_EXPERIENCE = 216
    """ 增加1U绝顶经验 """
    ADD_1_WClimax_EXPERIENCE = 217
    """ 增加1W绝顶经验 """
    # ADD_1_Climax_EXPERIENCE = 220
    # """ 增加1绝顶经验 """
    ADD_1_Cumming_EXPERIENCE = 221
    """ 增加1射精经验 """
    ADD_1_Milking_EXPERIENCE = 222
    """ 增加1喷乳经验 """
    ADD_1_Peeing_EXPERIENCE = 223
    """ 增加1放尿经验 """
    TARGET_ADD_1_Cums_EXPERIENCE = 224
    """ 交互对象增加1精液经验 """
    TARGET_ADD_SMALL_LUBRICATION = 225
    """ 交互对象增加少量润滑 """
    TARGET_ADD_MIDDLE_LUBRICATION = 226
    """ 交互对象增加中量润滑 """
    TARGET_ADD_LARGE_LUBRICATION = 227
    """ 交互对象增加大量润滑 """
    ADD_SMALL_LUBRICATION = 228
    """ 增加少量润滑 """
    ADD_MIDDLE_LUBRICATION = 229
    """ 增加中量润滑 """
    ADD_LARGE_LUBRICATION = 230
    """ 增加大量润滑 """
    DOWN_SMALL_HIT_POINT = 231
    """ 减少少量体力 """
    DOWN_SMALL_MANA_POINT = 232
    """ 减少少量气力 """
    DOWN_MIDDLE_HIT_POINT = 233
    """ 减少中量体力 """
    DOWN_MIDDLE_MANA_POINT = 234
    """ 减少中量气力 """
    DOWN_LARGE_HIT_POINT = 235
    """ 减少大量体力 """
    DOWN_LARGE_MANA_POINT = 236
    """ 减少大量气力 """
    ADD_SMALL_N_FEEL = 237
    """ 增加少量Ｎ快（N感补正） """
    ADD_SMALL_B_FEEL = 238
    """ 增加少量Ｂ快（B感补正） """
    ADD_SMALL_C_FEEL = 239
    """ 增加少量Ｃ快（C感补正） """
    ADD_SMALL_P_FEEL = 240
    """ 增加少量射精值（P感补正） """
    ADD_SMALL_V_FEEL = 241
    """ 增加少量Ｖ快（V感补正） """
    ADD_SMALL_A_FEEL = 242
    """ 增加少量Ａ快（A感补正） """
    ADD_SMALL_U_FEEL = 243
    """ 增加少量Ｕ快（U感补正） """
    ADD_SMALL_W_FEEL = 244
    """ 增加少量Ｗ快（W感补正） """
    ADD_MIDDLE_N_FEEL = 245
    """ 增加中量Ｎ快（N感补正） """
    ADD_MIDDLE_B_FEEL = 246
    """ 增加中量Ｂ快（B感补正） """
    ADD_MIDDLE_C_FEEL = 247
    """ 增加中量Ｃ快（C感补正） """
    ADD_MIDDLE_P_FEEL = 248
    """ 增加中量Ｐ快（P感补正） """
    ADD_MIDDLE_V_FEEL = 249
    """ 增加中量Ｖ快（V感补正） """
    ADD_MIDDLE_A_FEEL = 250
    """ 增加中量Ａ快（A感补正） """
    ADD_MIDDLE_U_FEEL = 251
    """ 增加中量Ｕ快（U感补正） """
    ADD_MIDDLE_W_FEEL = 252
    """ 增加中量Ｗ快（W感补正） """
    ADD_LARGE_N_FEEL = 253
    """ 增加大量Ｎ快（N感补正） """
    ADD_LARGE_B_FEEL = 254
    """ 增加大量Ｂ快（B感补正） """
    ADD_LARGE_C_FEEL = 255
    """ 增加大量Ｃ快（C感补正） """
    ADD_LARGE_P_FEEL = 256
    """ 增加大量Ｐ快（P感补正） """
    ADD_LARGE_V_FEEL = 257
    """ 增加大量Ｖ快（V感补正） """
    ADD_LARGE_A_FEEL = 258
    """ 增加大量Ａ快（A感补正） """
    ADD_LARGE_U_FEEL = 259
    """ 增加大量Ｕ快（U感补正） """
    ADD_LARGE_W_FEEL = 260
    """ 增加大量Ｗ快（W感补正） """
    ADD_SMALL_LUBRICATION_PLUS = 261
    """ 增加少量润滑（欲望补正） """
    ADD_SMALL_LEARN = 262
    """ 增加少量习得（技巧补正） """
    ADD_SMALL_RESPECT = 263
    """ 增加少量恭顺（顺从补正） """
    ADD_SMALL_FRIENDLY = 264
    """ 增加少量好意（亲密补正） """
    ADD_SMALL_DESIRE = 265
    """ 增加少量欲情（欲望补正） """
    ADD_SMALL_HAPPY = 266
    """ 增加少量快乐（快乐刻印补正） """
    ADD_SMALL_LEAD = 267
    """ 增加少量先导（施虐补正） """
    ADD_SMALL_SUBMIT = 268
    """ 增加少量屈服（屈服刻印补正） """
    ADD_SMALL_SHY = 269
    """ 增加少量羞耻（露出补正） """
    ADD_SMALL_PAIN = 270
    """ 增加少量苦痛（苦痛刻印补正） """
    ADD_SMALL_TERROR = 271
    """ 增加少量恐怖（恐怖刻印补正） """
    ADD_SMALL_DEPRESSION = 272
    """ 增加少量抑郁 """
    ADD_SMALL_DISGUST = 273
    """ 增加少量反感（反发刻印补正） """
    ADD_MIDDLE_LUBRICATION_PLUS = 274
    """ 增加中量润滑（欲望补正） """
    ADD_MIDDLE_LEARN = 275
    """ 增加中量习得（技巧补正） """
    ADD_MIDDLE_RESPECT = 276
    """ 增加中量恭顺（顺从补正） """
    ADD_MIDDLE_FRIENDLY = 277
    """ 增加中量好意（亲密补正） """
    ADD_MIDDLE_DESIRE = 278
    """ 增加中量欲情（欲望补正） """
    ADD_MIDDLE_HAPPY = 279
    """ 增加中量快乐（快乐刻印补正） """
    ADD_MIDDLE_LEAD = 280
    """ 增加中量先导（施虐补正） """
    ADD_MIDDLE_SUBMIT = 281
    """ 增加中量屈服（屈服刻印补正） """
    ADD_MIDDLE_SHY = 282
    """ 增加中量羞耻（露出补正） """
    ADD_MIDDLE_PAIN = 283
    """ 增加中量苦痛（苦痛刻印补正） """
    ADD_MIDDLE_TERROR = 284
    """ 增加中量恐怖（恐怖刻印补正） """
    ADD_MIDDLE_DEPRESSION = 285
    """ 增加中量抑郁 """
    ADD_MIDDLE_DISGUST = 286
    """ 增加中量反感（反发刻印补正） """
    ADD_LARGE_LUBRICATION_PLUS = 287
    """ 增加大量润滑（欲望补正） """
    ADD_LARGE_LEARN = 288
    """ 增加大量习得（技巧补正） """
    ADD_LARGE_RESPECT = 289
    """ 增加大量恭顺（顺从补正） """
    ADD_LARGE_FRIENDLY = 290
    """ 增加大量好意（亲密补正） """
    ADD_LARGE_DESIRE = 291
    """ 增加大量欲情（欲望补正） """
    ADD_LARGE_HAPPY = 292
    """ 增加大量快乐（快乐刻印补正） """
    ADD_LARGE_LEAD = 293
    """ 增加大量先导（施虐补正） """
    ADD_LARGE_SUBMIT = 294
    """ 增加大量屈服（屈服刻印补正） """
    ADD_LARGE_SHY = 295
    """ 增加大量羞耻（露出补正） """
    ADD_LARGE_PAIN = 296
    """ 增加大量苦痛（苦痛刻印补正） """
    ADD_LARGE_TERROR = 297
    """ 增加大量恐怖（恐怖刻印补正） """
    ADD_LARGE_DEPRESSION = 298
    """ 增加大量抑郁 """
    ADD_LARGE_DISGUST = 299
    """ 增加大量反感（反发刻印补正） """
    ADD_LARGE_PAIN_FIRST_SEX = 400
    """ 增加巨量苦痛（破处修正） """
    ADD_LARGE_PAIN_FIRST_A_SEX = 401
    """ 增加巨量苦痛（A破处修正） """
    ADD_URINATE = 402
    """ 增加尿意（持续性利尿剂） """

    PENIS_IN_T_RESET = 501
    """ 当前阴茎位置为交互对象_归零 """



#旧结算存档#
    # ADD_SOCIAL_FAVORABILITY = 7
    # """ 增加社交关系好感 """
    # ADD_INTIMACY_FAVORABILITY = 8
    # """ 增加亲密行为好感(关系不足2则增加反感) """
    # ADD_INTIMATE_FAVORABILITY = 9
    # """ 增加私密行为好感(关系不足3则增加反感) """


class InstructType:
    """指令类型"""

    SYSTEM = 0
    """ 系统 """
    DAILY = 1
    """ 日常 """
    PLAY = 2
    """ 娱乐 """
    WORK = 3
    """ 工作 """
    OBSCENITY = 4
    """ 猥亵 """
    SEX = 5
    """ 性爱 """


class Instruct:
    """指令id"""
    #日常#
    WAIT = 0
    """ 等待五分钟 """
    WAIT_1_HOUR = 0
    """ 等待一个小时 """
    WAIT_6_HOUR = 0
    """ 等待六个小时 """
    CHAT = 0
    """ 聊天 """
    STROKE = 0
    """ 身体接触 """
    MAKE_COFFEE = 0
    """ 泡咖啡 """
    MAKE_COFFEE_ADD = 0
    """ 泡咖啡（加料） """
    ASK_MAKE_COFFEE = 0
    """ 让对方泡咖啡 """
    MAKE_FOOD = 0
    """ 做饭 """
    EAT = 0
    """ 进食 """
    REST = 0
    """ 休息 """
    SLEEP = 0
    """ 睡觉 """
    TAKE_SHOWER = 0
    """ 淋浴 """
    BUY_ITEM = 0
    """ 购买道具 """
    BUY_FOOD = 0
    """ 购买食物 """
    FOLLOW = 0
    """ 邀请同行 """
    END_FOLLOW = 0
    """ 结束同行 """
    APOLOGIZE = 0
    """ 道歉 """
    LISTEN_COMPLAINT = 0
    """ 听牢骚 """
    PRAY = 0
    """ 祈愿 """
    CHECK_LOCKER = 0
    """ 检查衣柜 """
    COLLCET_PANTY = 0
    """ 收起内裤 """
    ASK_DATE = 0
    """ 邀请约会 """
    DRINK_ALCOHOL = 0
    """ 劝酒 """
    PEE = 0
    """ 解手 """
    COLLECT = 0
    """ 摆放藏品 """

    #娱乐#
    SINGING = 0
    """ 唱歌 """
    PLAY_INSTRUMENT = 0
    """ 演奏乐器 """


    #工作#
    BUILDING = 0
    """ 基建系统 """
    OFFICIAL_WORK = 0
    """ 处理公务 """
    BATTLE_COMMAND = 0
    """ 指挥作战 """
    LISTEN_MISSION = 0
    """ 听取委托 """
    APPOINTED_ASSISTANT = 0
    """ 指派助理 """
    TRAINING = 0
    """ 战斗训练 """
    EXERCISE = 0
    """ 锻炼身体 """
    CURE_PATIENT = 0
    """ 诊疗病人 """
    RECRUIT = 0
    """ 招募干员 """
    CONFIM_RECRUIT = 0
    """ 确认已招募的干员 """
    BORROW_BOOK = 0
    """ 借阅书籍 """
    READ_BOOK = 0
    """ 读书 """
    MANAGE_LIBRARY = 0
    """ 管理图书馆 """
    SEE_COLLECTION = 0
    """ 查看收藏品 """
    FIND_AND_CALL_NPC = 0
    """ 查找与召集干员 """
    SEE_DEPARTMENT = 0
    """ 查看部门运作情况 """

    #猥亵#
    TOUCH_HEAD = 0
    """ 摸头 """
    TOUCH_BREAST = 0
    """ 摸胸 """
    TOUCH_BUTTOCKS = 0
    """ 摸屁股 """
    TOUCH_EARS = 0
    """ 摸耳朵 """
    TOUCH_HORN = 0
    """ 摸角 """
    TOUCH_TAIL = 0
    """ 摸尾巴 """
    TOUCH_RING = 0
    """ 摸光环 """
    TOUCH_WING = 0
    """ 摸光翼 """
    TOUCH_TENTACLE = 0
    """ 摸触手 """
    TOUCH_CAR = 0
    """ 摸小车 """
    HAND_IN_HAND = 0
    """ 牵手 """
    EMBRACE = 0
    """ 拥抱 """
    KISS = 0
    """ 亲吻 """
    LAP_PILLOW = 0
    """ 膝枕 """
    RAISE_SKIRT = 0
    """ 掀起裙子 """
    ASK_FOR_PAN = 0
    """ 索要内裤 """
    ASK_FOR_SOCKS = 0
    """ 索要袜子 """
    TOUCH_CLITORIS = 0
    """ 阴蒂爱抚 """
    TOUCH_VAGINA = 0
    """ 手指插入（V） """
    TOUCH_ANUS = 0
    """ 手指插入（A） """
    DO_H = 0
    """ 邀请H """
    CONFESSION = 0
    """ 告白 """
    GIVE_NECKLACE = 0
    """ 戴上项圈 """

    #性爱#
    END_H = 0
    """ H结束 """
    MAKING_OUT = 0
    """ 身体爱抚 """
    KISS_H = 0
    """ 接吻 """
    BREAST_CARESS = 0
    """ 胸爱抚 """
    TWIDDLE_NIPPLES = 0
    """ 玩弄乳头 """
    BREAST_SUCKING = 0
    """ 舔吸乳头 """
    CLIT_CARESS = 0
    """ 阴蒂爱抚 """
    OPEN_LABIA = 0
    """ 掰开阴唇观察 """
    OPEN_ANUS = 0
    """ 掰开肛门观察 """
    CUNNILINGUS = 0
    """ 舔阴 """
    LICK_ANAL = 0
    """ 舔肛 """
    FINGER_INSERTION = 0
    """ 手指插入(V) """
    ANAL_CARESS = 0
    """ 手指插入(A) """
    MAKE_MASTUREBATE = 0
    """ 命令对方自慰 """
    MAKE_LICK_ANAL = 0
    """ 命令对方舔自己肛门 """
    DO_NOTHING = 0
    """ 什么也不做 """
    SEDECU = 0
    """ 诱惑 """
    HANDJOB = 0
    """ 手交 """
    BLOWJOB = 0
    """ 口交 """
    PAIZURI = 0
    """ 乳交 """
    FOOTJOB = 0
    """ 足交 """
    HAIRJOB = 0
    """ 发交 """
    AXILLAJOB = 0
    """ 腋交 """
    RUB_BUTTOCK = 0
    """ 素股 """
    HAND_BLOWJOB = 0
    """ 手交口交 """
    TITS_BLOWJOB = 0
    """ 乳交口交 """
    FOCUS_BLOWJOB = 0
    """ 真空口交 """
    DEEP_THROAT = 0
    """ 深喉插入 """
    SIXTY_NINE = 0
    """ 六九式 """
    LEGJOB = 0
    """ 腿交 """
    TAILJOB = 0
    """ 尾交 """
    FACE_RUB = 0
    """ 阴茎蹭脸 """
    HORN_RUB = 0
    """ 阴茎蹭角 """
    EARS_RUB = 0
    """ 阴茎蹭耳朵 """
    BODY_LUBRICANT = 0
    """ 润滑液 """
    BIRTH_CONTROL_PILLS = 0
    """ 避孕药 """
    PHILTER = 0
    """ 媚药 """
    ENEMAS = 0
    """ 灌肠液 """
    DIURETICS_ONCE = 0
    """ 一次性利尿剂 """
    DIURETICS_PERSISTENT = 0
    """ 持续性利尿剂 """
    SLEEPING_PILLS = 0
    """ 睡眠药 """
    CLOMID = 0
    """ 排卵促进药 """
    PUT_CONDOM = 0
    """ 戴上避孕套 """
    SAFE_CANDLES = 0
    """ 滴蜡 """
    URETHRAL_SWAB = 0
    """ 尿道棉棒 """
    NIPPLES_LOVE_EGG = 0
    """ 乳头跳蛋 """
    NIPPLE_CLAMP_ON = 0
    """ 戴上乳头夹 """
    CLIT_LOVE_EGG = 0
    """ 阴蒂跳蛋 """
    CLIT_CLAMP_ON = 0
    """ 戴上阴蒂夹 """
    ELECTRIC_MESSAGE_STICK = 0
    """ 电动按摩棒 """
    VIBRATOR_INSERTION = 0
    """ 插入震动棒 """
    BIG_VIBRATOR_INSERTION = 0
    """ 加粗震动棒 """
    HUGE_VIBRATOR_INSERTION = 0
    """ 巨型震动棒 """
    VIBRATOR_INSERTION_ANAL = 0
    """ 肛门插入振动棒 """
    BIG_VIBRATOR_INSERTION_ANAL = 0
    """ 加粗肛门震动棒 """
    HUGE_VIBRATOR_INSERTION_ANAL = 0
    """ 巨型肛门震动棒 """
    CLYSTER = 0
    """ 灌肠 """
    ANAL_PLUG = 0
    """ 肛塞 """
    ANAL_BEADS = 0
    """ 塞入肛门拉珠 """
    CLYSTER_END = 0
    """ 拔出肛塞 """
    NIPPLE_CLAMP_OFF = 0
    """ 取下乳头夹 """
    CLIT_CLAMP_OFF = 0
    """ 取下阴蒂夹 """
    VIBRATOR_INSERTION_OFF = 0
    """ 拔出振动棒 """
    VIBRATOR_INSERTION_ANAL_OFF = 0
    """ 拔出肛门振动棒 """
    ANAL_BEADS_OFF = 0
    """ 拔出肛门拉珠 """
    MILKING_MACHINE = 0
    """ 搾乳机 """
    URINE_COLLECTOR = 0
    """ 采尿器 """
    BONDAGE = 0
    """ 绳子 """
    PATCH = 0
    """ 眼罩 """
    WHIP = 0
    """ 鞭子 """
    NEEDLE = 0
    """ 针 """
    NORMAL_SEX = 0
    """ 正常位 """
    BACK_SEX = 0
    """ 背后位 """
    RIDING_SEX = 0
    """ 骑乘位 """
    FACE_SEAT_SEX = 0
    """ 对面座位 """
    BACK_SEAT_SEX = 0
    """ 背面座位 """
    FACE_STAND_SEX = 0
    """ 对面立位 """
    BACK_STAND_SEX = 0
    """ 背面立位 """
    STIMULATE_G_POINT = 0
    """ 刺激G点 """
    WOMB_OS_CARESS = 0
    """ 玩弄子宫口 """
    WOMB_INSERTION = 0
    """ 插入子宫 """
    NORMAL_ANAL_SEX = 0
    """ 正常位肛交 """
    BACK_ANAL_SEX = 0
    """ 后背位肛交 """
    RIDING_ANAL_SEX = 0
    """ 骑乘位肛交 """
    FACE_SEAT_ANAL_SEX = 0
    """ 对面座位肛交 """
    BACK_SEAT_ANAL_SEX = 0
    """ 背面座位肛交 """
    FACE_STAND_ANAL_SEX = 0
    """ 对面立位肛交 """
    BACK_STAND_ANAL_SEX = 0
    """ 背面立位肛交 """
    STIMULATE_SIGMOID_COLON = 0
    """ 玩弄s状结肠 """
    STIMULATE_VAGINA = 0
    """ 隔着刺激阴道 """
    DOUBLE_PENETRATION = 0
    """ 二穴插入 """
    PISSING_PLAY = 0
    """ 放尿play """
    URETHRAL_INSERTION = 0
    """ 尿道插入 """
    BEAT_BREAST = 0
    """ 打胸部 """
    SPANKING = 0
    """ 打屁股 """
    SHAME_PLAY = 0
    """ 羞耻play """
    BUNDLED_PLAY = 0
    """ 拘束play """
    TAKE_SHOWER_H = 0
    """ 淋浴 """
    BUBBLE_BATH = 0
    """ 泡泡浴 """
    CHANGE_TOP_AND_BOTTOM = 0
    """ 交给对方 """
    GIVE_BLOWJOB = 0
    """ 给对方口交 """
    UNDRESS = 0
    """ 脱衣服 """
    #系统#
    MOVE = 0
    """ 移动 """
    SEE_ATTR = 0
    """ 查看属性 """
    ITEM = 0
    """ 道具 """
    SAVE = 0
    """ 读写存档 """
    ABL_UP = 0
    """ 属性升级 """
    OWNER_ABL_UP = 0
    """ 自身属性升级 """
    SEE_DIRTY = 0
    """ 查看污浊情况 """
    INSTRUCT_FILTER = 0
    """ 指令过滤 """
    DEBUG_MODE_ON = 0
    """ 开启debug模式 """
    DEBUG_MODE_OFF = 0
    """ 关闭debug模式 """
    DEBUG_ADJUST = 0
    """ debug数值调整 """


i = 0
for k in Instruct.__dict__:
    if isinstance(Instruct.__dict__[k], int):
        setattr(Instruct, k, i)
        i += 1


handle_premise_data: Dict[str, FunctionType] = {}
""" 前提处理数据 """
handle_instruct_data: Dict[int, FunctionType] = {}
""" 指令处理数据 """
handle_instruct_name_data: Dict[int, str] = {}
""" 指令对应文本 """
instruct_type_data: Dict[int, Set] = {}
""" 指令类型拥有的指令集合 """
instruct_premise_data: Dict[int, Set] = {}
""" 指令显示的所需前提集合 """
handle_state_machine_data: Dict[int, FunctionType] = {}
""" 角色状态机函数 """
family_region_list: Dict[int, str] = {}
""" 姓氏区间数据 """
boys_region_list: Dict[int, str] = {}
""" 男孩名字区间数据 """
girls_region_list: Dict[int, str] = {}
""" 女孩名字区间数据 """
family_region_int_list: List[int] = []
""" 姓氏权重区间数据 """
boys_region_int_list: List[int] = []
""" 男孩名字权重区间数据 """
girls_region_int_list: List[int] = []
""" 女孩名字权重区间数据 """
panel_data: Dict[int, FunctionType] = {}
"""
面板id对应的面板绘制函数集合
面板id:面板绘制函数对象
"""
place_data: Dict[str, List[str]] = {}
""" 按房间类型分类的场景列表 场景标签:场景路径列表 """
cmd_map: Dict[int, FunctionType] = {}
""" cmd存储 """
settle_behavior_effect_data: Dict[int, FunctionType] = {}
""" 角色行为结算处理器 处理器id:处理器 """
settle_second_behavior_effect_data: Dict[int, FunctionType] = {}
""" 角色二段行为结算处理器 处理器id:处理器 """

instruct_en2cn = {"VIBRATOR_INSERTION" : "震动棒","VIBRATOR_INSERTION_ANAL" : "肛门震动棒","NORMAL_SEX" : "正常位","BACK_SEX" : "背后位","RIDING_SEX" : "骑乘位","FACE_SEAT_SEX" : "对面座位","BACK_SEAT_SEX" : "背面座位","FACE_STAND_SEX" : "对面立位","BACK_STAND_SEX" : "背面立位","NORMAL_ANAL_SEX" : "正常位肛交","BACK_ANAL_SEX" : "后背位肛交","RIDING_ANAL_SEX" : "骑乘位肛交","FACE_SEAT_ANAL_SEX" : "对面座位肛交","BACK_SEAT_ANAL_SEX" : "背面座位肛交","FACE_STAND_ANAL_SEX" : "对面立位肛交","BACK_STAND_ANAL_SEX" : "背面立位肛交"}


# 协力名单，不分先后 依吹脆香，反R，幻白，无色树，灵鸠伊凛