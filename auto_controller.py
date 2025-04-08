import time

class AutoController:
    def __init__(self):
        # 시뮬레이션 모드 설정
        self.simulation_mode = True
    
    def click_position(self, position):
        """주어진 위치를 클릭합니다."""
        if self.simulation_mode:
            print(f"클릭 시뮬레이션: {position}")
            time.sleep(0.5)
            return True
    
    def enter_cheat_code(self, cheat_code):
        """치트 코드를 입력합니다."""
        if self.simulation_mode:
            print(f"코드 입력 시뮬레이션: {cheat_code}")
            time.sleep(0.5)
            return True
    
    def press_key(self, key):
        """특정 키를 누릅니다."""
        if self.simulation_mode:
            print(f"키 입력 시뮬레이션: {key}")
            time.sleep(0.5)
            return True
    
    def execute_menu_flow(self, image_recognizer):
        """메뉴 클릭 플로우를 실행합니다."""
        if self.simulation_mode:
            print("메뉴 플로우 시뮬레이션 실행")
            # menu2 확인
            menu2_found = image_recognizer.find_menu2() is not None
            
            if menu2_found:
                print("menu2 클릭")
            else:
                print("menu 클릭")
            
            print("menu3 클릭")
            time.sleep(1)
            return True
    
    def execute_code_flow(self, image_recognizer, cheat_code):
        """치트 코드 입력 플로우를 실행합니다."""
        if self.simulation_mode:
            print("코드 플로우 시뮬레이션 실행")
            print("code 클릭")
            print("code2 클릭")
            print(f"치트 코드 입력: {cheat_code}")
            print("code3 클릭")
            print("code4 클릭")
            time.sleep(1)
            return True 