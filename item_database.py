"""
게임 아이템 데이터베이스
"""
import re
from difflib import SequenceMatcher

# 아이템 데이터 (품목ID, 아이템설명, 등급, 아이템이름)
ITEM_DB = [
    # 지급 무기
    {"id": "110001000", "desc": "실키라_헌터 지급 무기", "grade": "COMMON", "name": "오래된 메린의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "120001000", "desc": "실키라_어쌔신 지급 무기", "grade": "COMMON", "name": "오래된 메린의 쌍차", "job": "어쌔신", "part": "무기", "character": "실키라"},
    {"id": "210001000", "desc": "이리시아_마법사 지급 무기", "grade": "COMMON", "name": "오래된 메린의 오브", "job": "마법사", "part": "무기", "character": "이리시아"},
    {"id": "220001000", "desc": "이리시아_치유사 지급 무기", "grade": "COMMON", "name": "오래된 메린의 지팡이", "job": "치유사", "part": "무기", "character": "이리시아"},
    {"id": "310001000", "desc": "란스_지급무기", "grade": "COMMON", "name": "오래된 메린의 대검", "job": "기사", "part": "무기", "character": "란스"},
    {"id": "410001000", "desc": "라이뉴_궁수 지급 무기", "grade": "COMMON", "name": "오래된 메린의 대궁", "job": "궁수", "part": "무기", "character": "라이뉴"},
    {"id": "420001000", "desc": "라이뉴_창병 지급 무기", "grade": "COMMON", "name": "오래된 메린의 장창", "job": "창병", "part": "무기", "character": "라이뉴"},
    {"id": "510001000", "desc": "데커드_마검사 지급 무기", "grade": "COMMON", "name": "오래된 메린의 도끼", "job": "마검사", "part": "무기", "character": "데커드"},
    {"id": "520001000", "desc": "데커드_검투사 지급 무기", "grade": "COMMON", "name": "오래된 메린의 마검", "job": "검투사", "part": "무기", "character": "데커드"},
    {"id": "610001000", "desc": "로버_도적 지급 무기", "grade": "COMMON", "name": "오래된 메린의 단검", "job": "도적", "part": "무기", "character": "로버"},
    {"id": "620001000", "desc": "로버_연금술사 지급 무기", "grade": "COMMON", "name": "오래된 메린의 플라스크", "job": "연금술사", "part": "무기", "character": "로버"},

    # 헌터 무기
    {"id": "110001001", "desc": "헌터_일반_무기_01", "grade": "COMMON", "name": "기본형 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001002", "desc": "헌터_일반_무기_02", "grade": "COMMON", "name": "견습대원의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001003", "desc": "헌터_일반_무기_03", "grade": "COMMON", "name": "초보 모험가의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001004", "desc": "헌터_일반_무기_04", "grade": "COMMON", "name": "견습 사냥꾼의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001005", "desc": "헌터_일반_무기_05_제작", "grade": "COMMON", "name": "견습 대장장이의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001006", "desc": "헌터_일반_무기_06", "grade": "COMMON", "name": "보급형 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001007", "desc": "헌터_일반_무기_07", "grade": "COMMON", "name": "훈련병의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001008", "desc": "헌터_일반_무기_08", "grade": "COMMON", "name": "순찰자의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "110001009", "desc": "헌터_일반_무기_09", "grade": "COMMON", "name": "빛바랜 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001000", "desc": "헌터_고급_무기_01", "grade": "ADVANCE", "name": "개량형 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001001", "desc": "헌터_고급_무기_02_제작", "grade": "ADVANCE", "name": "공방 수제 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001002", "desc": "헌터_고급_무기_03", "grade": "ADVANCE", "name": "숙련된 모험가의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001003", "desc": "헌터_고급_무기_04", "grade": "ADVANCE", "name": "숙련된 사냥꾼의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001004", "desc": "헌터_고급_무기_05", "grade": "ADVANCE", "name": "세공된 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001005", "desc": "헌터_고급_무기_06_제작", "grade": "ADVANCE", "name": "노련한 대장장이의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001006", "desc": "헌터_고급_무기_07", "grade": "ADVANCE", "name": "견고한 일격의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001007", "desc": "헌터_고급_무기_08", "grade": "ADVANCE", "name": "투기장의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001008", "desc": "헌터_고급_무기_09", "grade": "ADVANCE", "name": "노련한 순찰자의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001009", "desc": "헌터_고급_무기_10", "grade": "ADVANCE", "name": "정식 대원의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "111001010", "desc": "헌터_고급_무기_11", "grade": "ADVANCE", "name": "예리한 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001000", "desc": "헌터_희귀_무기_01", "grade": "RARE", "name": "개조된 상급 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001001", "desc": "헌터_희귀_무기_02", "grade": "RARE", "name": "수비대장의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001002", "desc": "헌터_희귀_무기_03", "grade": "RARE", "name": "상급 모험가의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001003", "desc": "헌터_희귀_무기_04_제작", "grade": "RARE", "name": "비상하는 명인의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001004", "desc": "헌터_희귀_무기_05", "grade": "RARE", "name": "상급 사냥꾼의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001005", "desc": "헌터_희귀_무기_06_제작", "grade": "RARE", "name": "모험단장의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001006", "desc": "헌터_희귀_무기_07", "grade": "RARE", "name": "격렬한 투지의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001007", "desc": "헌터_희귀_무기_08", "grade": "RARE", "name": "기사단의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001008", "desc": "헌터_희귀_무기_09_제작", "grade": "RARE", "name": "연구소 특제 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001009", "desc": "헌터_희귀_무기_10", "grade": "RARE", "name": "견고한 맹세의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001010", "desc": "헌터_희귀_무기_11_제작", "grade": "RARE", "name": "긍지높은 명인의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "112001011", "desc": "헌터_희귀_무기_12", "grade": "RARE", "name": "거친 투사의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001000", "desc": "헌터_영웅_무기_01", "grade": "EPIC", "name": "굳센 맹약의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001001", "desc": "헌터_영웅_무기_02_제작", "grade": "EPIC", "name": "왕실 기사단장의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001002", "desc": "헌터_영웅_무기_03", "grade": "EPIC", "name": "부활한 영웅의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001003", "desc": "헌터_영웅_무기_04", "grade": "EPIC", "name": "용 사냥꾼의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001004", "desc": "헌터_영웅_무기_05_제작", "grade": "EPIC", "name": "유적 정복자의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001005", "desc": "헌터_영웅_무기_06", "grade": "EPIC", "name": "고귀한 혈통의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001006", "desc": "헌터_영웅_무기_07", "grade": "EPIC", "name": "포효하는 역린 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001007", "desc": "헌터_영웅_무기_08_제작", "grade": "EPIC", "name": "괴물 분쇄자의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001008", "desc": "헌터_영웅_무기_09_제작", "grade": "EPIC", "name": "약속된 복수의 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "113001009", "desc": "헌터_영웅_무기_10", "grade": "EPIC", "name": "위대한 무법자 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "114001000", "desc": "헌터_전설_무기_01", "grade": "LEGEND", "name": "전사장의 명예 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "114001001", "desc": "헌터_전설_무기_02_제작", "grade": "LEGEND", "name": "용기사의 분노 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "114001002", "desc": "헌터_전설_무기_03", "grade": "LEGEND", "name": "천상의 단죄 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "114001003", "desc": "헌터_전설_무기_04", "grade": "LEGEND", "name": "포효하는 복수 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "114001004", "desc": "헌터_전설_무기_05_제작", "grade": "LEGEND", "name": "잊힌 영웅의 증표 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "114001005", "desc": "헌터_전설_무기_06", "grade": "LEGEND", "name": "세계의 각인 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "115001000", "desc": "헌터_신화_무기_01_제작", "grade": "MYTH", "name": "각성의 수호자 핸드건", "job": "헌터", "part": "무기", "character": "실키라"},
    {"id": "115001001", "desc": "헌터_신화_무기_02_제작", "grade": "MYTH", "name": "별빛의 수호자 피스톨", "job": "헌터", "part": "무기", "character": "실키라"},

    # 어쌔신 무기
    {"id": "120001001", "desc": "어쌔신_일반_무기_01", "grade": "COMMON", "name": "기본형 쌍차", "job": "어쌔신", "part": "무기", "character": "실키라"},
    {"id": "120001002", "desc": "어쌔신_일반_무기_02", "grade": "COMMON", "name": "견습대원의 쌍차", "job": "어쌔신", "part": "무기", "character": "실키라"},
    {"id": "123001003", "desc": "어쌔신_영웅_무기_04", "grade": "EPIC", "name": "용 사냥꾼의 쌍차", "job": "어쌔신", "part": "무기", "character": "실키라"},

    # 마법사/치유사 무기
    {"id": "210001001", "desc": "마법사_일반_무기_01", "grade": "COMMON", "name": "기본형 오브", "job": "마법사", "part": "무기", "character": "이리시아"},
    {"id": "213001003", "desc": "마법사_영웅_무기_04", "grade": "EPIC", "name": "용 사냥꾼의 오브", "job": "마법사", "part": "무기", "character": "이리시아"},
    {"id": "220001001", "desc": "치유사_일반_무기_01", "grade": "COMMON", "name": "기본형 스태프", "job": "치유사", "part": "무기", "character": "이리시아"},

    # 기타 장비 아이템
    {"id": "900002000", "desc": "머리_일반_흠투_01", "grade": "COMMON", "name": "초심자의 캡", "job": "공용", "part": "머리", "character": "공용"},
    {"id": "900003000", "desc": "가슴_일반_01", "grade": "COMMON", "name": "초심자의 사냥복", "job": "공용", "part": "가슴", "character": "공용"},
    {"id": "900004000", "desc": "장갑_일반_01", "grade": "COMMON", "name": "초심자의 전투 장갑", "job": "공용", "part": "장갑", "character": "공용"},
    {"id": "900005000", "desc": "신발_일반_01", "grade": "COMMON", "name": "초심자의 전투 구두", "job": "공용", "part": "신발", "character": "공용"},
    {"id": "900006000", "desc": "망토_일반_01_제작", "grade": "COMMON", "name": "숲지기의 망토", "job": "공용", "part": "망토", "character": "공용"},
    {"id": "900007000", "desc": "목걸이_일반_01", "grade": "COMMON", "name": "초심자의 목걸이", "job": "공용", "part": "목걸이", "character": "공용"},
    {"id": "900008000", "desc": "귀걸이_일반_01", "grade": "COMMON", "name": "초심자의 귀걸이", "job": "공용", "part": "귀걸이", "character": "공용"},
    {"id": "900009000", "desc": "팔찌_일반_01", "grade": "COMMON", "name": "초심자의 팔찌", "job": "공용", "part": "팔찌", "character": "공용"},
    {"id": "900010000", "desc": "반지_일반_01", "grade": "COMMON", "name": "초심자의 반지", "job": "공용", "part": "반지", "character": "공용"},
    {"id": "900011000", "desc": "벨트_일반_01", "grade": "COMMON", "name": "초심자의 벨트", "job": "공용", "part": "벨트", "character": "공용"},
    {"id": "900012000", "desc": "꾳_일반_01", "grade": "COMMON", "name": "야생 마력꽃", "job": "공용", "part": "꽃", "character": "공용"},
    {"id": "900014000", "desc": "견장_일반_01", "grade": "COMMON", "name": "낡은 견장", "job": "공용", "part": "견장", "character": "공용"},
    {"id": "900015000", "desc": "깃털_일반_01", "grade": "COMMON", "name": "검은 깃털", "job": "공용", "part": "깃털", "character": "공용"},
    
    # 더 다양한 등급의 장비 추가 (예시)
    # 고급 공용 장비
    {"id": "901002000", "desc": "머리_고급_01", "grade": "ADVANCE", "name": "견고한 모험자의 캡", "job": "공용", "part": "머리", "character": "공용"},
    {"id": "901003000", "desc": "가슴_고급_01", "grade": "ADVANCE", "name": "견고한 모험자의 전투복", "job": "공용", "part": "가슴", "character": "공용"},
    {"id": "901004000", "desc": "장갑_고급_01", "grade": "ADVANCE", "name": "견고한 모험자의 전투 장갑", "job": "공용", "part": "장갑", "character": "공용"},
    {"id": "901005000", "desc": "신발_고급_01", "grade": "ADVANCE", "name": "견고한 모험자의 전투 장화", "job": "공용", "part": "신발", "character": "공용"},
    
    # 희귀 공용 장비
    {"id": "902002000", "desc": "머리_희귀_01", "grade": "RARE", "name": "화려한 모험자의 캡", "job": "공용", "part": "머리", "character": "공용"},
    {"id": "902003000", "desc": "가슴_희귀_01", "grade": "RARE", "name": "화려한 모험자의 전투복", "job": "공용", "part": "가슴", "character": "공용"},
    {"id": "902004000", "desc": "장갑_희귀_01", "grade": "RARE", "name": "화려한 연금술사의 장갑", "job": "공용", "part": "장갑", "character": "공용"},
    {"id": "902005000", "desc": "신발_희귀_01", "grade": "RARE", "name": "화려한 모험자의 전투 장화", "job": "공용", "part": "신발", "character": "공용"},
    
    # 영웅 공용 장비
    {"id": "903002000", "desc": "머리_영웅_01", "grade": "EPIC", "name": "광휘 기사단 투구", "job": "공용", "part": "머리", "character": "공용"},
    {"id": "903003000", "desc": "가슴_영웅_01", "grade": "EPIC", "name": "영광의 야수 사냥복", "job": "공용", "part": "가슴", "character": "공용"},
    {"id": "903004000", "desc": "장갑_영웅_01", "grade": "EPIC", "name": "예지의 마나장갑", "job": "공용", "part": "장갑", "character": "공용"},
    {"id": "903005000", "desc": "신발_영웅_01", "grade": "EPIC", "name": "영광의 야수 사냥 정화", "job": "공용", "part": "신발", "character": "공용"},
    
    # 전설 공용 장비
    {"id": "904002000", "desc": "머리전설_01", "grade": "LEGEND", "name": "성스러운 문지기의 투구", "job": "공용", "part": "머리", "character": "공용"},
    {"id": "904003000", "desc": "가슴전설_01", "grade": "LEGEND", "name": "성스러운 문지기의 갑주", "job": "공용", "part": "가슴", "character": "공용"},
    {"id": "904004000", "desc": "장갑전설_01", "grade": "LEGEND", "name": "성스러운 문지기의 건틀렛", "job": "공용", "part": "장갑", "character": "공용"},
    {"id": "904005000", "desc": "신발전설_01", "grade": "LEGEND", "name": "성스러운 문지기의 판금장화", "job": "공용", "part": "신발", "character": "공용"},
    
    # 신화 공용 장비
    {"id": "905002000", "desc": "머리신화_01_제작", "grade": "MYTH", "name": "각성의 수호자 투구", "job": "공용", "part": "머리", "character": "공용"},
    {"id": "905003000", "desc": "가슴신화_01_제작", "grade": "MYTH", "name": "각성의 수호자 갑주", "job": "공용", "part": "가슴", "character": "공용"},
    {"id": "905004000", "desc": "장갑신화_01_제작", "grade": "MYTH", "name": "각성한 수호자 건틀렛", "job": "공용", "part": "장갑", "character": "공용"},
    {"id": "905005000", "desc": "신발신화_01_제작", "grade": "MYTH", "name": "각성한 수호자 판금장화", "job": "공용", "part": "신발", "character": "공용"}
]

# 추가 아이템: 캐릭터별 특화 장비
EXTRA_ITEMS = [
    # 실키라용 장비
    {"id": "100202000", "desc": "실키라_특화_머리", "grade": "EPIC", "name": "실키라의 명예 투구", "job": "공용", "part": "머리", "character": "실키라"},
    {"id": "100203000", "desc": "실키라_특화_가슴", "grade": "EPIC", "name": "실키라의 전투복", "job": "공용", "part": "가슴", "character": "실키라"},
    {"id": "100204000", "desc": "실키라_특화_장갑", "grade": "EPIC", "name": "실키라의 전투 장갑", "job": "공용", "part": "장갑", "character": "실키라"},
    {"id": "100205000", "desc": "실키라_특화_신발", "grade": "EPIC", "name": "실키라의 전투 장화", "job": "공용", "part": "신발", "character": "실키라"},
    
    # 이리시아용 장비
    {"id": "200202000", "desc": "이리시아_특화_머리", "grade": "EPIC", "name": "이리시아의 마력 투구", "job": "공용", "part": "머리", "character": "이리시아"},
    {"id": "200203000", "desc": "이리시아_특화_가슴", "grade": "EPIC", "name": "이리시아의 마력 로브", "job": "공용", "part": "가슴", "character": "이리시아"},
    {"id": "200204000", "desc": "이리시아_특화_장갑", "grade": "EPIC", "name": "이리시아의 마력 장갑", "job": "공용", "part": "장갑", "character": "이리시아"},
    {"id": "200205000", "desc": "이리시아_특화_신발", "grade": "EPIC", "name": "이리시아의 마력 구두", "job": "공용", "part": "신발", "character": "이리시아"},
    
    # 란스용 장비
    {"id": "300202000", "desc": "란스_특화_머리", "grade": "EPIC", "name": "란스의 기사 헬멧", "job": "공용", "part": "머리", "character": "란스"},
    {"id": "300203000", "desc": "란스_특화_가슴", "grade": "EPIC", "name": "란스의 기사 갑옷", "job": "공용", "part": "가슴", "character": "란스"},
    {"id": "300204000", "desc": "란스_특화_장갑", "grade": "EPIC", "name": "란스의 기사 건틀렛", "job": "공용", "part": "장갑", "character": "란스"},
    {"id": "300205000", "desc": "란스_특화_신발", "grade": "EPIC", "name": "란스의 기사 부츠", "job": "공용", "part": "신발", "character": "란스"},
    
    # 직업별 특화 장비
    {"id": "910202000", "desc": "헌터_특화_머리", "grade": "EPIC", "name": "정밀 조준 헬멧", "job": "헌터", "part": "머리", "character": "공용"},
    {"id": "920202000", "desc": "마법사_특화_머리", "grade": "EPIC", "name": "마나 증폭 모자", "job": "마법사", "part": "머리", "character": "공용"},
    {"id": "930202000", "desc": "기사_특화_머리", "grade": "EPIC", "name": "수호자의 헬멧", "job": "기사", "part": "머리", "character": "공용"},
    {"id": "940202000", "desc": "궁수_특화_머리", "grade": "EPIC", "name": "시력 강화 후드", "job": "궁수", "part": "머리", "character": "공용"}
]

# 추가 아이템을 메인 아이템 DB에 통합
ITEM_DB.extend(EXTRA_ITEMS)

# 직업, 등급, 부위별 정보 목록
JOB_LIST = [
    "모두",
    "헌터", "어쌔신", 
    "마법사", "치유사",
    "기사", "전사",
    "궁수", "창병",
    "마검사", "검투사", 
    "도적", "알케미스트",  # 연금술사를 알케미스트로 변경
    "공용"
]

# 캐릭터 목록
CHARACTER_LIST = [
    "모두",
    "실키라",
    "이리시아",
    "란스",
    "라이뉴",
    "데커드",
    "로버",
    "공용"
]

GRADE_LIST = ["모두", "COMMON", "ADVANCE", "RARE", "EPIC", "LEGEND", "MYTH"]

PART_LIST = [
    "모두", "무기", "머리", "가슴", "장갑", "신발", "망토", 
    "목걸이", "귀걸이", "팔찌", "반지", "벨트", "꽃", "견장", "깃털"
]

# 등급별 색상 (Streamlit에서 사용)
GRADE_COLORS = {
    "COMMON": "gray",
    "ADVANCE": "green",
    "RARE": "blue",
    "EPIC": "purple",
    "LEGEND": "orange",
    "MYTH": "red"
}

def get_item_by_id(item_id):
    """아이템 ID로 아이템 정보 검색"""
    for item in ITEM_DB:
        if item["id"] == item_id:
            return item
    return None

def text_similarity(text1, text2):
    """두 텍스트의 유사도 계산 (0~1 사이 값)"""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def search_items_by_name(name):
    """이름으로 아이템 검색 (유사도 기반)"""
    if not name or name.strip() == "":
        return []
    
    name = name.lower()
    
    # 검색 결과 저장 (아이템, 유사도)
    results = []
    
    # 모든 아이템에 대해 이름 유사도 검사
    for item in ITEM_DB:
        # 완전 일치하는 경우
        if name in item["name"].lower():
            similarity = 1.0
        else:
            # 부분 일치 & 유사도 계산
            similarity = text_similarity(name, item["name"])
        
        # 유사도가 0.3 이상인 아이템만 결과에 포함
        if similarity >= 0.3:
            results.append((item, similarity))
    
    # 유사도 기준으로 내림차순 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    
    # 아이템만 추출하여 반환 (유사도 정보 제거)
    items = [item for item, _ in results]
    
    # 결과가 없는 경우 이름에 검색어가 포함된 아이템 찾기 (백업 방법)
    if not items:
        items = [item for item in ITEM_DB if re.search(name, item["name"].lower())]
    
    # 등급에 따라 정렬
    grade_order = {"MYTH": 0, "LEGEND": 1, "EPIC": 2, "RARE": 3, "ADVANCE": 4, "COMMON": 5}
    sorted_items = sorted(items, key=lambda x: (grade_order.get(x["grade"], 99), x["part"], x["name"]))
    
    # 최대 30개까지만 반환
    return sorted_items[:30]

def filter_items(grade=None, job=None, part=None):
    """필터 조건에 맞는 아이템 목록 반환 (개선된 필터링 알고리즘)"""
    # 기본 필터링 - 모든 아이템으로 시작
    filtered = ITEM_DB.copy()
    
    # 1. 등급 필터링 - 지정된 등급만 반환
    if grade and grade != "모두":
        filtered = [item for item in filtered if item["grade"] == grade]
    
    # 2. 직업 필터링 - 지정된 직업만 반환 (공용은 항상 포함)
    if job and job != "모두":
        filtered = [item for item in filtered if item["job"] == job or item["job"] == "공용"]
    
    # 3. 부위 필터링 - 지정된 부위만 반환
    if part and part != "모두":
        filtered = [item for item in filtered if item["part"] == part]
    
    # 필터링 결과가 없을 경우 유사 매칭 시도
    if not filtered:
        # 유사 매칭 결과 저장
        similar_items = []
        filter_text = ""
        
        # 필터 조건 텍스트 구성
        if grade and grade != "모두":
            filter_text += f"{grade} "
        if job and job != "모두":
            filter_text += f"{job} "
        if part and part != "모두":
            filter_text += f"{part} "
        
        # 모든 아이템에 대해 텍스트 유사도 검사
        for item in ITEM_DB:
            item_text = f"{item['grade']} {item['job']} {item['part']}"
            similarity = text_similarity(filter_text, item_text)
            
            # 유사도가 0.3 이상인 아이템만 결과에 포함
            if similarity >= 0.3:
                similar_items.append((item, similarity))
        
        # 유사도가 높은 순으로 정렬
        similar_items.sort(key=lambda x: x[1], reverse=True)
        
        # 아이템만 추출 (유사도 정보 제거)
        filtered = [item for item, _ in similar_items]
    
    # 아이템 정렬 (등급 > 부위 > 이름)
    # MYTH, LEGEND, EPIC, RARE, ADVANCE, COMMON 순서로 정렬 (높은 등급이 먼저)
    grade_order = {"MYTH": 0, "LEGEND": 1, "EPIC": 2, "RARE": 3, "ADVANCE": 4, "COMMON": 5}
    filtered = sorted(filtered, key=lambda x: (grade_order.get(x["grade"], 99), x["part"], x["name"]))
    
    # 최대 30개까지만 반환
    return filtered[:30]