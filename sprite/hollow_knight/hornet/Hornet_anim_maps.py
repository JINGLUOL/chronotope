from dataclasses import dataclass


@dataclass
class HornetAniStatus:
    Idle = 'Idle'
    ''' 等待 '''

    Turn = 'Turn'
    ''' 转向 '''

    Run = 'Run'
    ''' 跑 '''

    Jump_Antic = 'Jump Antic'
    ''' 起跳前 '''
    Jump = 'Jump'
    ''' 跳起 '''
    Hard_Land = 'Hard Land'
    ''' 硬着陆 '''

    Stop_Somebody = 'Stop Somebody'
    ''' 阻止动作 '''
    Stop_Somebody_End = 'Stop Somebody End'
    ''' 阻止动作结束 '''

    pass


before_anim_transition_map = {
    HornetAniStatus.Jump: HornetAniStatus.Jump_Antic,
}

after_anim_transition_map = {
    HornetAniStatus.Jump: HornetAniStatus.Hard_Land,
}

transition_turn_anim_map = [
    HornetAniStatus.Idle,
    HornetAniStatus.Run,
]

wait_status = [
    HornetAniStatus.Idle,
]
