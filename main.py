# PyInstaller 환경에서의 임포트 에러 처리
try:
    import streamlit as st
except ImportError as e:
    # 패키징된 환경에서 실행 중인지 확인
    if getattr(sys, 'frozen', False):
        import sys
        import os
        import tkinter as tk
        from tkinter import messagebox
        
        # 에러 출력
        print(f"Streamlit 모듈 임포트 오류: {e}")
        
        # 기본 tkinter 메시지 출력
        root = tk.Tk()
        root.withdraw()  # 메인 창 숨기기
        messagebox.showerror("오류", f"필요한 모듈을 찾을 수 없습니다: {e}\n\n'환경 설정' 버튼을 눌러 필요한 패키지를 설치하세요.")
        sys.exit(1)
    else:
        # 일반 환경에서는 그대로 예외 발생
        raise

import streamlit as st
import time
import json
import os
import sys
import platform
import pandas as pd
# 외부 라이브러리들을 가져옵니다
from window_manager import WindowManager
from image_recognition import ImageRecognizer
from auto_controller import AutoController
from item_database import filter_items, search_items_by_name, JOB_LIST, GRADE_LIST, PART_LIST, GRADE_COLORS, CHARACTER_LIST

# 전역 변수 정의
test_mode_options = None

# 밝은 테마 및 모던 UI 스타일 설정
st.set_page_config(
    page_title="게임 치트 자동화 프로그램",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS 스타일 적용
st.markdown("""
<style>
    /* 기본 스타일 초기화 */
    .main {
        background-color: white;
        color: #333333;
    }
    
    /* 심플한 헤더 스타일 */
    h1 {
        color: #333333 !important;
        font-size: 28px !important;
        font-weight: 600;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    
    h2 {
        color: #333333 !important;
        font-size: 20px !important;
        margin-top: 20px;
    }
    
    h3 {
        color: #333333 !important;
        font-size: 16px !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #4285F4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #3b78e7;
    }
    
    /* 선택 박스 */
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    /* 심플한 알림 메시지 */
    div[data-testid="stInfo"] {
        background-color: #e8f0fe;
        padding: 10px;
        border-radius: 4px;
    }
    
    div[data-testid="stSuccess"] {
        background-color: #e6f4ea;
        padding: 10px;
        border-radius: 4px;
    }
    
    div[data-testid="stWarning"] {
        background-color: #fef7e0;
        padding: 10px;
        border-radius: 4px;
    }
    
    div[data-testid="stError"] {
        background-color: #fce8e6;
        padding: 10px;
        border-radius: 4px;
    }
    
    /* 구분선 */
    hr {
        margin: 15px 0;
        border: none;
        height: 1px;
        background-color: #eee;
    }
    
    /* 메뉴 버튼 스타일 */
    .cat-button {
        text-align: left !important;
        margin-bottom: 2px !important;
        padding: 8px !important;
    }
    
    .sub-button {
        text-align: left !important;
        padding-left: 20px !important;
        font-size: 14px !important;
        background-color: #f8f9fa !important;
        color: #333 !important;
    }
    
    /* 텍스트 기본 간격 */
    p {
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

def load_data(filename):
    """
    Excel 파일에서 데이터를 로드하는 함수
    지원 형식: Excel(xlsx, xls)
    파일이 없으면 빈 리스트 반환
    """
    try:
        # Excel 파일 경로로 변환 (json 파일이름이 들어오면 엑셀 파일 경로로 변환)
        base_filename = os.path.basename(filename)  # 파일명만 추출
        name_without_ext, ext = os.path.splitext(base_filename)
        
        if ext.lower() == '.json':
            # data/items.json -> excel_data/items.xlsx
            excel_filename = os.path.join('excel_data', name_without_ext + '.xlsx')
        else:
            excel_filename = filename
            
        # 파일 존재 여부 확인
        if not os.path.exists(excel_filename):
            # 최초 실행 시 샘플 Excel 파일 생성
            if name_without_ext in ['asters', 'avatars', 'items', 'spirits', 'vehicles', 'weapon_souls']:
                st.info(f"'{excel_filename}' 파일이 없습니다. 샘플 데이터를 생성합니다.")
                
                # 샘플 데이터 생성
                sample_data = []
                
                if name_without_ext == 'asters':
                    sample_data = [
                        {"id": "111001", "name": "일반 선봉의 아스터1", "type": "아스터", "grade": "COMMON", "방향": "1"},
                        {"id": "112001", "name": "고급 선봉의 아스터1", "type": "아스터", "grade": "ADVANCE", "방향": "2"},
                        {"id": "113001", "name": "희귀 선봉의 아스터1", "type": "아스터", "grade": "RARE", "방향": "3"}
                    ]
                elif name_without_ext == 'avatars':
                    sample_data = [
                        {"id": "110018000", "name": "가벼운 사냥복", "type": "아바타", "grade": "COMMON", "job": "헌터"},
                        {"id": "110018001", "name": "추격자의 사냥복", "type": "아바타", "grade": "COMMON", "job": "헌터"},
                        {"id": "210018000", "name": "마법사의 로브", "type": "아바타", "grade": "RARE", "job": "마법사"}
                    ]
                else:
                    sample_data = [
                        {"id": "000001", "name": "샘플 아이템", "type": "기타", "grade": "COMMON", "job": "공용"},
                        {"id": "000002", "name": "샘플 아이템2", "type": "기타", "grade": "COMMON", "job": "공용"}
                    ]
                
                # 샘플 데이터 저장
                df = pd.DataFrame(sample_data)
                
                # 디렉토리 생성
                os.makedirs(os.path.dirname(excel_filename), exist_ok=True)
                
                # Excel 파일로 저장
                df.to_excel(excel_filename, index=False)
                st.success(f"'{excel_filename}' 파일이 생성되었습니다. 이 파일을 직접 편집하여 데이터를 관리할 수 있습니다.")
            else:
                st.warning(f"파일을 찾을 수 없습니다: {excel_filename}")
                return []
            
        # Excel 파일 처리
        df = pd.read_excel(excel_filename)
        
        # 빈 값 처리
        df = df.fillna('')
        
        # DataFrame을 딕셔너리 리스트로 변환
        data = df.to_dict('records')
        
        # 디버그: 아이템 타입 값 확인 (로그로 출력)
        if data and len(data) > 0 and excel_filename.endswith('Items.xlsx'):
            print("Items.xlsx 파일 컬럼 확인:")
            print(list(data[0].keys()))
            
            # 타입 값 추출 (정확한 키 확인)
            type_keys = ['Type', 'type', 'TYPE', 'item_type', 'ItemType']
            found_key = None
            
            # 어떤 키가 있는지 확인
            for key in type_keys:
                if key in data[0]:
                    found_key = key
                    break
            
            if found_key:
                print(f"Items.xlsx 파일에서 타입 값은 '{found_key}' 키에 저장되어 있습니다.")
                
                # 해당 키의 모든 고유 값 추출
                type_values = set()
                for item in data:
                    type_value = item.get(found_key, '')
                    if type_value and str(type_value).strip():
                        type_values.add(str(type_value).strip())
                
                print(f"Items.xlsx 파일 {found_key} 값 목록:")
                print(sorted(list(type_values)))
            else:
                print("Items.xlsx 파일에 타입 관련 키를 찾을 수 없습니다.")
                
                # 샘플 아이템 몇 개 확인
                print("샘플 아이템 데이터:")
                for i, item in enumerate(data[:3]):
                    print(f"아이템 {i+1}:", item)
            
        return data
            
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {str(e)}")
        return []

# 이전 함수 호환성 유지
def load_data_from_json(filename):
    """
    기존 JSON 파일명을 받아 Excel 파일을 로드하는 함수 (하위 호환성 유지)
    """
    return load_data(filename)

def filter_data_with_rag(data, filters):
    """
    Excel 데이터를 필터링하는 함수
    - 사용자 정의 필터 기준에 따라 Excel에서 로드된 데이터 필터링
    - 여러 필드에서 값을 검색할 수 있도록 지원 (Name이나 char에서 직업 검색)
    """
    if not data:
        return []
    
    # 원본 데이터 유지
    filtered_data = data
    
    # 엑셀 파일 컬럼명 매핑 (실제 엑셀 컬럼명 확인 결과 기반)
    excel_column_mapping = {
        'grade': 'Grade',     # 우리 코드: 엑셀 컬럼명
        'name': 'Name',
        'id': 'Id',
        'job': ['char', 'Name'],  # job 필드는 char 또는 Name 컬럼에서 검색
        'type': 'Type',        # 아이템 타입 필드
        '방향': 'Direction'
    }
    
    # 필터 적용
    for key, value in filters.items():
        if value and value != "모두":
            new_filtered = []
            
            # 등급 필터링 (Grade 컬럼)
            if key.lower() == 'grade':
                excel_key = excel_column_mapping.get(key, key)
                for item in filtered_data:
                    if excel_key in item and str(item[excel_key]).lower() == str(value).lower():
                        new_filtered.append(item)
                        
            # 직업 필터링 (char 컬럼에서만 검색)
            elif key.lower() == 'job':
                for item in filtered_data:
                    # char 필드에서 검색 (부분 일치)
                    if 'char' in item and str(value).lower() in str(item['char']).lower():
                        new_filtered.append(item)
                        continue
                    
                    # 원래 job 필드 검색 (하위 호환성)
                    if 'job' in item and str(item['job']).lower() == str(value).lower():
                        new_filtered.append(item)
                        continue
            
            # 타입 필터링 처리 (Type 또는 type 필드)
            elif key.lower() == 'type':
                # 모든 가능한 타입 필드 키
                type_keys = ['Type', 'type', 'TYPE', 'item_type', 'ItemType']
                
                for item in filtered_data:
                    # 모든 가능한 타입 키 확인
                    for type_key in type_keys:
                        if type_key in item:
                            type_value = str(item[type_key]).lower()
                            value_lower = str(value).lower()
                            
                            # 정확히 일치하거나 부분 일치
                            if type_value == value_lower or value_lower in type_value:
                                new_filtered.append(item)
                                break  # 타입 키 루프 종료
                    
                    # 이미 추가된 아이템은 건너뛰기
                    if item in new_filtered:
                        continue
            
            # 기타 필터 (방향 등)
            else:
                excel_key = excel_column_mapping.get(key, key)
                if isinstance(excel_key, list):
                    # 여러 필드에서 검색
                    for item in filtered_data:
                        for field in excel_key:
                            if field in item and str(item[field]).lower() == str(value).lower():
                                new_filtered.append(item)
                                break
                else:
                    # 단일 필드에서 검색
                    for item in filtered_data:
                        if excel_key in item and str(item[excel_key]).lower() == str(value).lower():
                            new_filtered.append(item)
            
            filtered_data = new_filtered
            
            # 결과가 없으면 디버그 메시지 표시
            if not filtered_data:
                print(f"필터 '{key}'='{value}'로 매칭된 항목이 없습니다.")
    
    return filtered_data

def main():
    # 앱 로고와 타이틀을 포함한 헤더 구성
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image("templates/menu.png", width=80)
        except:
            # 이미지를 로드할 수 없는 경우 아이콘으로 대체
            st.markdown("# 🎮")
    with col2:
        st.title("게임 치트 자동화 프로그램")
        st.markdown("##### 편리하고 안전한 게임 치트 코드 입력 자동화 시스템")
    
    st.markdown("---")
    
    # 세션 상태 초기화
    if 'window_confirmed' not in st.session_state:
        st.session_state.window_confirmed = False
    
    if 'selected_window' not in st.session_state:
        st.session_state.selected_window = None
    
    if 'current_cheat' not in st.session_state:
        st.session_state.current_cheat = None
    
    if 'current_category' not in st.session_state:
        st.session_state.current_category = None
        
    if 'expanded_categories' not in st.session_state:
        st.session_state.expanded_categories = {}
    
    # 아이콘 없는 카테고리 이름
    categories = [
        "전투 및 공격 관련",
        "이동 및 위치 조작 관련",
        "아이템 및 보상 생성 관련",
        "아이템 강화 및 합성 관련",
        "퀘스트 조작 관련",
        "경험치 및 성장 관련",
        "테스트 및 디버깅 관련",
        "설정"
    ]
    
    # 치트 코드 카테고리 및 하위 메뉴 구조 (아이콘 제거)
    cheat_structure = {
        "전투 및 공격 관련": [
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
        "이동 및 위치 조작 관련": [
            "유닛 좌표 이동",
            "NPC 좌표로 이동",
            "PROP 좌표로 이동",
            "퀘스트 목표 지역으로 이동",
            "현재 진행 중인 퀘스트 다음 스텝 강제 실행",
            "현재 진행 중인 퀘스트 이전 스텝 강제 실행",
            "특정 퀘스트 강제 실행",
            "특정 ID 퀘스트 골카운트 n 수치로 실행"
        ],
        "아이템 및 보상 생성 관련": [
            "아이템 생성",
            "아바타 아이템 생성",
            "탈것 생성",
            "정령 생성",
            "무기소울 생성",
            "아스터 생성",
            "정령 즐겨찾기",
            "정령 즐겨찾기 해제",
            "강화된 아이템 생성",
            "귀속 여부에 따른 아이템 생성",
            "아이템 보상 드랍 FX Trail 속도",
            "커런시 획득"
        ],
        "아이템 강화 및 합성 관련": [
            "아이템 강화",
            "아이템 하락 강화",
            "합성",
            "확정 - 교체",
            "자동 합성",
            "실패누적보상"
        ],
        "퀘스트 조작 관련": [
            "퀘스트 몬스터킬",
            "일일 의뢰 초기화"
        ],
        "경험치 및 성장 관련": [
            "경험치 증가",
            "스킬 획득",
            "길드 경험치 설정",
            "폴른 포인트 초기화"
        ],
        "테스트 및 디버깅 관련": [
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
        ],
        "설정": [
            "게임 창 선택"
        ]
    }
    
    # 심플한 사이드바 메뉴 구성
    with st.sidebar:
        st.title("게임 치트 자동화")
        st.markdown("---")
        
        # 카테고리 탭
        st.subheader("메뉴")
        
        # 각 카테고리 버튼
        for category in categories:
            # 카테고리 버튼
            if st.button(category, key=f"cat_{category}", use_container_width=True, 
                        help=f"{category} 메뉴 선택"):
                st.session_state.current_category = category
                st.session_state.current_cheat = None
                st.session_state.expanded_categories = {}  # 모든 확장 상태 초기화
                st.session_state.expanded_categories[category] = True  # 현재 카테고리만 확장
                st.experimental_rerun()
        
        # 현재 선택된 카테고리에 대한 서브메뉴 표시
        if st.session_state.current_category in cheat_structure:
            st.markdown("---")
            st.markdown(f"#### {st.session_state.current_category}")
            
            # 서브메뉴 표시
            cheats = cheat_structure[st.session_state.current_category]
            for cheat in cheats:
                if st.button(cheat, key=f"cheat_{cheat}", use_container_width=True):
                    st.session_state.current_cheat = cheat
                    st.experimental_rerun()
        
        # 설정 섹션
        st.markdown("---")
        if st.button("설정", use_container_width=True, key="settings_button"):
            st.session_state.current_category = "설정"
            st.session_state.current_cheat = "게임 창 선택"
            st.experimental_rerun()
    
    # 메인 콘텐츠 영역
    st.write("## 게임 치트 자동화 도구")
    st.write("왼쪽 사이드바에서 원하는 기능을 선택하세요.")
    
    if st.session_state.current_category == "설정":
            # 윈도우 관리자 초기화
            window_manager = WindowManager()
            windows = window_manager.get_windows()
            
            if not windows:
                st.error("활성화된 윈도우가 없습니다.")
            else:
                # 운영체제 정보 표시
                system_type = platform.system()
                st.caption(f"현재 운영체제: {system_type}")
                
                # 시뮬레이션 모드 관련 정보 및 옵션
                if window_manager.simulation_mode:
                    if platform.system() == 'Windows':
                        st.warning("윈도우 관리가 시뮬레이션 모드로 실행 중입니다.")
                        st.code("pip install pygetwindow==0.0.9", language="bash")
                        st.info("명령어를 실행한 후 프로그램을 다시 시작하세요.")
                    elif platform.system() == 'Linux':
                        st.warning("리눅스 환경에서는 시뮬레이션 모드로만 실행됩니다.")
                
                # 게임 창이 아직 확정되지 않은 경우, 선택 UI 표시
                if not st.session_state.window_confirmed:
                    # 창 선택 UI
                    selected_window = st.selectbox(
                        "게임 창을 선택하세요:",
                        windows
                    )
                    
                    # 직접 입력 옵션 추가
                    use_custom_window = st.checkbox("직접 창 이름 입력하기")
                    
                    if use_custom_window:
                        custom_window = st.text_input(
                            "창 이름을 직접 입력하세요:", 
                            placeholder="예: 게임 클라이언트", 
                            value=selected_window if selected_window else ""
                        )
                        if custom_window:
                            selected_window = custom_window
                    
                    # 확인 버튼
                    if st.button("창 선택 확인", key="confirm_window"):
                        if not selected_window:
                            st.error("창을 선택하거나 이름을 입력해주세요.")
                        else:
                            st.session_state.window_confirmed = True
                            st.session_state.selected_window = selected_window
                            
                            # 창 활성화 시도 (시뮬레이션 모드가 아닐 때만)
                            if not window_manager.simulation_mode:
                                if window_manager.activate_window(selected_window):
                                    st.success(f"'{selected_window}' 창을 활성화했습니다.")
                                else:
                                    st.warning(f"'{selected_window}' 창 활성화에 실패했습니다. 수동으로 창을 선택해주세요.")
                            
                            st.experimental_rerun()  # UI 업데이트를 위해 페이지 리로드
                else:
                    # 이미 확정된 게임 창 정보 표시
                    st.success(f"게임 창: '{st.session_state.selected_window}' 적용됨")
                    
                    # 변경 버튼 추가
                    if st.button("변경", key="change_window"):
                        st.session_state.window_confirmed = False
                        st.experimental_rerun()  # UI 업데이트를 위해 페이지 리로드
    
    # 치트 정보 저장 (치트명, 치트키, 사용예시, 추가정보)
    cheat_info = {
        # 🔥 전투 및 공격 관련
        "유닛 수동 공격": {
            "코드": "GT.UNIT_ATTACK {SKILLID}",
            "예시": "GT.UNIT_ATTACK 1100000",
            "정보": ""
        },
        "HP 절반 만들기": {
            "코드": "GT.DMG_SELF",
            "예시": "GT.DMG_SELF",
            "정보": "자기 자신에게 50프로의 데미지를 입힘"
        },
        "HP, MP 전체 회복": {
            "코드": "GT.RECOVERY_ALL",
            "예시": "GT.RECOVERY_ALL",
            "정보": ""
        },
        "PC 무적(피격 면역) 처리": {
            "코드": "GT.SET_INVIN {VALUE}",
            "예시": "GT.SET_INVIN 1",
            "정보": "1: 무적 상태\n0: 무적 해제"
        },
        "대미지 증가 실행": {
            "코드": "GT.ABS_DAMAGE {VALUE}",
            "예시": "GT.ABS_DAMAGE 1000",
            "정보": "0: 대미지 절대 값 적용 해제\n0 > :: 해당 수치로 대미지 적용(크리X, 미스X)"
        },
        "PC 스킬 쿨타임 미적용 + 마나 소모 0": {
            "코드": "GT.SKILL_NODELAY {VALUE}",
            "예시": "GT.SKILL_NODELAY 1",
            "정보": "1: 쿨타임 적용 안함\n0: 쿨타임 적용함"
        },
        "반격 (활성 / 비활성)": {
            "코드": "GT.HitBack {숫자값}",
            "예시": "GT.HitBack 1 → 활성\nGT.HitBack 0 → 비활성\nGT.HitBack → 토글 방식 (활성 / 비활성)",
            "정보": "플레이어 반격 (활성 / 비활성)\n기본값 (활성)\n환경설정에서 조정할 수 있게 바뀌어서 치트키를 통해 환경설정 값이 변경되도록 바꿈"
        },
        "스킬 사용 (통보 / 확인)": {
            "코드": "GT.SkillApproved {숫자값}",
            "예시": "GT.SkillApproved 1 → 통보\nGT.SkillApproved 0 → 확인\nGT.SkillApproved → 토글 방식 (통보 / 확인)",
            "정보": "플레이어 스킬 사용 (서버에 통보 / 서버로 부터 확인 받은 후 사용)\n기본값 (서버로 부터 확인 받은 후 사용)"
        },
        "우클릭 이동 (활성 / 비활성)": {
            "코드": "GT.MoveFromServerByRightClick {숫자값}",
            "예시": "GT.MoveFromServerByRightClick 1 → 활성\nGT.MoveFromServerByRightClick 0 → 비활성\nGT.MoveF…tClick → 토글 방식 (활성 / 비활성)",
            "정보": "마우스 우클릭시 그 위치까지 서버로부터 받은 패킷으로 이동 (활성 / 비활성)\n기본값 (비활성)"
        },
        "서버를 통한 움직임 디버그 표시 (표시 / 비표시)": {
            "코드": "GT.MoveFromServerDebug {숫자값}",
            "예시": "GT.MoveFromServerDebug 1 → 표시\nGT.MoveFromServerDebug 0 → 비표시\nGT.MoveF…rDebug → 토글 방식 (표시 / 비표시)",
            "정보": "서버를 통해 받은 스킬 사용, 스킬 완료, 이동 관련 패킷 화면상에 디버그 구체로 표시 (표시 /비표시)\n기본값 (비표시)"
        },
        "스킬 사용, 우클릭 이동, 서버를 통한 움직임 디버그 표시 한번에 (활성 / 비활성)": {
            "코드": "GT.MoveApprovedAll {숫자값}",
            "예시": "GT.MoveApprovedAll 1 → 활성\nGT.MoveApprovedAll 0 → 비활성\nGT.MoveA…dAll → 토글 방식 (활성 / 비활성)",
            "정보": "스킬 사용 (GT.SkillApproved), 우클릭 이동 (GT.MoveFromServerByRightClick), 서버를 통한 움직임 디버그 표시 (GT.MoveFromServerDebug) 한번에 (활성 / 비활성)\n토글 형식일때 스킬 사용 (GT.SkillApproved) 가 기준"
        },
        "플레이어 위치 클립보드로 복사": {
            "코드": "GT.Loc",
            "예시": "",
            "정보": "플레이어의 위치를 클립보드에 복사한다."
        },
        "BASE 이동": {
            "코드": "GT.SC GO_HOME",
            "예시": "GT.SC GO_HOME",
            "정보": "현재 대륙의 BASE(마을)로 이동 합니다."
        },
        
        # 🎯 이동 및 위치 조작 관련
        "유닛 좌표 이동": {
            "코드": "GT.WARP_TO_COOR {X} {Y} {Z}",
            "예시": "GT.WARP_TO_COOR 153722 60780 1739",
            "정보": "좌표 목록\n메튼 농장(마을앞): 153722,60780,1739\n후르츠 빌리지(마을앞): 147524,43515,2363\n마나마을 분수대: 163632,39279,3958"
        },
        "NPC 좌표로 이동": {
            "코드": "GT.WARP_TO_NPC {NPC_ID}",
            "예시": "GT.WARP_TO_NPC 1001030",
            "정보": "해당 npc가 있는 곳으로 강제 이동"
        },
        "PROP 좌표로 이동": {
            "코드": "GT.WARP_TO_PROP {PROP_ID}",
            "예시": "GT.WARP_TO_PROP 1000026",
            "정보": ""
        },
        "퀘스트 목표 지역으로 이동": {
            "코드": "GT.WARP_TO_QUEST {QUEST_ID}",
            "예시": "GT.WARP_TO_QUEST 1000026",
            "정보": "CONTINENT_KILL, ANY_KILL 타입은 지원 하지 않습니다."
        },
        "현재 진행 중인 퀘스트 다음 스텝 강제 실행": {
            "코드": "GT.SC NEXT_QUEST",
            "예시": "GT.SC NEXT_QUEST",
            "정보": "메인 퀘스트만 가능합니다."
        },
        "현재 진행 중인 퀘스트 이전 스텝 강제 실행": {
            "코드": "GT.SC PREV_QUEST",
            "예시": "GT.SC PREV_QUEST",
            "정보": "메인 퀘스트만 가능합니다."
        },
        "특정 퀘스트 강제 실행": {
            "코드": "GT.SC OPEN_QUEST {QUEST_ID} {STEP}",
            "예시": "GT.SC OPEN_QUEST 100200032 1",
            "정보": "메인 퀘스트만 가능합니다."
        },
        "특정 ID 퀘스트 골카운트 n 수치로 실행": {
            "코드": "GT.SC QUEST_GOAL {QuestID} {GoalCount}",
            "예시": "GT.SC QUEST_GOAL 1000001 10",
            "정보": "메인 퀘스트만 가능합니다."
        },
        
        # 🎁 아이템 및 보상 생성 관련
        "아이템 생성": {
            "코드": "GT.CREATE_ITEM {ITEM_ID} {ITEM_CNT}",
            "예시": "GT.CREATE_ITEM 900090001 100",
            "정보": ""
        },
        "아바타 아이템 생성": {
            "코드": "GT.CREATE_AVATAR",
            "예시": "GT.CREATE_AVATAR 900090001",
            "정보": ""
        },
        "탈것 생성": {
            "코드": "GT.SC CREATE_VEHICLE {VEHICLE_ID}",
            "예시": "GT.SC CREATE_VEHICLE 10001",
            "정보": ""
        },
        "정령 생성": {
            "코드": "GT.SC CREATE_SPIRIT {SPIRIT_ID}",
            "예시": "GT.SC CREATE_SPIRIT 10000",
            "정보": ""
        },
        "정령 즐겨찾기": {
            "코드": "GT.SC SPIRIT_BOOKMARK_SET {SPIRIT_COLLECTION_ID}",
            "예시": "GT.SC SPIRIT_BOOKMARK_SET 100002",
            "정보": ""
        },
        "정령 즐겨찾기 해제": {
            "코드": "GT.SC SPIRIT_BOOKMARK_DELETE {SPIRIT_COLLECTION_ID}",
            "예시": "GT.SC SPIRIT_BOOKMARK_DELETE 100002",
            "정보": ""
        },
        "무기소울 생성": {
            "코드": "GT.SC CREATE_WEAPONSOUL {WEAPONSOUL_ID}",
            "예시": "GT.SC CREATE_WEAPONSOUL 1000",
            "정보": ""
        },
        "아스터 생성": {
            "코드": "GT.SC CREATE_ASTER {ASTER_ID}",
            "예시": "GT.SC CREATE_ASTER 1000",
            "정보": ""
        },
        "강화된 아이템 생성": {
            "코드": "GT.SC CREATE_ITEM_WITH_LEVEL {아이템ID} {개수} {레벨}",
            "예시": "GT.SC CREATE_ITEM_WITH_LEVEL 903003000 1 20",
            "정보": ""
        },
        "귀속 여부에 따른 아이템 생성": {
            "코드": "GT.SC CREATE_ITEM_WITH_BELONGING {아이템ID} {개수} {귀속 여부}",
            "예시": "GT.SC CREATE_ITEM_WITH_BELONGING 00090001 1 CHARACTER",
            "정보": ""
        },
        "아이템 보상 드랍 FX Trail 속도": {
            "코드": "di.Speed {값}",
            "예시": "di.Speed 20",
            "정보": "콘솔 커맨드 명령어"
        },
        "커런시 획득": {
            "코드": "GT.ADD_CURRENCY {재화타입} {수량}",
            "예시": "",
            "정보": "커런시 획득"
        },
        
        # 📈 아이템 강화 및 합성 관련
        "아이템 강화": {
            "코드": "GT.SC ITEM_UPGRADE {강화재료 아이템ID} {강화목표단계} {강화시킬 아이템 시퀀스1} {강화시킬 아이템 시퀀스2}",
            "예시": "GT.SC ITEM_UPGRADE 900090020 8 18521",
            "정보": "아규먼트 3개 이상 필요 / 강화 재료 아이템을 보유하고 있지 않아도 실행 가능(하지만 강화 재료 아이디는 기재 필요)"
        },
        "아이템 하락 강화": {
            "코드": "GT.SC ITEM_DOWNGRADE {강화재료 아이템ID} {강화목표단계} {강화시킬 아이템 시퀀스1} {강화시킬 아이템 시퀀스2}",
            "예시": "GT.SC ITEM_DOWNGRADE 900090020 8 18521 18522",
            "정보": "아규먼트 3개 이상 필요"
        },
        "합성": {
            "코드": "GT.SC COMPOSE {아이템타입} {합성할 아이템ID} {합성할 아이템ID} {합성할 아이템ID} {합성할 아이템ID}",
            "예시": "GT.SC COMPOSE AVATAR 110318000 10318000 110318000 0",
            "정보": ""
        },
        "확정 - 교체": {
            "코드": "GT.SC COMPOSE_CHANGE {아이템 타입} {교체할(교체전) 아이템 ID}",
            "예시": "GT.SC COMPOSE_CHANGE AVATAR 110518000",
            "정보": ""
        },
        "자동 합성": {
            "코드": "GT.SC COMPOSE_AUTO {아이템 타입} {목표등급} {선택클래스}",
            "예시": "GT.SC COMPOSE_AUTO AVATAR MYTH ALL",
            "정보": ""
        },
        "실패누적보상": {
            "코드": "GT.SC COMPOSE_FAIL_REWARD {아이템 타입} {보상받을 등급}",
            "예시": "GT.SC COMPOSE_FAIL_REWARD AVATAR LEGEND",
            "정보": ""
        },
        
        # 📚 퀘스트 조작 관련
        "퀘스트 몬스터킬": {
            "코드": "GT.QMOB_KILL {MOB_ID}",
            "예시": "GT.QMOB_KILL 1000001",
            "정보": ""
        },
        "일일 의뢰 초기화": {
            "코드": "GT.SC RESET_DAILY_QUEST_CNT",
            "예시": "GT.SC RESET_DAILY_QUEST_CNT",
            "정보": "일일 의뢰 초기화"
        },
        
        # 🎓 경험치 및 성장 관련
        "경험치 증가": {
            "코드": "GT.ADD_EXP {VALUE}",
            "예시": "GT.ADD_EXP 10000",
            "정보": "VALUE 만큼 경험치 추가"
        },
        "스킬 획득": {
            "코드": "GT.GetSkill {DATA_CLASS_SKILL.ID}",
            "예시": "GT.GetSkill 6100003",
            "정보": "해당 ID의 스킬 획득\n※ 치트키 사용 후 재접속을 해야 적용됩니다.\n※ 서버와는 무관한 치트입니다. 서버사이드에서는 스킬 사용이 안됩니다."
        },
        "길드 경험치 설정": {
            "코드": "GT.SC CHEAT_ADD_GUILD_EXP {SetValue} {GuildName}",
            "예시": "GT.SC CHEAT_ADD_GUILD_EXP 5000 길드이름",
            "정보": "길드 경험치를 추가하는 것이 아니라 설정함"
        },
        "폴른 포인트 초기화": {
            "코드": "GT.SC SET_FALLEN_ZERO",
            "예시": "GT.SC SET_FALLEN_ZERO",
            "정보": "폴른 포인트를 0으로 지정"
        },
        
        # 🛠️ 테스트 및 디버깅 관련
        "테스트 모드 변경": {
            "코드": "GT.TestMode {숫자값}",
            "예시": "GT.TestMode 1 → 상태이상 테스트 활성\nGT.TestMode 2 → 충돌 테스트 활성\nGT.TestMode 3 → 파티원 어시스트 테스트 활성\nGT.TestMode 0 → 모두 비활성",
            "정보": "테스트 모드 변경\n기본값 (비활성)"
        },
        "상태이상 테스트 (활성 / 비활성)": {
            "코드": "GT.AbnormalTest {숫자값}",
            "예시": "GT.AbnormalTest 1 → 활성\nGT.AbnormalTest 0 → 비활성\nGT.AbnormalTest → 토글 방식 (활성 / 비활성)",
            "정보": "상태이상 테스트 모드 (활성 / 비활성)\n기본값 (비활성)\n활성화 후 Ctrl+1 기절 활성 / 비활성\n활성화 후 Ctrl+2 빙결 활성 / 비활성\n활성화 후 Ctrl+3 석화 활성 / 비활성\n활성화 후 Ctrl+4 화상 활성 / 비활성\n활성화 후 Ctrl+5 둔화 활성 / 비활성\n활성화 후 Ctrl+6 수면 활성 / 비활성\n활성화 후 Ctrl+7 넉백 활성 / 비활성\n활성화 후 Ctrl+8 넘어짐 활성 / 비활성\n활성화 후 Ctrl+9 위의 상태이상 모두 회복 + HP, MP 회복 + 다이아 100 획득\n(서버에선 플레이어의 상태이상 상황을 알 수 없으니 실제와 완전히 동일할순 없음)"
        },
        "충돌 테스트 (활성 / 비활성)": {
            "코드": "GT.CollisionTest {숫자값}",
            "예시": "GT.CollisionTest 1 → 활성\nGT.CollisionTest 0 → 비활성\nGT.CollisionTest → 토글 방식 (활성 / 비활성)",
            "정보": "충돌 테스트 모드 (활성 / 비활성)\n기본값 (비활성)\n활성화 후 Ctrl+1 내 플레이어와 모두간 충돌 활성\n활성화 후 Ctrl+2 내 플레이어와 모두간 충돌 비활성\n활성화 후 Ctrl+7 디버그 표시 활성\n활성화 후 Ctrl+8 디버그 표시 비활성\n활성화 후 Ctrl+9 충돌 설정 서버로 부터 받은 값으로 초기화\n(서버에선 플레이어의 상태이상 상황을 알 수 없으니 실제와 완전히 동일할 순 없음)"
        },
        "파티원 어시스트 테스트 (활성 / 비활성)": {
            "코드": "GT.TestMode {숫자값}",
            "예시": "GT.TestMode 3 → 활성\nGT.TestMode 0 → 비활성",
            "정보": "파티원 어시스트 테스트 (활성 / 비활성)\n기본값 (비활성)\n활성화 후 Ctrl+7 어시스트 관련 설정 값, 상태값 보기\n활성화 후 Ctrl+8 PVP 설정 - ON\n활성화 후 Ctrl+9 PVP 설정 - OFF\n활성화 후 Ctrl+4 자동 사냥 설정 - OFF - 모두 끄기\n활성화 후 Ctrl+5 자동 사냥 설정 - ON -타겟 어시스트\n활성화 후 Ctrl+6 자동 사냥 설정 - ON -주변 자동 사냥\n활성화 후 Ctrl+1 PVP 어시스트 - 활성\n활성화 후 Ctrl+2 자동 사냥 - 타겟 어시스트 - 활성 / 비활성\n활성화 후 Ctrl+3 자동 사냥 - 주변 자동사냥 - 활성 / 비활성"
        },
        "배틀로얄 참가 최대 인원 변경": {
            "코드": "GT.SC SET_BRSTART_CNT {count}",
            "예시": "GT.SC SET_BRSTART_CNT 2",
            "정보": "2명이 입장하면 배틀로얄이 시작됨"
        },
        "자살": {
            "코드": "GT.SELF_KILL",
            "예시": "GT.SELF_KILL",
            "정보": ""
        },
        "가방 비우기": {
            "코드": "GT.CLEAR_INVEN",
            "예시": "GT.CLEAR_INVEN",
            "정보": "장비 프리셋에 등록된 아이템을 제외하고 모든 아이템 삭제"
        },
        "유닛 속도 변경": {
            "코드": "GT.CHANGE_MVSPD {VALUE}",
            "예시": "GT.CHANGE_MVSPD 1000",
            "정보": ""
        },
        "서버 치트키 직접 실행": {
            "코드": "GT.SC {\"GT.\"을 제외한 치트명령어}",
            "예시": "GT.SC SELF_KILL\nGT.SC ABS_DAMAGE 1000",
            "정보": "치트키를 서버에 직접 전송합니다.\n클라이언트용 치트키는 동작하지 않으며 기존 치트키에서 \"GT.\"을 제외하고 입력해야 합니다.\n예를 들면 \"GT.ABS_DAMAGE 1000\"는 \"GT.SC ABS_DAMAGE 1000\"이 됩니다."
        },
        "치트창 열기": {
            "코드": "GT.OpenCheatUI",
            "예시": "",
            "정보": "치트창을 엽니다."
        }
    }
    
    # 치트 코드 매핑 생성 (실제 실행에 사용)
    cheat_codes = {name: info["코드"] for name, info in cheat_info.items()}
    
    # 테스트 모드에 대한 특별 매핑
    test_mode_codes = {
        "1. 상태이상 테스트 활성": "GT.TestMode 1",
        "2. 충돌 테스트 활성": "GT.TestMode 2",
        "3. 파티원 어시스트 테스트 활성": "GT.TestMode 3", 
        "0. 모두 비활성": "GT.TestMode 0"
    }
    
# 새 UI를 사용하는지 여부를 확인하는 플래그
    use_new_ui = True
    
    # 테스트 모드 변경을 위한 추가 선택 옵션 정의 (전역 변수)
    if 'test_mode_options' not in globals():
        global test_mode_options
        test_mode_options = None
    
    # 기존 코드와의 호환성 유지
    if use_new_ui and st.session_state.current_cheat is not None:
        # 이전 코드와의 호환성을 위한 변수 설정
        selected_cheat = st.session_state.current_cheat 
        selected_category = st.session_state.current_category
        
        # 테스트 모드 치트에 대한 처리
        if st.session_state.current_category == "🛠️ 테스트 및 디버깅 관련" and st.session_state.current_cheat == "테스트 모드 변경":
            test_mode_options = "1. 상태이상 테스트 활성"  # 기본값
    else:
        # 기존 인터페이스 사용 시 필요한 변수들
        selected_category = st.selectbox(
            "카테고리를 선택하세요:",
            list(cheat_structure.keys()),
            key="category_select_legacy"
        )
        
        selected_cheat = st.selectbox(
            "기능을 선택하세요:",
            cheat_structure[selected_category],
            key="cheat_select_legacy"
        )
    
    # 새 UI 레이아웃
    if use_new_ui:
        with col2:
            # 선택된 치트가 없거나 설정 화면이면 홈 화면 표시
            if st.session_state.current_cheat is None:
                if st.session_state.current_category is None:
                    # 홈 화면
                    st.markdown("<h1 style='text-align: center;'>게임 치트 자동화 프로그램</h1>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center;'>왼쪽 메뉴에서 카테고리와 기능을 선택하세요</p>", unsafe_allow_html=True)
                    
                    # 간단한 통계와 시작 가이드
                    col_a, col_b = st.columns(2)
                    
                    # 좌측 카드
                    with col_a:
                        with st.container():
                            st.markdown("""
                            <div class='stCard'>
                                <h3>📚 시작하기</h3>
                                <p>1. <b>게임 창 선택</b>: 오른쪽 상단 "설정" 탭에서 게임 창을 선택하세요.</p>
                                <p>2. <b>카테고리 선택</b>: 왼쪽 카테고리 목록에서 원하는 치트 종류를 선택하세요.</p>
                                <p>3. <b>기능 사용</b>: 세부 기능을 선택하고 필요한 정보를 입력한 후 실행하세요.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # 우측 카드
                    with col_b:
                        with st.container():
                            st.markdown("""
                            <div class='stCard'>
                                <h3>💡 자주 사용하는 기능</h3>
                                <p>• <b>아이템 생성</b>: 엑셀 데이터를 활용한 아이템 필터링 및 생성</p>
                                <p>• <b>이동 조작</b>: 지정한 좌표로 캐릭터 이동</p>
                                <p>• <b>전투 능력</b>: 무적, 대미지 증가 등 전투 관련 치트</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # 게임 창 상태 표시
                    st.markdown("<hr>", unsafe_allow_html=True)
                    
                    # 창 선택 상태
                    window_manager = WindowManager()
                    
                    if st.session_state.window_confirmed:
                        st.success(f"✅ 게임 창 '{st.session_state.selected_window}'이(가) 선택되었습니다.")
                    else:
                        st.warning("⚠️ 게임 창이 선택되지 않았습니다. '설정' 탭에서 창을 선택해주세요.")
                        
                        if window_manager.simulation_mode:
                            if platform.system() == 'Windows':
                                st.error("윈도우 관리가 시뮬레이션 모드로 실행 중입니다.")
                                with st.expander("해결 방법"):
                                    st.code("pip install pygetwindow==0.0.9", language="bash")
                                    st.info("위 명령어를 실행한 후 프로그램을 다시 시작하세요.")
                            elif platform.system() == 'Linux':
                                st.error("리눅스 환경에서는 시뮬레이션 모드로만 실행됩니다.")
                else:
                    # 카테고리 헤더 표시
                    st.markdown(f"<h2>{st.session_state.current_category}</h2>", unsafe_allow_html=True)
                    st.markdown("<p>왼쪽 메뉴에서 세부 기능을 선택하세요</p>", unsafe_allow_html=True)
                    
                    # 카테고리 설명
                    category_descriptions = {
                        "🔥 전투 및 공격 관련": "캐릭터의 전투 능력을 강화하고 공격 관련 기능을 조작합니다.",
                        "🎯 이동 및 위치 조작 관련": "게임 내 캐릭터의 이동 및 위치를 조작합니다.",
                        "🎁 아이템 및 보상 생성 관련": "다양한 아이템과 보상을 생성합니다.",
                        "📈 아이템 강화 및 합성 관련": "아이템 강화와 합성 관련 기능을 제공합니다.",
                        "📚 퀘스트 조작 관련": "게임 내 퀘스트를 조작하고 관리합니다.",
                        "🎓 경험치 및 성장 관련": "캐릭터의 경험치와 성장 관련 기능을 제공합니다.",
                        "🛠️ 테스트 및 디버깅 관련": "게임 테스트와 디버깅을 위한 기능을 제공합니다."
                    }
                    
                    # 카테고리 설명 표시
                    if st.session_state.current_category in category_descriptions:
                        st.info(category_descriptions[st.session_state.current_category])
                    
                    # 카테고리 내 기능 리스트를 그리드로 표시
                    if st.session_state.current_category in cheat_structure:
                        cheats = cheat_structure[st.session_state.current_category]
                        
                        # 3열 그리드 레이아웃
                        cols = st.columns(3)
                        
                        for i, cheat in enumerate(cheats):
                            with cols[i % 3]:
                                if st.button(f"🔹 {cheat}", key=f"grid_{cheat}", use_container_width=True):
                                    st.session_state.current_cheat = cheat
                                    st.experimental_rerun()
            else:
                # 선택된 치트 표시
                st.markdown(f"<h2>{st.session_state.current_cheat}</h2>", unsafe_allow_html=True)
                
                # 뒤로가기 버튼
                if st.button("◀️ 뒤로"):
                    st.session_state.current_cheat = None
                    st.experimental_rerun()
                    
                # 치트 정보 표시
                if st.session_state.current_cheat in cheat_info:
                    info = cheat_info[st.session_state.current_cheat]
                    
                    # 정보 카드
                    with st.container():
                        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
                        st.markdown("<h3>치트 정보</h3>", unsafe_allow_html=True)
                        
                        if info["예시"]:
                            st.code(info["예시"], language="bash")
                        if info["정보"]:
                            st.info(info["정보"])
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # 테스트 모드 변경을 위한 추가 선택 옵션 (전역 변수 사용)
                if st.session_state.current_category == "🛠️ 테스트 및 디버깅 관련" and st.session_state.current_cheat == "테스트 모드 변경":
                    test_mode_options = st.selectbox(
                        "테스트 모드 선택:",
                        [
                            "1. 상태이상 테스트 활성",
                            "2. 충돌 테스트 활성",
                            "3. 파티원 어시스트 테스트 활성",
                            "0. 모두 비활성"
                        ]
                    )
    
    # 선택된 치트에 추가 입력이 필요한지 확인
    additional_params = {}
    
    # 치트 선택에 따른 추가 파라미터 입력 필드 설정
    with st.container():
        if selected_cheat == "퀘스트 몬스터킬":
            mob_id = st.text_input("몬스터 ID를 입력하세요:", "1000001")
            additional_params["MOB_ID"] = mob_id
            
        elif selected_cheat == "아이템 생성":
            # 장비 검색 인터페이스 추가
            search_method = st.radio("아이템 생성 방법 선택:", ["필터", "장비 검색", "직접 ID 입력"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                item_id = st.text_input("아이템 ID를 입력하세요:", "900090001")
            elif search_method == "장비 검색":
                # 검색 인터페이스
                st.subheader("아이템 검색", divider=True)
                
                # 검색입력과 버튼 배치
                search_col1, search_col2 = st.columns([3, 1])
                with search_col1:
                    search_query = st.text_input("이름으로 아이템 검색 (키워드 입력):", "")
                with search_col2:
                    search_button = st.button("검색")
                
                # 검색 결과 처리
                search_results = []
                if search_query and (search_button or search_query.strip() != ""):
                    search_results = search_items_by_name(search_query)
                    if search_results:
                        st.success(f"'{search_query}' 검색 결과: {len(search_results)}개 아이템 발견")
                    else:
                        st.warning(f"'{search_query}' 검색 결과가 없습니다.")
                
                # 아이템 표시
                display_items = []
                if search_query and (search_button or search_query.strip() != "") and search_results:
                    display_items = search_results
                    st.subheader("검색 결과")
                else:
                    # 기본 아이템 몇 개 표시
                    display_items = filter_items("모두", "모두", "모두")[:30]
                    st.subheader("아이템 목록")
                
                if len(display_items) == 0:
                    st.warning("표시할 아이템이 없습니다.")
                    st.info("다른 검색어를 입력하거나 필터 조건을 변경해보세요.")
                
                if display_items:
                    # 등급별 색상 표시를 위한 함수
                    def format_item(item):
                        # Excel 컬럼 매핑: Grade -> grade, Name -> name, Id -> id
                        grade = item.get('Grade', item.get('grade', 'N/A'))
                        name = item.get('Name', item.get('name', 'Unknown'))
                        id_value = item.get('Id', item.get('id', 'N/A'))
                        job_info = item.get('job', '공용')
                        job_info = job_info if job_info != "공용" else "공용"
                        return f"[{grade}] {name} - {job_info} ({id_value})"
                    
                    # 아이템 선택 UI
                    selected_item = st.selectbox(
                        "아이템 선택:",
                        options=display_items,
                        format_func=format_item
                    )
                    
                    item_id = selected_item.get("Id", selected_item.get("id", ""))
                    
                    # 선택된 아이템 정보 표시
                    grade = selected_item.get('Grade', selected_item.get('grade', 'COMMON'))
                    grade_color = GRADE_COLORS.get(grade, "gray")
                    
                    # 엑셀 컬럼 매핑
                    name = selected_item.get('Name', selected_item.get('name', 'Unknown'))
                    id_value = selected_item.get('Id', selected_item.get('id', 'N/A'))
                    job = selected_item.get('job', '공용')
                    part = selected_item.get('part', 'N/A')
                    
                    st.markdown(f"""
                    <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                        <p><strong>아이템 ID:</strong> {id_value}</p>
                        <p><strong>등급:</strong> {grade}</p>
                        <p><strong>직업:</strong> {job}</p>
                        <p><strong>부위:</strong> {part}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("조건에 맞는 아이템이 없습니다.")
                    item_id = ""
            else:  # 필터
                st.subheader("아이템 필터", divider=True)
                
                # JSON 데이터 로드
                items_data = load_data_from_json("data/items.json")
                
                if not items_data:
                    st.warning("아이템 데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
                    item_id = ""
                else:
                    # 필터링 인터페이스
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        grade_filter = st.selectbox("등급 선택:", ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"])
                    
                    with col2:
                        # Excel 파일(Items.xlsx)에서 타입 목록 추출
                        type_options = ["모두"]
                        
                        # items_data에서 Type 키 확인
                        type_keys = ['Type', 'type', 'TYPE', 'item_type', 'ItemType']
                        found_key = None
                        
                        # Items.xlsx 엑셀 파일 직접 로딩하여 Type 값 추출
                        # data/items.json 경로로 전달하면 내부에서 excel_data/Items.xlsx로 변환하고 없으면 생성함
                        excel_items = load_data_from_json("data/items.json")
                        
                        if excel_items and len(excel_items) > 0:
                            # 어떤 키가 있는지 확인
                            for key in type_keys:
                                if key in excel_items[0]:
                                    found_key = key
                                    break
                            
                            # 해당 키의 모든 고유 값 추출
                            if found_key:
                                type_values = set()
                                for item in excel_items:
                                    type_value = item.get(found_key, '')
                                    if type_value and str(type_value).strip():
                                        type_values.add(str(type_value).strip())
                                
                                # 타입 옵션 추가
                                type_options.extend(sorted(list(type_values)))
                            else:
                                # 기본 타입 옵션
                                type_options.extend(["무기", "방어구", "장신구", "소비", "스킬북", "상자", "제작서", "재료", "퀘스트", "기타"])
                        else:
                            # 엑셀 파일 로드 실패 시 JSON 데이터에서 추출 시도 (기존 방식 유지)
                            if items_data and len(items_data) > 0:
                                for key in type_keys:
                                    if key in items_data[0]:
                                        found_key = key
                                        break
                            
                            if found_key:
                                type_values = set()
                                for item in items_data:
                                    type_value = item.get(found_key, '')
                                    if type_value and str(type_value).strip():
                                        type_values.add(str(type_value).strip())
                                
                                # 타입 옵션 추가
                                type_options.extend(sorted(list(type_values)))
                            else:
                                # 기본 타입 옵션
                                type_options.extend(["무기", "방어구", "장신구", "소비", "스킬북", "상자", "제작서", "재료", "퀘스트", "기타"])
                        
                        type_filter = st.selectbox("타입 선택:", type_options)
                    
                    # 필터 적용
                    filters = {
                        "grade": grade_filter,
                        "type": type_filter
                    }
                    
                    # RAG 시스템으로 필터링
                    filtered_items = filter_data_with_rag(items_data, filters)
                    
                    if filtered_items:
                        st.success(f"필터링 결과: {len(filtered_items)}개 아이템")
                        
                        # 아이템 선택 UI
                        def format_item(item):
                            # Excel 컬럼 매핑: Grade -> grade, Name -> name, Id -> id
                            grade = item.get('Grade', item.get('grade', 'N/A'))
                            name = item.get('Name', item.get('name', 'Unknown'))
                            id_value = item.get('Id', item.get('id', 'N/A'))
                            job_info = item.get('char', item.get('job', '공용'))
                            job_info = job_info if job_info != "공용" else "공용"
                            item_type = item.get('Type', item.get('type', item.get('TYPE', '')))
                            
                            # 타입 정보가 있을 경우 표시
                            if item_type:
                                return f"[{grade}] {name} - {job_info} - {item_type} ({id_value})"
                            else:
                                return f"[{grade}] {name} - {job_info} ({id_value})"
                        
                        selected_item = st.selectbox(
                            "아이템 선택:",
                            options=filtered_items,
                            format_func=format_item
                        )
                        
                        item_id = selected_item.get("Id", selected_item.get("id", ""))
                        
                        # 선택된 아이템 정보 표시
                        grade = selected_item.get('Grade', selected_item.get('grade', 'COMMON'))
                        grade_color = GRADE_COLORS.get(grade, "gray")
                        
                        # 엑셀 컬럼 매핑
                        name = selected_item.get('Name', selected_item.get('name', 'Unknown'))
                        id_value = selected_item.get('Id', selected_item.get('id', 'N/A'))
                        job = selected_item.get('char', selected_item.get('job', '공용'))
                        item_type = selected_item.get('Type', selected_item.get('type', selected_item.get('TYPE', 'N/A')))
                        
                        st.markdown(f"""
                        <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                            <p><strong>아이템 ID:</strong> {id_value}</p>
                            <p><strong>등급:</strong> {grade}</p>
                            <p><strong>직업:</strong> {job}</p>
                            <p><strong>타입:</strong> {item_type}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("조건에 맞는 아이템이 없습니다.")
                        item_id = ""
            
            # 개수 입력은 항상 표시
            item_cnt = st.text_input("생성할 개수를 입력하세요:", "1")
            additional_params["ITEM_ID"] = item_id
            additional_params["ITEM_CNT"] = item_cnt
            
        elif selected_cheat == "아바타 아이템 생성":
            search_method = st.radio("아바타 생성 방법 선택:", ["필터", "직접 ID 입력"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                avatar_id = st.text_input("아바타 ID를 입력하세요:", "900090001")
            else:  # 필터
                st.subheader("아바타 필터", divider=True)
                
                # JSON 데이터 로드
                avatars_data = load_data_from_json("data/avatars.json")
                
                if not avatars_data:
                    st.warning("아바타 데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
                    avatar_id = ""
                else:
                    # 필터링 인터페이스 - 2개 컬럼
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        grade_filter = st.selectbox("등급 선택:", ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"], key="avatar_grade")
                    
                    with col2:
                        job_filter = st.selectbox("직업 선택:", JOB_LIST, key="avatar_job")
                    
                    # 필터 적용
                    filters = {
                        "grade": grade_filter,
                        "job": job_filter
                    }
                    
                    # RAG 시스템으로 필터링
                    filtered_avatars = filter_data_with_rag(avatars_data, filters)
                    
                    # 검색 기능 추가
                    search_col1, search_col2 = st.columns([3, 1])
                    with search_col1:
                        search_query = st.text_input("이름으로 아바타 검색 (키워드 입력):", "", key="avatar_search")
                    with search_col2:
                        search_button = st.button("검색", key="avatar_search_btn")
                    
                    # 검색 결과 처리
                    if search_query and (search_button or search_query.strip() != ""):
                        search_results = []
                        query = search_query.lower()
                        for avatar in filtered_avatars:
                            if query in avatar.get("name", "").lower():
                                search_results.append(avatar)
                        
                        if search_results:
                            filtered_avatars = search_results
                            st.success(f"'{search_query}' 검색 결과: {len(filtered_avatars)}개 아바타 발견")
                        else:
                            st.warning(f"'{search_query}' 검색 결과가 없습니다.")
                    
                    if filtered_avatars:
                        st.success(f"필터링 결과: {len(filtered_avatars)}개 아바타")
                        
                        # 아바타 선택 UI
                        def format_avatar(item):
                            # 엑셀 파일과 매핑: Grade -> grade, Name -> name, Id -> id, char -> job
                            grade = item.get('Grade', item.get('grade', 'N/A'))
                            name = item.get('Name', item.get('name', 'Unknown'))
                            id_value = item.get('Id', item.get('id', 'N/A'))
                            job = item.get('char', item.get('job', 'N/A'))
                            
                            return f"[{grade}] {name} - {job} ({id_value})"
                        
                        selected_avatar = st.selectbox(
                            "아바타 선택:",
                            options=filtered_avatars,
                            format_func=format_avatar,
                            key="avatar_select"
                        )
                        
                        # 엑셀 파일과 매핑: Id -> id
                        avatar_id = selected_avatar.get("Id", selected_avatar.get("id", ""))
                        
                        # 선택된 아바타 정보 표시
                        grade = selected_avatar.get("Grade", selected_avatar.get("grade", "COMMON"))
                        grade_color = GRADE_COLORS.get(grade, "gray")
                        
                        # 엑셀 컬럼명에 맞게 매핑
                        name = selected_avatar.get('Name', selected_avatar.get('name', 'Unknown'))
                        id_value = selected_avatar.get('Id', selected_avatar.get('id', 'N/A'))
                        job = selected_avatar.get('char', selected_avatar.get('job', 'N/A'))
                        
                        st.markdown(f"""
                        <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                            <p><strong>아바타 ID:</strong> {id_value}</p>
                            <p><strong>등급:</strong> {grade}</p>
                            <p><strong>직업/캐릭터:</strong> {job}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("조건에 맞는 아바타가 없습니다.")
                        avatar_id = ""
            
            # 코드 패턴 수정 (GT.CREATE_AVATAR 뒤에 ID 추가)
            cheat_codes[selected_cheat] = "GT.CREATE_AVATAR {AVATAR_ID}"
            additional_params["AVATAR_ID"] = avatar_id
            
        elif selected_cheat == "유닛 수동 공격":
            skill_id = st.text_input("스킬 ID를 입력하세요:", "1100000")
            additional_params["SKILLID"] = skill_id
            
        elif selected_cheat == "PC 무적(피격 면역) 처리":
            value = st.radio("상태를 선택하세요:", ["무적 상태", "무적 해제"])
            additional_params["VALUE"] = "1" if value == "무적 상태" else "0"
            
        elif selected_cheat == "대미지 증가 실행":
            value = st.text_input("데미지 증가 값을 입력하세요:", "1000")
            additional_params["VALUE"] = value
            
        elif selected_cheat == "PC 스킬 쿨타임 미적용 + 마나 소모 0":
            value = st.radio("상태를 선택하세요:", ["쿨타임 적용 안함", "쿨타임 적용함"])
            additional_params["VALUE"] = "1" if value == "쿨타임 적용 안함" else "0"
            
        elif selected_cheat == "유닛 좌표 이동":
            # 추천 좌표 선택
            coord_presets = {
                "직접 입력": {"x": "", "y": "", "z": ""},
                "메튼 농장(마을앞)": {"x": "153722", "y": "60780", "z": "1739"},
                "후르츠 빌리지(마을앞)": {"x": "147524", "y": "43515", "z": "2363"},
                "마나마을 분수대": {"x": "163632", "y": "39279", "z": "3958"}
            }
            
            preset = st.selectbox("추천 좌표 선택:", list(coord_presets.keys()))
            
            if preset == "직접 입력":
                x = st.text_input("X 좌표:", "")
                y = st.text_input("Y 좌표:", "")
                z = st.text_input("Z 좌표:", "")
            else:
                preset_coords = coord_presets[preset]
                x = st.text_input("X 좌표:", preset_coords["x"])
                y = st.text_input("Y 좌표:", preset_coords["y"])
                z = st.text_input("Z 좌표:", preset_coords["z"])
                
            additional_params["X"] = x
            additional_params["Y"] = y
            additional_params["Z"] = z
            
        elif selected_cheat == "NPC 좌표로 이동":
            npc_id = st.text_input("NPC ID:", "1001030")
            additional_params["NPC_ID"] = npc_id
            
        elif selected_cheat == "PROP 좌표로 이동":
            prop_id = st.text_input("PROP ID:", "1000026")
            additional_params["PROP_ID"] = prop_id
            
        elif selected_cheat == "퀘스트 목표 지역으로 이동":
            quest_id = st.text_input("퀘스트 ID:", "1000026")
            additional_params["QUEST_ID"] = quest_id
            
        elif selected_cheat == "특정 퀘스트 강제 실행":
            quest_id = st.text_input("퀘스트 ID:", "100200032")
            step = st.text_input("스텝:", "1")
            additional_params["QUEST_ID"] = quest_id
            additional_params["STEP"] = step
            
        elif selected_cheat == "특정 ID 퀘스트 골카운트 n 수치로 실행":
            quest_id = st.text_input("퀘스트 ID:", "1000001")
            goal_count = st.text_input("골 카운트:", "10")
            additional_params["QuestID"] = quest_id
            additional_params["GoalCount"] = goal_count
            
        elif selected_cheat == "경험치 증가":
            value = st.text_input("경험치 증가량:", "10000")
            additional_params["VALUE"] = value
            
        elif selected_cheat == "스킬 획득":
            skill_id = st.text_input("스킬 ID:", "6100003")
            additional_params["DATA_CLASS_SKILL.ID"] = skill_id
            
        elif selected_cheat == "유닛 속도 변경":
            value = st.text_input("속도 값:", "1000")
            additional_params["VALUE"] = value
            
        elif selected_cheat == "탈것 생성":
            search_method = st.radio("탈것 생성 방법 선택:", ["필터", "직접 ID 입력"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                vehicle_id = st.text_input("탈것 ID:", "10001")
            else:  # 필터
                st.subheader("탈것 필터", divider=True)
                
                # JSON 데이터 로드
                vehicles_data = load_data_from_json("data/vehicles.json")
                
                if not vehicles_data:
                    st.warning("탈것 데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
                    vehicle_id = ""
                else:
                    # 필터링 인터페이스
                    grade_filter = st.selectbox("등급 선택:", ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"])
                    
                    # 필터 적용
                    filters = {
                        "grade": grade_filter
                    }
                    
                    # RAG 시스템으로 필터링
                    filtered_vehicles = filter_data_with_rag(vehicles_data, filters)
                    
                    if filtered_vehicles:
                        st.success(f"필터링 결과: {len(filtered_vehicles)}개 탈것")
                        
                        # 탈것 선택 UI
                        def format_vehicle(item):
                            # 엑셀 파일과 매핑: Grade -> grade, Name -> name, Id -> id
                            grade = item.get('Grade', item.get('grade', 'N/A'))
                            name = item.get('Name', item.get('name', 'Unknown'))
                            id_value = item.get('Id', item.get('id', 'N/A'))
                            return f"[{grade}] {name} ({id_value})"
                        
                        selected_vehicle = st.selectbox(
                            "탈것 선택:",
                            options=filtered_vehicles,
                            format_func=format_vehicle
                        )
                        
                        vehicle_id = selected_vehicle.get("Id", selected_vehicle.get("id", ""))
                        
                        # 선택된 탈것 정보 표시
                        grade = selected_vehicle.get('Grade', selected_vehicle.get('grade', 'COMMON'))
                        grade_color = GRADE_COLORS.get(grade, "gray")
                        
                        # 엑셀 컬럼 매핑
                        name = selected_vehicle.get('Name', selected_vehicle.get('name', 'Unknown'))
                        id_value = selected_vehicle.get('Id', selected_vehicle.get('id', 'N/A'))
                        
                        st.markdown(f"""
                        <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                            <p><strong>탈것 ID:</strong> {id_value}</p>
                            <p><strong>등급:</strong> {grade}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("조건에 맞는 탈것이 없습니다.")
                        vehicle_id = ""
            
            additional_params["VEHICLE_ID"] = vehicle_id
            
        elif selected_cheat == "정령 생성":
            search_method = st.radio("정령 생성 방법 선택:", ["필터", "직접 ID 입력"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                spirit_id = st.text_input("정령 ID:", "10000")
            else:  # 필터
                st.subheader("정령 필터", divider=True)
                
                # JSON 데이터 로드
                spirits_data = load_data_from_json("data/spirits.json")
                
                if not spirits_data:
                    st.warning("정령 데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
                    spirit_id = ""
                else:
                    # 필터링 인터페이스
                    col1, col2 = st.columns(2)
                    
                    # 필터링 인터페이스
                    grade_filter = st.selectbox("등급 선택:", ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"])
                    
                    # 필터 적용
                    filters = {
                        "grade": grade_filter
                    }
                    
                    # RAG 시스템으로 필터링
                    filtered_spirits = filter_data_with_rag(spirits_data, filters)
                    
                    if filtered_spirits:
                        st.success(f"필터링 결과: {len(filtered_spirits)}개 정령")
                        
                        # 정령 선택 UI
                        def format_spirit(item):
                            # 엑셀 파일과 매핑: Grade, Name, Id
                            grade = item.get('Grade', item.get('grade', 'N/A'))
                            name = item.get('Name', item.get('name', 'Unknown'))
                            id_value = item.get('Id', item.get('id', 'N/A'))
                            return f"[{grade}] {name} ({id_value})"
                        
                        selected_spirit = st.selectbox(
                            "정령 선택:",
                            options=filtered_spirits,
                            format_func=format_spirit
                        )
                        
                        spirit_id = selected_spirit.get("Id", selected_spirit.get("id", ""))
                        
                        # 선택된 정령 정보 표시
                        grade = selected_spirit.get('Grade', selected_spirit.get('grade', 'COMMON'))
                        grade_color = GRADE_COLORS.get(grade, "gray")
                        
                        # 엑셀 컬럼 매핑
                        name = selected_spirit.get('Name', selected_spirit.get('name', 'Unknown'))
                        id_value = selected_spirit.get('Id', selected_spirit.get('id', 'N/A'))
                        element = selected_spirit.get('Element', selected_spirit.get('element', 'N/A'))
                        
                        st.markdown(f"""
                        <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                            <p><strong>정령 ID:</strong> {id_value}</p>
                            <p><strong>등급:</strong> {grade}</p>
                            <p><strong>원소:</strong> {element}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("조건에 맞는 정령이 없습니다.")
                        spirit_id = ""
            
            additional_params["SPIRIT_ID"] = spirit_id
            
        elif selected_cheat == "정령 즐겨찾기" or selected_cheat == "정령 즐겨찾기 해제":
            collection_id = st.text_input("정령 컬렉션 ID:", "100002")
            additional_params["SPIRIT_COLLECTION_ID"] = collection_id
            
        elif selected_cheat == "서버 치트키 직접 실행":
            cmd = st.text_area("치트 명령어 (GT. 제외):", "CREATE_ITEM 20001 1")
            additional_params["\"GT.\"을 제외한 치트명령어"] = cmd
            
        elif selected_cheat == "반격 (활성 / 비활성)" or selected_cheat == "스킬 사용 (통보 / 확인)" or \
             selected_cheat == "우클릭 이동 (활성 / 비활성)" or selected_cheat == "서버를 통한 움직임 디버그 표시 (표시 / 비표시)" or \
             selected_cheat == "스킬 사용, 우클릭 이동, 서버를 통한 움직임 디버그 표시 한번에 (활성 / 비활성)" or \
             selected_cheat == "상태이상 테스트 (활성 / 비활성)" or selected_cheat == "충돌 테스트 (활성 / 비활성)" or \
             selected_cheat == "파티원 어시스트 테스트 (활성 / 비활성)":
            
            # 각 치트에 맞는 라벨 설정
            if selected_cheat == "반격 (활성 / 비활성)":
                options = ["활성", "비활성"]
                label = "반격 상태:"
            elif selected_cheat == "스킬 사용 (통보 / 확인)":
                options = ["통보", "확인"]
                label = "스킬 사용 모드:"
            elif selected_cheat == "우클릭 이동 (활성 / 비활성)":
                options = ["활성", "비활성"]
                label = "우클릭 이동:"
            elif selected_cheat == "서버를 통한 움직임 디버그 표시 (표시 / 비표시)":
                options = ["표시", "비표시"]
                label = "움직임 디버그:"
            elif selected_cheat == "스킬 사용, 우클릭 이동, 서버를 통한 움직임 디버그 표시 한번에 (활성 / 비활성)":
                options = ["활성", "비활성"]
                label = "모든 디버그 설정:"
            elif selected_cheat == "상태이상 테스트 (활성 / 비활성)":
                options = ["활성", "비활성"]
                label = "상태이상 테스트:"
            elif selected_cheat == "충돌 테스트 (활성 / 비활성)":
                options = ["활성", "비활성"]
                label = "충돌 테스트:"
            elif selected_cheat == "파티원 어시스트 테스트 (활성 / 비활성)":
                options = ["활성", "비활성"]
                label = "파티원 어시스트 테스트:"
                
            value = st.radio(label, options)
            additional_params["숫자값"] = "1" if value == options[0] else "0"
            
        elif selected_cheat == "테스트 모드 변경":
            # 테스트 모드 옵션이 정의되어 있지 않으면 라디오 버튼으로 선택
            if 'test_mode_options' not in locals() or test_mode_options is None:
                value = st.radio("테스트 모드 선택:", [
                    "상태이상 테스트 활성",
                    "충돌 테스트 활성",
                    "파티원 어시스트 테스트 활성", 
                    "모두 비활성"
                ])
                mode_map = {
                    "상태이상 테스트 활성": "1",
                    "충돌 테스트 활성": "2",
                    "파티원 어시스트 테스트 활성": "3",
                    "모두 비활성": "0"
                }
                additional_params["숫자값"] = mode_map[value]
            else:
                # 이미 selectbox에서 선택된 테스트 모드 옵션 사용
                mode_value = test_mode_options.split(".")[0]
                additional_params["숫자값"] = mode_value
            
        elif selected_cheat == "배틀로얄 참가 최대 인원 변경":
            count = st.text_input("최대 인원:", "2")
            additional_params["count"] = count
            
        elif selected_cheat == "아이템 보상 드랍 FX Trail 속도":
            value = st.text_input("속도 값:", "20")
            additional_params["값"] = value
            
        elif selected_cheat == "커런시 획득":
            currency_type = st.text_input("재화 타입:", "1")
            amount = st.text_input("수량:", "1000")
            additional_params["재화타입"] = currency_type
            additional_params["수량"] = amount
            
        elif selected_cheat == "무기소울 생성":
            search_method = st.radio("무기소울 생성 방법 선택:", ["필터", "직접 ID 입력"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                weapon_soul_id = st.text_input("무기소울 ID:", "10000")
            else:  # 필터
                st.subheader("무기소울 필터", divider=True)
                
                # JSON 데이터 로드
                weapon_souls_data = load_data_from_json("data/weapon_souls.json")
                
                if not weapon_souls_data:
                    st.warning("무기소울 데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
                    weapon_soul_id = ""
                else:
                    # 필터링 인터페이스
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        grade_filter = st.selectbox("등급 선택:", ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"])
                    
                    with col2:
                        job_filter = st.selectbox("직업 선택:", ["모두", "헌터", "어쌔신", "마법사", "치유사", "기사", "궁수", "창병", "마검사", "검투사", "도적", "알케미스트", "공용"])
                    
                    # 필터 적용
                    filters = {
                        "grade": grade_filter,
                        "job": job_filter
                    }
                    
                    # RAG 시스템으로 필터링
                    filtered_weapon_souls = filter_data_with_rag(weapon_souls_data, filters)
                    
                    if filtered_weapon_souls:
                        st.success(f"필터링 결과: {len(filtered_weapon_souls)}개 무기소울")
                        
                        # 무기소울 선택 UI
                        def format_weapon_soul(item):
                            # 엑셀 파일과 매핑: Grade -> grade, Name -> name, Id -> id, Job/char -> job
                            grade = item.get('Grade', item.get('grade', 'N/A'))
                            name = item.get('Name', item.get('name', 'Unknown'))
                            job = item.get('char', item.get('job', 'N/A'))
                            id_value = item.get('Id', item.get('id', 'N/A'))
                            return f"[{grade}] {name} - {job} ({id_value})"
                        
                        selected_weapon_soul = st.selectbox(
                            "무기소울 선택:",
                            options=filtered_weapon_souls,
                            format_func=format_weapon_soul
                        )
                        
                        weapon_soul_id = selected_weapon_soul.get("Id", selected_weapon_soul.get("id", ""))
                        
                        # 선택된 무기소울 정보 표시
                        grade = selected_weapon_soul.get('Grade', selected_weapon_soul.get('grade', 'COMMON'))
                        grade_color = GRADE_COLORS.get(grade, "gray")
                        
                        # 엑셀 컬럼 매핑
                        name = selected_weapon_soul.get('Name', selected_weapon_soul.get('name', 'Unknown'))
                        id_value = selected_weapon_soul.get('Id', selected_weapon_soul.get('id', 'N/A'))
                        job = selected_weapon_soul.get('char', selected_weapon_soul.get('job', 'N/A'))
                        
                        st.markdown(f"""
                        <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                            <p><strong>무기소울 ID:</strong> {id_value}</p>
                            <p><strong>등급:</strong> {grade}</p>
                            <p><strong>직업:</strong> {job}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("조건에 맞는 무기소울이 없습니다.")
                        weapon_soul_id = ""
            
            additional_params["WEAPONSOUL_ID"] = weapon_soul_id
            
        elif selected_cheat == "아스터 생성":
            search_method = st.radio("아스터 생성 방법 선택:", ["필터", "직접 ID 입력"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                aster_id = st.text_input("아스터 ID:", "10000")
            else:  # 필터
                st.subheader("아스터 필터", divider=True)
                
                # JSON 데이터 로드
                asters_data = load_data_from_json("data/asters.json")
                
                if not asters_data:
                    st.warning("아스터 데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
                    aster_id = ""
                else:
                    # 필터링 인터페이스
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        grade_filter = st.selectbox("등급 선택:", ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"])
                    
                    with col2:
                        direction_filter = st.selectbox("방향 선택:", ["모두", "1", "2", "3", "4", "5", "6"])
                    
                    # 등급 필터 적용 (RAG 시스템)
                    filters = {
                        "grade": grade_filter
                    }
                    
                    # 먼저 등급 필터링 적용
                    filtered_asters = filter_data_with_rag(asters_data, filters)
                    
                    # 방향 필터링을 수동으로 처리 (이름의 마지막 숫자 기준)
                    if direction_filter and direction_filter != "모두":
                        # 방향 필터 수동 적용 (이름 마지막 숫자)
                        filtered_by_direction = []
                        for item in filtered_asters:
                            name = item.get('Name', item.get('name', ''))
                            if name and len(name) > 0 and name[-1].isdigit() and name[-1] == direction_filter:
                                filtered_by_direction.append(item)
                        filtered_asters = filtered_by_direction
                    
                    if filtered_asters:
                        st.success(f"필터링 결과: {len(filtered_asters)}개 아스터")
                        
                        # 아스터 선택 UI
                        def format_aster(item):
                            # 엑셀 컬럼 매핑: Grade, Name, Id
                            grade = item.get('Grade', item.get('grade', 'N/A'))
                            name = item.get('Name', item.get('name', 'Unknown'))
                            id_value = item.get('Id', item.get('id', 'N/A'))
                            
                            # 이름에서 방향 추출 (아스터1, 아스터2, ... 에서 마지막 숫자)
                            direction = ""
                            if name:
                                # 이름의 마지막 문자가 숫자인지 확인
                                if name[-1].isdigit():
                                    direction = name[-1]
                                    
                            return f"[{grade}] {name} - 방향: {direction} ({id_value})"
                        
                        selected_aster = st.selectbox(
                            "아스터 선택:",
                            options=filtered_asters,
                            format_func=format_aster,
                            key="aster_select"
                        )
                        
                        aster_id = selected_aster.get("Id", selected_aster.get("id", ""))
                        
                        # 선택된 아스터 정보 표시
                        grade = selected_aster.get('Grade', selected_aster.get('grade', 'COMMON'))
                        grade_color = GRADE_COLORS.get(grade, "gray")
                        
                        # 엑셀 컬럼 매핑
                        name = selected_aster.get('Name', selected_aster.get('name', 'Unknown'))
                        id_value = selected_aster.get('Id', selected_aster.get('id', 'N/A'))
                        
                        # 이름에서 방향 추출
                        direction = ""
                        if name and name[-1].isdigit():
                            direction = name[-1]
                        
                        st.markdown(f"""
                        <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: {grade_color}; margin-top: 0;">{name}</h4>
                            <p><strong>아스터 ID:</strong> {id_value}</p>
                            <p><strong>등급:</strong> {grade}</p>
                            <p><strong>방향:</strong> {direction}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("조건에 맞는 아스터가 없습니다.")
                        aster_id = ""
            
            additional_params["ASTER_ID"] = aster_id
            
        elif selected_cheat == "강화된 아이템 생성":
            # 아이템 검색 인터페이스 추가
            search_method = st.radio("아이템 선택 방법:", ["직접 ID 입력", "아이템 검색"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                item_id = st.text_input("아이템 ID:", "903003000")
            else:
                # 검색과 필터 분리
                st.subheader("강화 아이템 검색", divider=True)
                
                # 검색입력과 버튼 배치
                search_col1, search_col2 = st.columns([3, 1])
                with search_col1:
                    search_query = st.text_input("이름으로 강화 아이템 검색 (키워드 입력):", "")
                with search_col2:
                    search_button = st.button("검색", key="search_upgrade")
                
                # 검색 결과 처리
                search_results = []
                if search_query and (search_button or search_query.strip() != ""):
                    search_results = search_items_by_name(search_query)
                    if search_results:
                        st.success(f"'{search_query}' 검색 결과: {len(search_results)}개 아이템 발견")
                    else:
                        st.warning(f"'{search_query}' 검색 결과가 없습니다.")
                
                # 필터링 인터페이스
                st.subheader("강화 아이템 필터링", divider=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    grade = st.selectbox("등급 선택 (강화 아이템):", GRADE_LIST)
                
                with col2:
                    job = st.selectbox("직업 선택 (강화 아이템):", JOB_LIST)
                
                with col3:
                    part = st.selectbox("부위 선택 (강화 아이템):", PART_LIST)
                
                # 필터 적용 버튼
                filter_button = st.button("필터 검색", key="filter_upgrade")
                filtered_items = []
                
                if filter_button:
                    # 필터 상태 표시
                    filter_status = []
                    if grade != "모두":
                        filter_status.append(f"등급: {grade}")
                    if job != "모두":
                        filter_status.append(f"직업: {job}")
                    if part != "모두":
                        filter_status.append(f"부위: {part}")
                    
                    if filter_status:
                        st.caption(f"적용된 필터: {', '.join(filter_status)}")
                    
                    # 필터링 적용
                    filtered_items = filter_items(grade, job, part)
                
                # 최종 표시 아이템 결정 (검색 또는 필터 중 하나만 사용)
                display_items = []
                if search_query and (search_button or search_query.strip() != "") and search_results:
                    display_items = search_results
                    st.subheader("검색 결과")
                elif filter_button:
                    if filtered_items:
                        display_items = filtered_items
                        st.subheader(f"필터링 결과 ({len(filtered_items)}개 아이템)")
                    else:
                        st.warning("조건에 맞는 아이템이 없습니다.")
                else:
                    # 기본 아이템 몇 개 표시
                    display_items = filter_items("모두", "모두", "모두")[:30]
                    st.subheader("강화 가능 아이템 목록")
                
                if len(display_items) == 0:
                    st.warning("표시할 아이템이 없습니다.")
                    st.info("다른 검색어를 입력하거나 필터 조건을 변경해보세요.")
                
                if display_items:
                    # 등급별 색상 표시를 위한 함수
                    def format_item(item):
                        # Excel 컬럼 매핑: Grade -> grade, Name -> name, Id -> id
                        grade = item.get('Grade', item.get('grade', 'N/A'))
                        name = item.get('Name', item.get('name', 'Unknown'))
                        id_value = item.get('Id', item.get('id', 'N/A'))
                        job_info = item.get('job', '공용')
                        job_info = job_info if job_info != "공용" else "공용"
                        return f"[{grade}] {name} - {job_info} ({id_value})"
                    
                    # 아이템 선택 UI
                    selected_item = st.selectbox(
                        "강화할 아이템 선택:",
                        options=display_items,
                        format_func=format_item
                    )
                    
                    item_id = selected_item.get("Id", selected_item.get("id", ""))
                    
                    # 선택된 아이템 정보 표시
                    grade_color = GRADE_COLORS.get(selected_item["grade"], "gray")
                    
                    st.markdown(f"""
                    <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <h4 style="color: {grade_color}; margin-top: 0;">{selected_item['name']}</h4>
                        <p><strong>아이템 ID:</strong> {selected_item['id']}</p>
                        <p><strong>등급:</strong> {selected_item['grade']}</p>
                        <p><strong>직업:</strong> {selected_item['job']}</p>
                        <p><strong>부위:</strong> {selected_item['part']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("조건에 맞는 아이템이 없습니다.")
                    item_id = ""
            
            # 강화 옵션 입력
            col1, col2 = st.columns(2)
            
            with col1:
                count = st.text_input("생성할 개수:", "1")
            
            with col2:
                level = st.slider("강화 레벨:", min_value=1, max_value=20, value=10)
            
            additional_params["아이템ID"] = item_id
            additional_params["개수"] = count
            additional_params["레벨"] = str(level)
            
        elif selected_cheat == "귀속 여부에 따른 아이템 생성":
            # 아이템 검색 인터페이스 추가
            search_method = st.radio("아이템 선택 방법 (귀속):", ["직접 ID 입력", "아이템 검색"], horizontal=True)
            
            if search_method == "직접 ID 입력":
                item_id = st.text_input("아이템 ID:", "00090001")
            else:
                # 검색과 필터 분리
                st.subheader("귀속 아이템 검색", divider=True)
                
                # 검색입력과 버튼 배치
                search_col1, search_col2 = st.columns([3, 1])
                with search_col1:
                    search_query = st.text_input("이름으로 귀속 아이템 검색 (키워드 입력):", "")
                with search_col2:
                    search_button = st.button("검색", key="search_binding")
                
                # 검색 결과 처리
                search_results = []
                if search_query and (search_button or search_query.strip() != ""):
                    search_results = search_items_by_name(search_query)
                    if search_results:
                        st.success(f"'{search_query}' 검색 결과: {len(search_results)}개 아이템 발견")
                    else:
                        st.warning(f"'{search_query}' 검색 결과가 없습니다.")
                
                # 필터링 인터페이스
                st.subheader("귀속 아이템 필터링", divider=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    grade = st.selectbox("등급 선택 (귀속 아이템):", GRADE_LIST)
                
                with col2:
                    job = st.selectbox("직업 선택 (귀속 아이템):", JOB_LIST)
                
                with col3:
                    part = st.selectbox("부위 선택 (귀속 아이템):", PART_LIST)
                
                # 필터 적용 버튼
                filter_button = st.button("필터 검색", key="filter_binding")
                filtered_items = []
                
                if filter_button:
                    # 필터 상태 표시
                    filter_status = []
                    if grade != "모두":
                        filter_status.append(f"등급: {grade}")
                    if job != "모두":
                        filter_status.append(f"직업: {job}")
                    if part != "모두":
                        filter_status.append(f"부위: {part}")
                    
                    if filter_status:
                        st.caption(f"적용된 필터: {', '.join(filter_status)}")
                
                # 필터링 적용 (검색과 분리)
                if filter_button:
                    filtered_items = filter_items(grade, job, part)
                
                # 최종 표시 아이템 결정 (검색 또는 필터 중 하나만 사용)
                display_items = []
                if search_query and (search_button or search_query.strip() != "") and search_results:
                    display_items = search_results
                    st.subheader("검색 결과")
                elif filter_button:
                    if filtered_items:
                        display_items = filtered_items
                        st.subheader(f"필터링 결과 ({len(filtered_items)}개 아이템)")
                    else:
                        st.warning("조건에 맞는 아이템이 없습니다.")
                else:
                    # 기본 아이템 몇 개 표시
                    display_items = filter_items("모두", "모두", "모두")[:30]
                    st.subheader("귀속 가능 아이템 목록")
                
                if len(display_items) == 0:
                    st.warning("표시할 아이템이 없습니다.")
                    st.info("다른 검색어를 입력하거나 필터 조건을 변경해보세요.")
                
                if display_items:
                    # 등급별 색상 표시를 위한 함수
                    def format_item(item):
                        # Excel 컬럼 매핑: Grade -> grade, Name -> name, Id -> id
                        grade = item.get('Grade', item.get('grade', 'N/A'))
                        name = item.get('Name', item.get('name', 'Unknown'))
                        id_value = item.get('Id', item.get('id', 'N/A'))
                        job_info = item.get('job', '공용')
                        job_info = job_info if job_info != "공용" else "공용"
                        return f"[{grade}] {name} - {job_info} ({id_value})"
                    
                    # 아이템 선택 UI
                    selected_item = st.selectbox(
                        "귀속 설정할 아이템 선택:",
                        options=display_items,
                        format_func=format_item
                    )
                    
                    item_id = selected_item.get("Id", selected_item.get("id", ""))
                    
                    # 선택된 아이템 정보 표시
                    grade_color = GRADE_COLORS.get(selected_item["grade"], "gray")
                    
                    st.markdown(f"""
                    <div style="border: 1px solid {grade_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <h4 style="color: {grade_color}; margin-top: 0;">{selected_item['name']}</h4>
                        <p><strong>아이템 ID:</strong> {selected_item['id']}</p>
                        <p><strong>등급:</strong> {selected_item['grade']}</p>
                        <p><strong>직업:</strong> {selected_item['job']}</p>
                        <p><strong>부위:</strong> {selected_item['part']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("조건에 맞는 아이템이 없습니다.")
                    item_id = ""
            
            # 귀속 및 개수 설정
            col1, col2 = st.columns(2)
            
            with col1:
                count = st.text_input("개수:", "1")
            
            with col2:
                binding = st.selectbox("귀속 여부:", ["CHARACTER", "ACCOUNT", "NONE"], 
                                      help="CHARACTER: 캐릭터 귀속, ACCOUNT: 계정 귀속, NONE: 미귀속")
            
            additional_params["아이템ID"] = item_id
            additional_params["개수"] = count
            additional_params["귀속 여부"] = binding
            
        elif selected_cheat == "길드 경험치 설정":
            exp_value = st.text_input("경험치 값:", "5000")
            guild_name = st.text_input("길드 이름:", "길드이름")
            additional_params["SetValue"] = exp_value
            additional_params["GuildName"] = guild_name
            
        # 복잡한 합성 관련 파라미터
        elif selected_cheat == "아이템 강화":
            material_id = st.text_input("강화재료 아이템 ID:", "900090020")
            target_level = st.text_input("강화목표단계:", "8")
            seq1 = st.text_input("강화시킬 아이템 시퀀스1:", "18521")
            seq2 = st.text_input("강화시킬 아이템 시퀀스2:", "")
            additional_params["강화재료 아이템ID"] = material_id
            additional_params["강화목표단계"] = target_level
            additional_params["강화시킬 아이템 시퀀스1"] = seq1
            if seq2:
                additional_params["강화시킬 아이템 시퀀스2"] = seq2
            
        elif selected_cheat == "아이템 하락 강화":
            material_id = st.text_input("강화재료 아이템 ID:", "900090020")
            target_level = st.text_input("강화목표단계:", "8")
            seq1 = st.text_input("강화시킬 아이템 시퀀스1:", "18521")
            seq2 = st.text_input("강화시킬 아이템 시퀀스2:", "18522")
            additional_params["강화재료 아이템ID"] = material_id
            additional_params["강화목표단계"] = target_level
            additional_params["강화시킬 아이템 시퀀스1"] = seq1
            additional_params["강화시킬 아이템 시퀀스2"] = seq2
            
        elif selected_cheat == "합성":
            item_type = st.text_input("아이템 타입:", "AVATAR")
            item1 = st.text_input("합성할 아이템 ID 1:", "110318000")
            item2 = st.text_input("합성할 아이템 ID 2:", "10318000")
            item3 = st.text_input("합성할 아이템 ID 3:", "110318000")
            item4 = st.text_input("합성할 아이템 ID 4:", "0")
            additional_params["아이템타입"] = item_type
            additional_params["합성할 아이템ID"] = f"{item1} {item2} {item3} {item4}"
            
        elif selected_cheat == "확정 - 교체":
            item_type = st.text_input("아이템 타입:", "AVATAR")
            prev_item = st.text_input("교체할(교체전) 아이템 ID:", "110518000")
            additional_params["아이템 타입"] = item_type
            additional_params["교체할(교체전) 아이템 ID"] = prev_item
            
        elif selected_cheat == "자동 합성":
            item_type = st.text_input("아이템 타입:", "AVATAR")
            target_grade = st.selectbox("목표등급:", ["MYTH", "LEGEND", "EPIC", "RARE", "UNCOMMON", "COMMON"])
            class_selection = st.selectbox("선택클래스:", ["ALL", "WARRIOR", "MAGICIAN", "ARCHER", "THIEF"])
            additional_params["아이템 타입"] = item_type
            additional_params["목표등급"] = target_grade
            additional_params["선택클래스"] = class_selection
            
        elif selected_cheat == "실패누적보상":
            item_type = st.text_input("아이템 타입:", "AVATAR")
            reward_grade = st.selectbox("보상받을 등급:", ["LEGEND", "EPIC", "RARE", "UNCOMMON", "COMMON"])
            additional_params["아이템 타입"] = item_type
            additional_params["보상받을 등급"] = reward_grade
    
    # 선택된 치트 코드 가져오기
    # 테스트 모드 변경인 경우 세부 옵션 코드 사용
    if selected_cheat == "테스트 모드 변경" and 'test_mode_options' in globals() and test_mode_options is not None:
        cheat_code = test_mode_codes.get(test_mode_options, "GT.TestMode 0")
    else:
        # 매핑된 코드가 없으면 기본값으로 치트 이름 그대로 사용
        cheat_code = cheat_codes.get(selected_cheat, selected_cheat.replace(" ", "_").upper())
        
        # 특수 처리 - 합성 관련
        if selected_cheat == "합성":
            # 합성 명령어는 합성할 아이템 ID를 개별적으로 처리해야 함
            item_type = additional_params.get("아이템타입", "1")
            items = additional_params.get("합성할 아이템ID", "").split()
            cheat_code = f"GT.SC COMPOSE {item_type}"
            for item in items:
                cheat_code += f" {item}"
        # 추가 파라미터가 있는 경우 치트 코드에 반영
        elif additional_params:
            # 플레이스홀더 대체 (예: {MOB_ID}를 실제 값으로 대체)
            for key, value in additional_params.items():
                placeholder = "{" + key + "}"
                cheat_code = cheat_code.replace(placeholder, str(value))
    
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
                
                # 코드 플로우 실행 및 로그 메시지 받기
                try:
                    result, log_messages = auto_controller.execute_code_flow(image_recognizer, cheat_code)
                except ValueError:  # 이전 버전과의 호환성을 위해
                    auto_controller.execute_code_flow(image_recognizer, cheat_code)
                    log_messages = [
                        "치트 메뉴 진입 중...",
                        "치트 메뉴 열기 (code 버튼 클릭)",
                        "치트 입력창 선택 (code2 버튼 클릭)",
                        f"치트 코드 입력: {cheat_code}",
                        "확인 버튼 클릭 (code3 버튼 클릭)",
                        "적용 버튼 클릭 (code4 버튼 클릭)",
                        f"치트 코드 '{cheat_code}' 적용 완료!"
                    ]
                
                # 치트 적용 결과 표시
                if test_mode_options:
                    st.success(f"테스트 모드가 '{test_mode_options}'(으)로 성공적으로 변경되었습니다!")
                else:
                    st.success(f"치트 적용 성공: {selected_cheat}")
                
                # 적용된 코드 정보 보여주기 (상세 정보 포함)
                with st.expander("실행 상세 정보", expanded=True):
                    st.code(f"실행된 치트 코드: {cheat_code}", language="bash")
                    
                    # 시뮬레이션 모드 상세 정보
                    st.info("시뮬레이션 실행 로그:")
                    log_area = st.empty()
                    log_text = "\n".join(log_messages)
                    log_area.text(log_text)
            
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("게임 창을 선택하고 '확인' 버튼을 눌러주세요.")

if __name__ == "__main__":
    main() 