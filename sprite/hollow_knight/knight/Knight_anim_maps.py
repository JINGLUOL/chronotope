from dataclasses import dataclass


@dataclass
class KnightAniStatus:
    """ 小骑士行为状态集 """

    IDLE = 'Idle'
    ''' 闲置 '''
    IDLE_WIND = 'Idle Wind'

    WALK = 'Walk'
    ''' 走 '''

    Turn = 'Turn'
    ''' 转向 '''

    RUN = 'Run'
    ''' 跑 '''
    RUN_TO_IDLE = 'Run To Idle'

    LookUp = 'LookUp'
    ''' 向上看 '''
    LookUpEnd = 'LookUpEnd'

    LookDown = 'LookDown'
    '''向下看'''
    LookDownEnd = 'LookDownEnd'

    Airborne = 'Airborne'
    ''' 跳 '''

    Fall = 'Fall'
    ''' 坠落 '''

    Land = 'Land'
    ''' 着陆 '''
    HardLand = 'HardLand'

    Reach_Out = 'Reach Out'
    ''' 伸手 '''
    Reach_Out_Back = 'Reach Out Back'

    Shadow_Recharge = 'Shadow Recharge'
    ''' 阴影充能 '''
    pass


coherent_anim_map = {
    KnightAniStatus.Airborne: KnightAniStatus.Fall
}

before_anim_transition_map = {
}

after_anim_transition_map = {
    KnightAniStatus.Airborne: KnightAniStatus.Land,
    KnightAniStatus.Fall: KnightAniStatus.Land,

    KnightAniStatus.Reach_Out: KnightAniStatus.Reach_Out_Back,

    KnightAniStatus.LookUp: KnightAniStatus.LookUpEnd,
    KnightAniStatus.LookDown: KnightAniStatus.LookDownEnd,
}

turn_transition_anim_map = [
    KnightAniStatus.IDLE,
    KnightAniStatus.IDLE_WIND,
    KnightAniStatus.WALK,
    KnightAniStatus.RUN,
    KnightAniStatus.LookUp,
    KnightAniStatus.LookDown,
]

wait_status = [
    KnightAniStatus.IDLE,
    KnightAniStatus.IDLE_WIND,
    KnightAniStatus.LookUp,
    KnightAniStatus.LookDown,
]
''' 等待状态集 '''
