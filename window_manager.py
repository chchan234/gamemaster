import pygetwindow as gw
import win32gui
import win32con

class WindowManager:
    def get_windows(self):
        """현재 실행 중인 모든 윈도우 목록을 반환합니다."""
        windows = []
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append(title)
            return True
        
        win32gui.EnumWindows(callback, windows)
        return windows
    
    def activate_window(self, window_title):
        """선택된 윈도우를 활성화합니다."""
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            window.activate()
            return True
        except Exception as e:
            raise Exception(f"윈도우 활성화 실패: {str(e)}")
    
    def get_window_rect(self, window_title):
        """윈도우의 위치와 크기를 반환합니다."""
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            return window.left, window.top, window.width, window.height
        except Exception as e:
            raise Exception(f"윈도우 정보 가져오기 실패: {str(e)}") 