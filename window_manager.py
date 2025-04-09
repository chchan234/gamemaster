import sys
import platform

# 운영체제 확인
SYSTEM = platform.system()

# Windows 환경에서는 pygetwindow 사용
if SYSTEM == 'Windows':
    try:
        import pygetwindow as gw
        SIMULATION_MODE = False
    except ImportError:
        SIMULATION_MODE = True
        print("pygetwindow를 불러올 수 없습니다. 시뮬레이션 모드로 실행합니다.")
# macOS 환경에서는 AppKit 사용 시도
elif SYSTEM == 'Darwin':
    try:
        import pygetwindow as gw
        SIMULATION_MODE = False
    except (ImportError, NotImplementedError):
        SIMULATION_MODE = True
        print("macOS에서 윈도우 정보를 불러올 수 없습니다. 시뮬레이션 모드로 실행합니다.")
# 기타 환경(Linux 등)에서는 시뮬레이션 모드
else:
    SIMULATION_MODE = True
    print(f"{SYSTEM} 환경에서는 시뮬레이션 모드로 실행합니다.")

class WindowManager:
    def __init__(self):
        self.simulation_mode = SIMULATION_MODE
        # 시뮬레이션 모드일 때 사용할 가상 윈도우 목록
        self.simulated_windows = [
            "게임 클라이언트: 메인 화면", 
            "게임 클라이언트: 월드맵", 
            "게임 클라이언트: 던전 인스턴스",
            "테스트 윈도우 1",
            "테스트 윈도우 2"
        ]
        
        # 운영 체제 타입 저장
        self.system = platform.system()
    
    def get_windows(self):
        """현재 실행 중인 모든 윈도우 목록을 반환합니다."""
        if self.simulation_mode:
            # 운영체제별 시뮬레이션 윈도우 목록 확장
            if self.system == 'Windows':
                return self.simulated_windows + [
                    "게임 - 메인 화면", 
                    "메인 메뉴", 
                    "로비", 
                    "Microsoft Edge", 
                    "Chrome", 
                    "메모장", 
                    "계산기"
                ]
            else:
                return self.simulated_windows
        else:
            try:
                # 실제 열려있는 모든 윈도우 목록 가져오기
                all_windows = gw.getAllTitles()
                # 빈 제목 필터링
                active_windows = [title for title in all_windows if title.strip()]
                # 결과가 비어있으면 시뮬레이션 모드로 대체
                if not active_windows:
                    print("윈도우 목록을 가져올 수 없습니다. 시뮬레이션 모드로 전환합니다.")
                    self.simulation_mode = True
                    return self.get_windows()
                return active_windows
            except Exception as e:
                print(f"윈도우 목록 가져오기 실패: {e}")
                self.simulation_mode = True
                return self.get_windows()
    
    def activate_window(self, window_title):
        """선택된 윈도우를 활성화합니다."""
        if self.simulation_mode:
            print(f"시뮬레이션: '{window_title}' 윈도우 활성화")
            return True
        else:
            try:
                window = gw.getWindowsWithTitle(window_title)[0]
                window.activate()
                return True
            except (IndexError, Exception) as e:
                print(f"윈도우 활성화 실패: {e}")
                return False
    
    def get_window_rect(self, window_title):
        """윈도우의 위치와 크기를 반환합니다."""
        if self.simulation_mode:
            # 시뮬레이션 모드에서는 가상의 윈도우 크기 반환
            return 0, 0, 800, 600
        else:
            try:
                window = gw.getWindowsWithTitle(window_title)[0]
                return window.left, window.top, window.width, window.height
            except (IndexError, Exception):
                # 윈도우를 찾지 못한 경우 기본 좌표 반환
                return 0, 0, 800, 600