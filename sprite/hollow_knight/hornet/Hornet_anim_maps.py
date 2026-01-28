from dataclasses import dataclass


@dataclass
class HornetAniStatus:

    Idle = 'Idle'

    Turn = 'Turn'

    Run = 'Run'

    Jump_Antic = 'Jump Antic'
    Jump = 'Jump'
    Hard_Land='Hard Land'

    pass

transition_before_anim_map = {
    HornetAniStatus.Jump: HornetAniStatus.Jump_Antic,
}

transition_after_anim_map = {
    HornetAniStatus.Jump: HornetAniStatus.Hard_Land,
}

transition_turn_anim_map = [
    HornetAniStatus.Idle,
    HornetAniStatus.Run,
]

wait_status = [
    HornetAniStatus.Idle,
]
