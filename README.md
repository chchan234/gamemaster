# 게임 치트 자동화 프로그램

게임 내 치트 코드 입력을 자동화하여 게임 진행을 도와주는 프로그램입니다.

## 주요 기능

- 아이템 생성 (엑셀 데이터에서 타입별 필터링 가능)
- 탈것, 정령, 무기소울, 아스터 등 다양한 콘텐츠 생성
- 이동 및 위치 조작
- 전투 능력 향상
- 이미지 인식을 통한 메뉴, 입력창, 버튼 자동 클릭

## 설치 방법

### 방법 1: 윈도우에서 EXE 파일 실행 (권장)

1. 빌드 스크립트를 실행해 EXE 파일을 만듭니다:
```bash
python build_exe.py
```

2. 빌드가 완료되면 `dist/게임치트자동화` 폴더에 `게임치트자동화.exe` 파일이 생성됩니다.
3. 생성된 EXE 파일을 실행하여 프로그램을 시작합니다.

### 방법 2: 소스 코드 직접 실행

#### 1. 필수 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

#### 2. 설치 단계

Windows 환경에서 실행하는 경우:

```bash
# 필요한 패키지 설치
pip install -r requirements.txt
```

#### 3. 실행 방법

```bash
# 런처 실행 (권장)
python launcher.py

# 또는 직접 메인 프로그램 실행
streamlit run main.py
```

## 사용 방법

1. 프로그램을 실행하면 게임 창 선택 화면이 나타납니다.
2. 현재 실행 중인 게임 창을 선택하고 '확인' 버튼을 클릭합니다.
3. 원하는 치트 카테고리와 기능을 선택합니다.
4. 필요한 경우 추가 정보를 입력합니다.
5. '치트 실행' 버튼을 클릭하여 자동으로 게임에 치트 코드를 적용합니다.

## 주의사항

- **중요**: 이 프로그램은 반드시 게임과 같은 컴퓨터에서 로컬로 실행해야 합니다.
- 프로그램 실행 중 마우스를 움직이지 마세요.
- 게임 창이 최소화되지 않도록 주의하세요.
- 이 프로그램은 싱글 플레이어 게임에서만 사용하세요.
- 온라인 게임에서 사용할 경우 계정 제재의 위험이 있습니다.

## 문제 해결

- **윈도우 감지 오류**: Windows 환경에서 실행 시 `pygetwindow` 패키지가 필요합니다. 런처를 통해 자동으로 설치하거나 `pip install pygetwindow==0.0.9` 명령으로 설치하세요.
- **엑셀 파일 로드 실패**: 프로그램 첫 실행 시 자동으로 기본 엑셀 파일을 생성합니다. 오류 발생 시 `excel_data` 폴더 존재 여부를 확인하세요.