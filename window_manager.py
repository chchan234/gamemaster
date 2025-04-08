import pyautogui

class WindowManager:
    def get_windows(self):
        """현재 실행 중인 모든 윈도우 목록을 반환합니다."""
        try:
            windows = []
            for window in pyautogui.getAllWindows():
                if window.title:
                    windows.append(window.title)
            return windows
        except Exception as e:
            raise Exception(f"윈도우 목록 가져오기 실패: {str(e)}")
    
    def activate_window(self, window_title):
        """선택된 윈도우를 활성화합니다."""
        try:
            windows = pyautogui.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                window.activate()
                return True
            return False
        except Exception as e:
            raise Exception(f"윈도우 활성화 실패: {str(e)}")
    
    def get_window_rect(self, window_title):
        """윈도우의 위치와 크기를 반환합니다."""
        try:
            windows = pyautogui.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                return window.left, window.top, window.width, window.height
            return None
        except Exception as e:
            raise Exception(f"윈도우 정보 가져오기 실패: {str(e)}") 