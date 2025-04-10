#!/usr/bin/env python
"""
게임 치트 자동화 프로그램 실행 파일 생성 스크립트
"""
import os
import sys
import shutil
import subprocess
import platform

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print(" 게임 치트 자동화 프로그램 EXE 빌드 유틸리티 ")
    print("=" * 60)
    
    # 현재 경로 확인
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"현재 디렉토리: {current_dir}")
    
    # 필요한 패키지 설치 여부 확인
    try:
        import PyInstaller
        print("PyInstaller가 설치되어 있습니다.")
    except ImportError:
        print("PyInstaller가 설치되어 있지 않습니다. 설치를 시작합니다...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller==6.5.0"])
            print("PyInstaller 설치가 완료되었습니다.")
        except Exception as e:
            print(f"PyInstaller 설치 중 오류가 발생했습니다: {e}")
            input("Enter 키를 누르면 종료합니다...")
            return
    
    # 빌드 설정
    output_dir = os.path.join(current_dir, "dist")
    build_dir = os.path.join(current_dir, "build")
    spec_file = os.path.join(current_dir, "launcher.spec")
    
    # 이전 빌드 제거
    print("이전 빌드 파일 정리 중...")
    for path in [output_dir, build_dir, spec_file]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    # PyInstaller 명령어 구성
    print("EXE 파일 생성 시작...")
    main_script = os.path.join(current_dir, "launcher.py")
    
    # 아이콘 파일 경로 설정
    icon_path = None
    if os.path.exists(os.path.join(current_dir, "icon.ico")):
        icon_path = os.path.join(current_dir, "icon.ico")
    
    # 기본 명령어
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        f"--name=게임치트자동화",
        f"--distpath={output_dir}",
        f"--workpath={build_dir}",
        "--clean",
        # 데이터 파일 추가
        "--add-data", f"{os.path.join(current_dir, 'excel_data')}{os.pathsep}excel_data",
        "--add-data", f"{os.path.join(current_dir, 'templates')}{os.pathsep}templates",
        "--add-data", f"{os.path.join(current_dir, 'requirements.txt')}{os.pathsep}.",
    ]
    
    # streamlit-option-menu 패키지 설치 (모든 플랫폼)
    try:
        print("streamlit-option-menu 패키지 설치 중...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-option-menu"])
        print("streamlit-option-menu 설치 완료")
    except Exception as e:
        print(f"streamlit-option-menu 설치 중 오류: {e}")
    
    # Windows에서 추가 옵션
    if platform.system() == "Windows":
        # 먼저 필수 패키지 설치 여부 확인 및 설치
        print("필수 패키지 설치 확인 중...")
        
        try:
            with open(os.path.join(current_dir, "requirements.txt"), "r", encoding="utf-8") as req_file:
                requirements = req_file.readlines()
        except UnicodeDecodeError:
            # CP949 인코딩을 시도
            with open(os.path.join(current_dir, "requirements.txt"), "r", encoding="cp949") as req_file:
                requirements = req_file.readlines()
        except Exception as e:
            print(f"requirements.txt 파일 읽기 오류: {e}")
            # 직접 패키지 목록 지정
            requirements = [
                "streamlit==1.32.0",
                "pygetwindow==0.0.9",
                "pandas==2.2.1",
                "openpyxl==3.1.2", 
                "PyAutoGUI==0.9.54",
                "pillow==10.2.0",
                "numpy==1.26.4",
                "pyinstaller==6.5.0",
                "streamlit-option-menu==0.3.6"
            ]
        
        # 주석 제거 및 공백 제거
        packages = []
        for req in requirements:
            req = req.strip()
            if req and not req.startswith("#"):
                # 버전 정보 제거
                package = req.split("==")[0]
                packages.append(package)
        
        # 필수 패키지 설치
        for package in packages:
            try:
                print(f"{package} 설치 여부 확인 중...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} 설치 완료")
            except Exception as e:
                print(f"{package} 설치 중 오류: {e}")
        
        # PyInstaller 명령에 필요한 패키지 추가
        cmd.extend([
            "--collect-submodules=streamlit",
            "--collect-submodules=streamlit_option_menu",
            "--collect-submodules=pandas",
            "--collect-submodules=openpyxl",
            "--collect-submodules=pyautogui", 
            "--collect-submodules=pygetwindow",
            "--collect-submodules=PIL",
            "--collect-submodules=numpy",
            "--collect-submodules=tkinter"
        ])
    
    # 아이콘 추가
    if icon_path:
        cmd.extend([f"--icon={icon_path}"])
    
    # 메인 스크립트 추가
    cmd.append(main_script)
    
    # hidden imports 추가
    cmd.extend([
        "--hidden-import=streamlit",
        "--hidden-import=streamlit.web.bootstrap",
        "--hidden-import=streamlit.runtime",
        "--hidden-import=streamlit.runtime.scriptrunner",
        "--hidden-import=streamlit_option_menu",
        "--hidden-import=pandas",
        "--hidden-import=pygetwindow",
        "--hidden-import=openpyxl",
        "--hidden-import=pyautogui",
        "--hidden-import=pillow",
        "--hidden-import=PIL",
        "--hidden-import=PIL._imagingtk",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=numpy",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.scrolledtext",
        "--hidden-import=threading",
        "--hidden-import=subprocess",
        "--hidden-import=time"
    ])
    
    # Windows 운영체제인 경우 추가 설정
    if platform.system() == "Windows":
        cmd.extend([
            "--hidden-import=win32api",
            "--hidden-import=win32con",
            "--hidden-import=win32gui",
            "--hidden-import=pywintypes",
            "--hidden-import=win32com",
            "--hidden-import=pythoncom"
        ])
    
    # 명령 실행
    print(f"실행 명령어: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("\n빌드가 성공적으로 완료되었습니다!")
        
        # 추가 파일 복사
        print("추가 필요 파일 복사 중...")
        exe_dir = os.path.join(output_dir, "게임치트자동화")
        
        # Windows의 경우 venv 환경에서 필요한 DLL을 복사
        if platform.system() == "Windows":
            print("Windows 환경에 필요한 추가 라이브러리 복사 중...")
            try:
                import site
                python_dir = os.path.dirname(sys.executable)
                
                # 필수 DLL 파일 복사
                dll_files = ["python3.dll", "python39.dll", "python310.dll", "python311.dll", 
                            "vcruntime140.dll", "vcruntime140_1.dll"]
                
                for dll in dll_files:
                    dll_path = os.path.join(python_dir, dll)
                    if os.path.exists(dll_path):
                        shutil.copy2(dll_path, exe_dir)
                        print(f"  - {dll} 복사됨")
            except Exception as e:
                print(f"DLL 파일 복사 중 오류 발생: {e}")
        
        files_to_copy = [
            "main.py",
            "auto_controller.py",
            "image_recognition.py",
            "item_database.py",
            "window_manager.py",
            "requirements.txt"
        ]
        
        for file in files_to_copy:
            source = os.path.join(current_dir, file)
            if os.path.exists(source):
                shutil.copy2(source, exe_dir)
                print(f"  - {file} 복사됨")
        
        # 안내 메시지
        print("\n" + "=" * 60)
        print(f"실행 파일 위치: {os.path.join(exe_dir, '게임치트자동화.exe')}")
        print("=" * 60)
        print("\n프로그램을 실행하려면 dist/게임치트자동화 폴더에 있는 '게임치트자동화.exe'를 실행하세요.")
        
    except Exception as e:
        print(f"\n빌드 중 오류가 발생했습니다: {e}")
    
    input("\n종료하려면 Enter 키를 누르세요...")

if __name__ == "__main__":
    main()