from .HornetSpriteAbs import HornetSpriteAbs


class HornetSprite(HornetSpriteAbs):

    def __init__(self):
        super().__init__('Hornet', 'Idle')
        pass

    def _sprite_call_handle(self):
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_k]:
        #     self.jump()
        #     if self.transition_ani: return
        #     if self.animation.in_loop:
        #         if keys[pygame.K_s]:
        #             self.down_move()
        #         else:
        #             self.up_move()
        #         if keys[pygame.K_a]:
        #             self._set_flip_x(False)
        #             self.run_move()
        #         elif keys[pygame.K_d]:
        #             self._set_flip_x(True)
        #             self.run_move()
        #     else:
        #         self.y -= 13
        # elif keys[pygame.K_a]:
        #     self.left_run()
        # elif keys[pygame.K_d]:
        #     self.right_run()
        # else:
        #     self.idle()
        #     pass
        pass

    def _sprite_follow_handle(self):
        pass

    pass
