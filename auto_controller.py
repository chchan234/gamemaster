import pyautogui
import time

class AutoController:
    def __init__(self):
        # PyAutoGUI 설정
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def click_position(self, position):
        """주어진 위치를 클릭합니다."""
        try:
            x, y = position
            pyautogui.click(x, y)
            time.sleep(0.5)  # 클릭 후 대기
        except Exception as e:
            raise Exception(f"클릭 실패: {str(e)}")
    
    def enter_cheat_code(self, cheat_code):
        """치트 코드를 입력합니다."""
        try:
            pyautogui.write(cheat_code)
            time.sleep(0.5)  # 입력 후 대기
        except Exception as e:
            raise Exception(f"치트 코드 입력 실패: {str(e)}")
    
    def press_key(self, key):
        """특정 키를 누릅니다."""
        try:
            pyautogui.press(key)
            time.sleep(0.5)  # 키 입력 후 대기
        except Exception as e:
            raise Exception(f"키 입력 실패: {str(e)}")
    
    def execute_menu_flow(self, image_recognizer):
        """메뉴 클릭 플로우를 실행합니다."""
        try:
            # menu2 확인
            menu2_location = image_recognizer.find_menu2()
            
            if menu2_location:
                # menu2가 보일 때
                self.click_position(menu2_location)
                time.sleep(1)
            else:
                # menu2가 보이지 않을 때
                menu_location = image_recognizer.find_menu()
                if menu_location:
                    self.click_position(menu_location)
                    time.sleep(1)
            
            # menu3 클릭
            menu3_location = image_recognizer.find_menu3()
            if menu3_location:
                self.click_position(menu3_location)
                time.sleep(1)
            else:
                raise Exception("menu3을 찾을 수 없습니다.")
                
        except Exception as e:
            raise Exception(f"메뉴 플로우 실행 실패: {str(e)}")
    
    def execute_code_flow(self, image_recognizer, cheat_code):
        """치트 코드 입력 플로우를 실행합니다."""
        try:
            # code 클릭
            code_location = image_recognizer.find_code()
            if code_location:
                self.click_position(code_location)
                time.sleep(1)
            else:
                raise Exception("code를 찾을 수 없습니다.")
            
            # code2 클릭
            code2_location = image_recognizer.find_code2()
            if code2_location:
                self.click_position(code2_location)
                time.sleep(1)
            else:
                raise Exception("code2를 찾을 수 없습니다.")
            
            # 치트 코드 입력
            self.enter_cheat_code(cheat_code)
            time.sleep(1)
            
            # code3 클릭
            code3_location = image_recognizer.find_code3()
            if code3_location:
                self.click_position(code3_location)
                time.sleep(1)
            else:
                raise Exception("code3을 찾을 수 없습니다.")
            
            # code4 클릭
            code4_location = image_recognizer.find_code4()
            if code4_location:
                self.click_position(code4_location)
                time.sleep(1)
            else:
                raise Exception("code4를 찾을 수 없습니다.")
                
        except Exception as e:
            raise Exception(f"코드 플로우 실행 실패: {str(e)}") 