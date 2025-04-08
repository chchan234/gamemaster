import cv2
import numpy as np
import pyautogui
import os

class ImageRecognizer:
    def __init__(self):
        self.template_dir = "templates"
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
    
    def find_template(self, template_name, confidence=0.8):
        """템플릿 이미지를 찾아 위치를 반환합니다."""
        try:
            # 스크린샷 캡처
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # 템플릿 이미지 로드
            template_path = os.path.join(self.template_dir, f"{template_name}.png")
            template = cv2.imread(template_path)
            
            if template is None:
                raise Exception(f"템플릿 이미지를 찾을 수 없습니다: {template_name}")
            
            # 템플릿 매칭
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                # 템플릿의 중앙 좌표 계산
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
            return None
            
        except Exception as e:
            raise Exception(f"이미지 인식 실패: {str(e)}")
    
    def find_menu(self):
        """메뉴 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("menu")
    
    def find_menu2(self):
        """menu2 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("menu2")
    
    def find_menu3(self):
        """menu3 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("menu3")
    
    def find_code(self):
        """code 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("code")
    
    def find_code2(self):
        """code2 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("code2")
    
    def find_code3(self):
        """code3 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("code3")
    
    def find_code4(self):
        """code4 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("code4")
    
    def find_input_box(self):
        """치트 입력창을 찾아 위치를 반환합니다."""
        return self.find_template("input_box")
    
    def find_confirm_button(self):
        """확인 버튼을 찾아 위치를 반환합니다."""
        return self.find_template("confirm_button") 