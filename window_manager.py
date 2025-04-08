import pyautogui

class WindowManager:
    def get_windows(self):
        """현재 실행 중인 모든 윈도우 목록을 반환합니다."""
        # 데모 목적으로 더미 윈도우 목록 반환
        return ["게임 창 1", "게임 창 2", "게임 창 3"]
    
    def activate_window(self, window_title):
        """선택된 윈도우를 활성화합니다."""
        # 데모 목적으로 항상 성공으로 처리
        return True
    
    def get_window_rect(self, window_title):
        """윈도우의 위치와 크기를 반환합니다."""
        # 데모 목적으로 기본 좌표 반환
        return 0, 0, 800, 600 