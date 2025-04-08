import streamlit as st
import time
from window_manager import WindowManager
from image_recognition import ImageRecognizer
from auto_controller import AutoController

def main():
    st.title("게임 치트 자동화 프로그램")
    
    # 세션 상태 초기화
    if 'window_confirmed' not in st.session_state:
        st.session_state.window_confirmed = False
    
    if 'selected_window' not in st.session_state:
        st.session_state.selected_window = None
    
    # 사이드바 설정
    st.sidebar.title("설정")
    
    # 치트 코드 카테고리 및 하위 메뉴 구조
    cheat_structure = {
        "🔥 전투 및 공격 관련": [
            "유닛 수동 공격",
            "HP 절반 만들기",
            "HP, MP 전체 회복",
            "PC 무적(피격 면역) 처리",
            "대미지 증가 실행",
            "PC 스킬 쿨타임 미적용 + 마나 소모 0",
            "반격 (활성 / 비활성)",
            "스킬 사용 (통보 / 확인)",
            "우클릭 이동 (활성 / 비활성)",
            "서버를 통한 움직임 디버그 표시 (표시 / 비표시)",
            "스킬 사용, 우클릭 이동, 서버를 통한 움직임 디버그 표시 한번에 (활성 / 비활성)",
            "플레이어 위치 클립보드로 복사",
            "BASE 이동"
        ],
        "🎯 이동 및 위치 조작 관련": [
            "유닛 좌표 이동",
            "NPC 좌표로 이동",
            "PROP 좌표로 이동",
            "퀘스트 목표 지역으로 이동",
            "현재 진행 중인 퀘스트 다음 스텝 강제 실행",
            "현재 진행 중인 퀘스트 이전 스텝 강제 실행",
            "특정 퀘스트 강제 실행",
            "특정 ID 퀘스트 골카운트 n 수치로 실행"
        ],
        "🎁 아이템 및 보상 생성 관련": [
            "아이템 생성",
            "아바타 아이템 생성",
            "탈것 생성",
            "정령 생성",
            "정령 즐겨찾기",
            "정령 즐겨찾기 해제",
            "정령, 탈것, 무기소울, 아바타, 아스터 생성",
            "강화된 아이템 생성",
            "귀속 여부에 따른 아이템 생성",
            "아이템 보상 드랍 FX Trail 속도",
            "커런시 획득"
        ],
        "📈 아이템 강화 및 합성 관련": [
            "아이템 강화",
            "아이템 하락 강화",
            "합성",
            "확정 - 교체",
            "자동 합성",
            "실패누적보상"
        ],
        "📚 퀘스트 조작 관련": [
            "퀘스트 몬스터킬",
            "일일 의뢰 초기화"
        ],
        "🎓 경험치 및 성장 관련": [
            "경험치 증가",
            "스킬 획득",
            "길드 경험치 설정",
            "폴른 포인트 초기화"
        ],
        "🛠️ 테스트 및 디버깅 관련": [
            "테스트 모드 변경",
            "상태이상 테스트 (활성 / 비활성)",
            "충돌 테스트 (활성 / 비활성)",
            "파티원 어시스트 테스트 (활성 / 비활성)",
            "배틀로얄 참가 최대 인원 변경",
            "자살",
            "가방 비우기",
            "유닛 속도 변경",
            "서버 치트키 직접 실행",
            "치트창 열기"
        ]
    }
    
    # 치트 코드 매핑 (서버에 실제로 전송될 코드)
    cheat_codes = {
        # 전투 및 공격 관련
        "유닛 수동 공격": "ATTACK_MANUAL",
        "HP 절반 만들기": "HP_HALF",
        "HP, MP 전체 회복": "FULL_RECOVERY",
        "PC 무적(피격 면역) 처리": "GOD_MODE",
        "대미지 증가 실행": "DAMAGE_BOOST",
        "PC 스킬 쿨타임 미적용 + 마나 소모 0": "NO_COOLDOWN",
        "반격 (활성 / 비활성)": "COUNTER_TOGGLE",
        "스킬 사용 (통보 / 확인)": "SKILL_NOTIFICATION",
        "우클릭 이동 (활성 / 비활성)": "RIGHT_CLICK_MOVE",
        "서버를 통한 움직임 디버그 표시 (표시 / 비표시)": "MOVE_DEBUG",
        "스킬 사용, 우클릭 이동, 서버를 통한 움직임 디버그 표시 한번에 (활성 / 비활성)": "ALL_DEBUG",
        "플레이어 위치 클립보드로 복사": "COPY_POS",
        "BASE 이동": "MOVE_BASE",
        
        # 나머지 카테고리의 치트 코드들도 비슷한 방식으로 매핑됩니다.
        # 여기서는 대표적으로 첫 번째 카테고리만 상세하게 매핑했습니다.
    }
    
    # 윈도우 목록 가져오기
    window_manager = WindowManager()
    windows = window_manager.get_windows()
    
    if not windows:
        st.error("활성화된 윈도우가 없습니다.")
        return
    
    # 윈도우 선택을 사이드바로 이동
    st.sidebar.subheader("게임 창 선택")
    
    # 게임 창이 아직 확정되지 않은 경우, 선택 UI 표시
    if not st.session_state.window_confirmed:
        # 선택 상자와 확인 버튼을 나란히 배치하기 위한 열 생성
        window_col1, window_col2 = st.sidebar.columns([3, 1])
        
        # 첫 번째 열에 선택 상자 배치
        selected_window = window_col1.selectbox(
            "게임 창을 선택하세요:",
            windows
        )
        
        # 두 번째 열에 확인 버튼 배치
        if window_col2.button("확인", key="confirm_window"):
            st.session_state.window_confirmed = True
            st.session_state.selected_window = selected_window
            st.rerun()  # UI 업데이트를 위해 페이지 리로드
    else:
        # 이미 확정된 게임 창 정보 표시
        st.sidebar.success(f"게임 창: '{st.session_state.selected_window}' 적용됨")
        
        # 변경 버튼 추가
        if st.sidebar.button("변경", key="change_window"):
            st.session_state.window_confirmed = False
            st.rerun()  # UI 업데이트를 위해 페이지 리로드
        
        # 선택된 창 사용
        selected_window = st.session_state.selected_window
    
    # 카테고리 선택을 메인 화면으로 이동
    st.subheader("치트 카테고리")
    selected_category = st.selectbox(
        "카테고리를 선택하세요:",
        list(cheat_structure.keys())
    )
    
    # 선택된 카테고리의 치트 코드 선택을 메인 화면으로 이동
    selected_cheat = st.selectbox(
        "기능을 선택하세요:",
        cheat_structure[selected_category]
    )
    
    # 테스트 모드 변경을 위한 추가 선택 옵션 (메인 화면으로 이동)
    test_mode_options = None
    if selected_category == "🛠️ 테스트 및 디버깅 관련" and selected_cheat == "테스트 모드 변경":
        test_mode_options = st.selectbox(
            "테스트 모드 선택:",
            [
                "1. 상태이상 테스트 활성",
                "2. 충돌 테스트 활성",
                "3. 파티원 어시스트 테스트 활성",
                "0. 모두 비활성"
            ]
        )
    
    # 선택된 치트 코드 가져오기
    # 테스트 모드 변경인 경우 세부 옵션 코드 사용
    if test_mode_options:
        cheat_code = test_mode_options.replace(" ", "_").upper()
    else:
        # 매핑된 코드가 없으면 기본값으로 치트 이름 그대로 사용
        cheat_code = cheat_codes.get(selected_cheat, selected_cheat.replace(" ", "_").upper())
    
    # 게임 창이 확정된 경우에만 치트 실행 버튼 활성화
    if st.session_state.window_confirmed:
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
                auto_controller.execute_code_flow(image_recognizer, cheat_code)
                
                # 테스트 모드 변경인 경우 세부 옵션 메시지 표시
                if test_mode_options:
                    st.success(f"테스트 모드가 '{test_mode_options}'(으)로 성공적으로 변경되었습니다!")
                else:
                    st.success(f"{selected_cheat} 치트가 성공적으로 적용되었습니다!")
            
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("게임 창을 선택하고 '확인' 버튼을 눌러주세요.")

if __name__ == "__main__":
    main() 