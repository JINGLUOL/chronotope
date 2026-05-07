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
    ''' 触发起跳 '''
    Jump = 'Jump'
    ''' 跳起 '''
    Fall = 'Fall'
    ''' 降落 '''
    Hard_Land = 'Hard Land'
    ''' 硬着陆 '''

    Stop_Somebody = 'Stop Somebody'
    ''' 阻止动作 '''
    Stop_Somebody_End = 'Stop Somebody End'
    ''' 阻止动作结束 '''

    Barb_Throw_Antic = 'Barb Throw Antic'
    Barb_Throw = 'Barb Throw'
    ''' 投出骨钉 '''
    Barb_Throw_Recover = 'Barb Throw Recover'

    Air_Dash_Effect = 'Air Dash Effect'
    ''' 爆气 '''

    Sphere_Attack = 'Sphere Attack'
    ''' 灵丝风暴 '''
    Sphere_Ball = 'Sphere Ball'
    ''' 灵丝风暴效果 '''
    pass


coherent_anim_map = {
    HornetAniStatus.Jump: HornetAniStatus.Fall,
}

before_anim_transition_map = {
    HornetAniStatus.Jump: HornetAniStatus.Jump_Antic,
    HornetAniStatus.Barb_Throw: HornetAniStatus.Barb_Throw_Antic,
}

after_anim_transition_map = {
    HornetAniStatus.Jump: HornetAniStatus.Hard_Land,
    HornetAniStatus.Fall: HornetAniStatus.Hard_Land,
    HornetAniStatus.Stop_Somebody: HornetAniStatus.Stop_Somebody_End,
    HornetAniStatus.Barb_Throw: HornetAniStatus.Barb_Throw_Recover,
    HornetAniStatus.Sphere_Attack: HornetAniStatus.Hard_Land,
}

effect_transition_map = {
    HornetAniStatus.Barb_Throw: HornetAniStatus.Air_Dash_Effect,
    HornetAniStatus.Sphere_Attack: HornetAniStatus.Sphere_Ball,
}

effect_loop_map = [
    HornetAniStatus.Sphere_Ball
]

turn_anim_transition_map = [
    HornetAniStatus.Idle,
    HornetAniStatus.Run,
]

wait_status = [
    HornetAniStatus.Idle,
]
