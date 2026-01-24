from dataclasses import dataclass


@dataclass
class KnightAniStatus:
    # 闲置
    IDLE = 'Idle'
    IDLE_WIND = 'Idle Wind'

    # 走
    WALK = 'Walk'

    # 转向
    Turn = 'Turn'

    # 跑
    RUN = 'Run'
    RUN_TO_IDLE = 'Run To Idle'

    # 向上看
    LookUp = 'LookUp'
    LookUpEnd = 'LookUpEnd'

    # 向下看
    LookDown = 'LookDown'
    LookDownEnd = 'LookDownEnd'

    # 飞
    Scream = 'Scream'
    Scream_End = 'Scream End'

    # 坠
    SD_Charge_Ground = 'SD Charge Ground'
    SD_Charge_Ground_End = 'SD Charge Ground End'
    pass


transition_anim_map = {
    KnightAniStatus.LookUp: KnightAniStatus.LookUpEnd,
    KnightAniStatus.LookDown: KnightAniStatus.LookDownEnd,
    KnightAniStatus.Scream: KnightAniStatus.Scream_End,
    KnightAniStatus.SD_Charge_Ground: KnightAniStatus.SD_Charge_Ground_End,
}


turn_transition_anim_map = [
    KnightAniStatus.IDLE,
    KnightAniStatus.IDLE_WIND,
    KnightAniStatus.WALK,
    KnightAniStatus.LookUp,
    KnightAniStatus.LookDown,
]


wait_status = [
    KnightAniStatus.IDLE,
    KnightAniStatus.IDLE_WIND,
    KnightAniStatus.LookUp,
    KnightAniStatus.LookDown,
]
''' 等待状态集合 '''
