import os
import random

class ImageRecognizer:
    def __init__(self):
        self.template_dir = "templates"
        self.simulation_mode = True
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
    
    def find_template(self, template_name, confidence=0.8):
        """템플릿 이미지를 찾아 위치를 반환합니다."""
        if self.simulation_mode:
            # 시뮬레이션 모드에서는 더미 좌표 반환
            if template_name == "menu2":
                # menu2는 50% 확률로 발견되지 않음 (시뮬레이션)
                if random.random() < 0.5:
                    return None
            return (100, 100)  # 더미 좌표
    
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