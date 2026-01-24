from collections.abc import Callable

import pygame


class ContextMenu:

    def __init__(self):
        self.items = []
        self.visible = False
        self.rect = None
        self.font = pygame.font.Font(None, 24)

    def add_item(self, text: str, callback: Callable[[], None]):
        """添加菜单项"""
        self.items.append({
            'text': text,
            'callback': callback,
            'rect': None
        })

    def show(self, pos):
        """显示菜单"""
        self.visible = True
        # 这里可以计算菜单位置
        self.rect = pygame.Rect(pos[0], pos[1], 120, len(self.items) * 30)

    def hide(self):
        """隐藏菜单"""
        self.visible = False

    def draw(self, surface):
        """绘制菜单"""
        if not self.visible or not self.rect:
            return

        # 绘制背景
        pygame.draw.rect(surface, (60, 60, 70), self.rect, border_radius=3)
        pygame.draw.rect(surface, (40, 40, 50), self.rect, 2, border_radius=3)

        # 绘制菜单项
        mouse_pos = pygame.mouse.get_pos()
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + i * 30,
                self.rect.width,
                30
            )
            item['rect'] = item_rect

            # 悬停效果
            if item_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, (80, 80, 100), item_rect, border_radius=2)

            # 绘制文本
            text = self.font.render(item['text'], True, (220, 220, 220))
            text_rect = text.get_rect(center=item_rect.center)
            surface.blit(text, text_rect)

    def handle_click(self, pos):
        """处理菜单点击"""
        if not self.visible:
            return False

        for item in self.items:
            if item['rect'] and item['rect'].collidepoint(pos):
                item['callback']()
                self.hide()
                return True
        return False
