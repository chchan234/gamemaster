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
        "정령, 탈것, 무기소울, 아바타, 아스터 생성": {
            "코드": "GT.SC CREATE_{아이템 타입} {생성할 아이템 ID} {생성할 개수}",
            "예시": "GT.SC CREATE_AVATAR 900090001 100",
            "정보": "{생성할 개수} 생략시 1개만 생성"
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
    
    # 테스트 모드에 대한 특별 매핑
    test_mode_codes = {
        "1. 상태이상 테스트 활성": "GT.TestMode 1",
        "2. 충돌 테스트 활성": "GT.TestMode 2",
        "3. 파티원 어시스트 테스트 활성": "GT.TestMode 3", 
        "0. 모두 비활성": "GT.TestMode 0"
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
    
    # 선택된 치트에 대한 정보 표시
    if selected_cheat in cheat_info:
        info = cheat_info[selected_cheat]
        
        # 정보 섹션 만들기
        with st.expander("치트 정보", expanded=True):
            if info["예시"]:
                st.code(info["예시"], language="bash")
            if info["정보"]:
                st.info(info["정보"])
    
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
    
    # 선택된 치트에 추가 입력이 필요한지 확인
    additional_params = {}
    
    # 치트 선택에 따른 추가 파라미터 입력 필드 설정
    with st.container():
        if selected_cheat == "퀘스트 몬스터킬":
            mob_id = st.text_input("몬스터 ID를 입력하세요:", "1000001")
            additional_params["MOB_ID"] = mob_id
            
        elif selected_cheat == "아이템 생성":
            item_id = st.text_input("아이템 ID를 입력하세요:", "900090001")
            item_cnt = st.text_input("생성할 개수를 입력하세요:", "100")
            additional_params["ITEM_ID"] = item_id
            additional_params["ITEM_CNT"] = item_cnt
            
        elif selected_cheat == "아바타 아이템 생성":
            avatar_id = st.text_input("아바타 ID를 입력하세요:", "900090001")
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
            vehicle_id = st.text_input("탈것 ID:", "10001")
            additional_params["VEHICLE_ID"] = vehicle_id
            
        elif selected_cheat == "정령 생성":
            spirit_id = st.text_input("정령 ID:", "10000")
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
            
        elif selected_cheat == "테스트 모드 변경" and not test_mode_options:
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
            
        elif selected_cheat == "정령, 탈것, 무기소울, 아바타, 아스터 생성":
            item_type = st.selectbox("아이템 타입:", ["SPIRIT", "VEHICLE", "WEAPONSOUL", "AVATAR", "ASTER"])
            item_id = st.text_input("아이템 ID:", "900090001")
            count = st.text_input("개수:", "100")
            additional_params["아이템 타입"] = item_type
            additional_params["생성할 아이템 ID"] = item_id
            additional_params["생성할 개수"] = count
            
        elif selected_cheat == "강화된 아이템 생성":
            item_id = st.text_input("아이템 ID:", "903003000")
            count = st.text_input("개수:", "1")
            level = st.text_input("레벨:", "20")
            additional_params["아이템ID"] = item_id
            additional_params["개수"] = count
            additional_params["레벨"] = level
            
        elif selected_cheat == "귀속 여부에 따른 아이템 생성":
            item_id = st.text_input("아이템 ID:", "00090001")
            count = st.text_input("개수:", "1")
            binding = st.selectbox("귀속 여부:", ["CHARACTER", "ACCOUNT", "NONE"])
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
    if test_mode_options:
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
                cheat_code = cheat_code.replace(placeholder, value)
    
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