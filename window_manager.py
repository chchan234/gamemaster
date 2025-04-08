import pygetwindow as gw

class WindowManager:
    def get_windows(self):
        """현재 실행 중인 모든 윈도우 목록을 반환합니다."""
        # 실제 열려있는 모든 윈도우 목록 가져오기
        all_windows = gw.getAllTitles()
        # 빈 제목 필터링
        active_windows = [title for title in all_windows if title.strip()]
        return active_windows
    
    def activate_window(self, window_title):
        """선택된 윈도우를 활성화합니다."""
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            window.activate()
            return True
        except (IndexError, Exception) as e:
            print(f"윈도우 활성화 실패: {e}")
            return False
    
    def get_window_rect(self, window_title):
        """윈도우의 위치와 크기를 반환합니다."""
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            return window.left, window.top, window.width, window.height
        except (IndexError, Exception):
            # 윈도우를 찾지 못한 경우 기본 좌표 반환
            return 0, 0, 800, 600