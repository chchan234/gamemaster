import streamlit as st
import time
from window_manager import WindowManager
from image_recognition import ImageRecognizer
from auto_controller import AutoController

def main():
    st.title("게임 치트 자동화 프로그램")
    
    # 사이드바 설정
    st.sidebar.title("설정")
    
    # 치트 코드 선택
    cheat_codes = {
        "무적": "GODMODE",
        "무한 탄약": "INFINITEAMMO",
        "모든 무기": "ALLWEAPONS",
        "스텔스 모드": "STEALTHMODE"
    }
    
    selected_cheat = st.sidebar.selectbox(
        "치트를 선택하세요:",
        list(cheat_codes.keys())
    )
    
    # 윈도우 목록 가져오기
    window_manager = WindowManager()
    windows = window_manager.get_windows()
    
    if not windows:
        st.error("활성화된 윈도우가 없습니다.")
        return
    
    # 윈도우 선택 드롭다운
    selected_window = st.selectbox(
        "게임 창을 선택하세요:",
        windows
    )
    
    if st.button("치트 실행"):
        try:
            # 선택된 윈도우 활성화
            window_manager.activate_window(selected_window)
            time.sleep(1)  # 윈도우 활성화 대기
            
            # 이미지 인식 및 자동화 실행
            image_recognizer = ImageRecognizer()
            auto_controller = AutoController()
            
            # 메뉴 플로우 실행
            auto_controller.execute_menu_flow(image_recognizer)
            
            # 코드 플로우 실행
            auto_controller.execute_code_flow(image_recognizer, cheat_codes[selected_cheat])
            
            st.success(f"{selected_cheat} 치트가 성공적으로 적용되었습니다!")
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main() 