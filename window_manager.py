import sys
import platform

# 운영체제 확인
SYSTEM = platform.system()

# Windows 환경에서는 pygetwindow 사용
if SYSTEM == 'Windows':
    try:
        # PyGetWindow는 윈도우 환경에서 윈도우 컨트롤을 위해 필수 라이브러리
        import pygetwindow as gw
        print("윈도우 관리 모듈이 성공적으로 로드되었습니다.")
        SIMULATION_MODE = False
    except ImportError:
        # 설치되지 않은 경우 자동 설치 제안 메시지 출력
        SIMULATION_MODE = True
        print("윈도우 관리 모듈(pygetwindow)을 불러올 수 없습니다.")
        print("시뮬레이션 모드로 실행합니다.")
        print("실제 윈도우 선택을 위해 다음 명령을 실행하세요: pip install pygetwindow==0.0.9")
# macOS 환경에서는 AppKit 사용 시도
elif SYSTEM == 'Darwin':
    try:
        import pygetwindow as gw
        SIMULATION_MODE = False
    except (ImportError, NotImplementedError):
        SIMULATION_MODE = True
        print("macOS에서 윈도우 정보를 불러올 수 없습니다. 시뮬레이션 모드로 실행합니다.")
# Linux 환경에서는 현재 직접 지원이 어려워 시뮬레이션 모드 사용
# 나중에 Linux 지원을 추가할 수 있음
elif SYSTEM == 'Linux':
    SIMULATION_MODE = True
    print("Linux 환경에서는 현재 시뮬레이션 모드로만 실행됩니다.")
# 기타 환경에서는 시뮬레이션 모드
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
        
        # 환경 감지 및 시뮬레이션 모드 오버라이드
        # 사용자가 강제로 실제 윈도우 사용 가능
        self.check_environment()
    
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
                
                # Windows에서는 특별히 추가 로깅 - 디버깅용
                if self.system == 'Windows':
                    print(f"감지된 윈도우 수: {len(all_windows)}")
                    print(f"유효한 윈도우 수: {len(active_windows)}")
                    # 일부 윈도우 제목 출력 (최대 5개)
                    if active_windows:
                        print("감지된 윈도우 예시:")
                        for idx, title in enumerate(active_windows[:5]):
                            print(f"  {idx+1}. {title}")
                
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
    
    def check_environment(self):
        """환경을 확인하고 윈도우 시스템 사용 가능성 테스트"""
        # 이미 시뮬레이션 모드가 아니라면 그대로 유지
        if not self.simulation_mode:
            return
        
        # Windows 환경에서는 추가로 pygetwindow 다시 로드 시도
        if self.system == 'Windows':
            try:
                # pygetwindow를 다시 로드 시도
                import pygetwindow as gw
                
                # 간단한 테스트로 윈도우 목록을 가져와봄
                windows = gw.getAllTitles()
                if windows:
                    print(f"윈도우 {len(windows)}개를 감지했습니다.")
                    print("Windows 환경에서 윈도우 관리 기능을 사용합니다.")
                    self.simulation_mode = False
                    return
            except Exception as e:
                print(f"Windows 환경 윈도우 관리 로드 오류: {e}")
                print("pygetwindow가 올바르게 설치되었는지 확인하세요: pip install pygetwindow==0.0.9")
                
        # Linux 환경에서 추가 확인 
        elif self.system == 'Linux':
            try:
                # PyAutoGUI를 통해 스크린 크기 확인 시도
                import pyautogui
                screen_width, screen_height = pyautogui.size()
                
                # 스크린 크기를 가져올 수 있다면 
                # 윈도우 관리 패키지가 제대로 설치된 것으로 간주
                if screen_width > 0 and screen_height > 0:
                    print(f"화면 크기 감지: {screen_width}x{screen_height}")
                    print("Linux 환경에서 윈도우 관리를 사용할 수 있습니다.")
                    # 실제 윈도우 사용 설정
                    self.simulation_mode = False
                    return
            except Exception as e:
                print(f"Linux 환경 확인 중 오류: {e}")
                print("시뮬레이션 모드로 계속합니다.")
    
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