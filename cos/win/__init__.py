import ctypes
import sys

import psutil
import win32con
import win32gui
import win32process


def to_util_window(hwnd, transparent_color: int = None):
    if hwnd is None: return
    """设置窗口透明和置顶属性"""
    try:
        # 获取当前样式
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, win32con.GWL_EXSTYLE)

        # 设置新样式：透明、置顶、工具窗口
        new_style = (
                current_style | win32con.WS_EX_LAYERED |
                win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW
        )

        ctypes.windll.user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, new_style)

        if transparent_color is not None:
            # 设置窗口透明色
            win32gui.SetLayeredWindowAttributes(
                hwnd,
                transparent_color,  # 颜色键
                0,  # 透明度 (0-255)
                win32con.LWA_COLORKEY
            )
            pass

        # 刷新窗口
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,  # 位置
            win32con.SWP_NOSIZE | win32con.SWP_NOMOVE
        )

    except Exception as e:
        print(f"窗口属性设置失败: {e}")
    pass


def bring_to_front(hwnd):
    """ 窗口前置 """
    if sys.platform == "win32":
        user32 = ctypes.windll.user32

        # 如果窗口最小化了，恢复
        # if user32.IsIconic(hwnd):
        #     user32.ShowWindow(hwnd, 9)  # SW_RESTORE

        # 激活窗口并前置
        user32.ShowWindow(hwnd, win32con.SW_SHOW)
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)

        # 确保窗口获得焦点
        user32.SetFocus(hwnd)


def exit_to_background(hwnd):
    """ 退出至后台 """
    ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_HIDE)
    pass


def get_all_windows(include_hidden=False):
    """
    获取所有窗口句柄和详细信息
    include_hidden: 是否包含隐藏窗口
    """
    windows = []

    def callback(hwnd, windows_list):
        # 检查窗口是否可见（可选）
        if not include_hidden and not win32gui.IsWindowVisible(hwnd):
            return True

        try:
            # 获取窗口标题
            title = win32gui.GetWindowText(hwnd)

            # 获取窗口类名
            class_name = win32gui.GetClassName(hwnd)

            # 获取窗口位置和大小
            try:
                rect = win32gui.GetWindowRect(hwnd)
                x, y, right, bottom = rect
                width = right - x
                height = bottom - y
            except Exception as e:
                print(e)
                x = y = width = height = 0

            # 获取进程信息
            try:
                tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                process_name = process.name()
                exe_path = process.exe()
            except Exception as e:
                print(e)
                pid = 0
                process_name = "未知"
                exe_path = ""

            # 检查窗口是否有效
            if win32gui.IsWindow(hwnd):
                windows_list.append({
                    'hwnd': hwnd,
                    'title': title,
                    'class_name': class_name,
                    'pid': pid,
                    'process_name': process_name,
                    'exe_path': exe_path,
                    'position': (x, y),
                    'size': (width, height),
                    'visible': win32gui.IsWindowVisible(hwnd),
                    'enabled': win32gui.IsWindowEnabled(hwnd),
                })

        except Exception as e:
            print(e)
            pass  # 跳过无法访问的窗口

        return True  # 继续枚举

    win32gui.EnumWindows(callback, windows)
    return windows


def get_window_info_by_hwnd(hwnd):
    """根据句柄获取窗口详细信息"""
    try:
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)

        # 获取父窗口和子窗口
        parent = win32gui.GetParent(hwnd)

        # 获取窗口位置
        rect = win32gui.GetWindowRect(hwnd)

        # 判断窗口状态
        is_visible = win32gui.IsWindowVisible(hwnd)
        is_enabled = win32gui.IsWindowEnabled(hwnd)
        # is_zoomed = win32gui.IsZoomed(hwnd)
        is_iconic = win32gui.IsIconic(hwnd)

        return {
            'hwnd': hwnd,
            'title': title,
            'class_name': class_name,
            'style': style,
            'parent': parent,
            'rect': rect,
            'visible': is_visible,
            'enabled': is_enabled,
            # 'maximized': is_zoomed,
            'minimized': is_iconic,
        }
    except Exception as e:
        print(e)
        return None
