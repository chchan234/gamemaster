#!/usr/bin/env python
"""
게임 치트 자동화 프로그램 실행기
"""
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import platform
import threading
import time

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("게임 치트 자동화 프로그램")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 현재 스크립트 경로 및 파이썬 경로 설정
        # PyInstaller가 만든 실행 파일에서 사용할 수 있도록 경로 설정
        if getattr(sys, 'frozen', False):
            # PyInstaller로 패키징된 경우
            self.script_dir = os.path.dirname(sys.executable)
        else:
            # 일반 Python 스크립트로 실행된 경우
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 상단 로고 및 설명
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(pady=20, fill=tk.X)
        
        self.title_label = tk.Label(
            self.header_frame, 
            text="게임 치트 자동화 프로그램", 
            font=("Arial", 18, "bold")
        )
        self.title_label.pack()
        
        self.desc_label = tk.Label(
            self.header_frame,
            text="이 프로그램은 게임 치트 코드 입력을 자동화합니다.\n실행 전 필요한 라이브러리를 확인합니다.",
            font=("Arial", 10),
            justify=tk.CENTER
        )
        self.desc_label.pack(pady=10)
        
        # 메인 컨텐츠 프레임
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # 상태 표시
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(pady=10, fill=tk.X)
        
        # 상태 라벨
        self.status_label = tk.Label(
            self.status_frame,
            text="준비 중...",
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # 진행 상태 표시줄
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.pack(pady=10, padx=20)
        
        # 로그 표시
        self.log_frame = tk.Frame(self.main_frame)
        self.log_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        self.log_label = tk.Label(
            self.log_frame,
            text="로그:",
            anchor="w"
        )
        self.log_label.pack(anchor="w")
        
        self.log_text = tk.Text(
            self.log_frame,
            height=8,
            width=50,
            font=("Consolas", 9),
            bg="#f0f0f0",
            state="disabled"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 스크롤바 추가
        self.scrollbar = ttk.Scrollbar(self.log_text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log_text.yview)
        
        # 버튼 프레임
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)
        
        # 실행 버튼
        self.run_button = ttk.Button(
            self.button_frame,
            text="프로그램 실행",
            command=self.run_program,
            width=20
        )
        self.run_button.pack(side=tk.LEFT, padx=10)
        
        # 환경 설정 버튼
        self.setup_button = ttk.Button(
            self.button_frame,
            text="환경 설정",
            command=self.setup_environment,
            width=20
        )
        self.setup_button.pack(side=tk.LEFT, padx=10)
        
        # 종료 버튼
        self.quit_button = ttk.Button(
            self.button_frame,
            text="종료",
            command=root.destroy,
            width=10
        )
        self.quit_button.pack(side=tk.LEFT, padx=10)
        
        # 초기화
        self.update_status("시작 준비 완료")
        self.check_requirements()
    
    def update_log(self, message):
        """로그 메시지 업데이트"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # 스크롤 최하단으로
        self.log_text.config(state="disabled")
        self.root.update()
    
    def update_status(self, message):
        """상태 메시지 업데이트"""
        self.status_label.config(text=message)
        self.root.update()
    
    def check_requirements(self):
        """필요한 패키지가 설치되어 있는지 확인"""
        self.update_status("환경 검사 중...")
        self.progress["value"] = 0
        
        # PyInstaller로 패키징된 경우, 이미 모든 패키지가 번들링되어 있다고 가정
        if getattr(sys, 'frozen', False):
            self.update_log("패키징된 실행 파일입니다. 모든 필수 패키지가 포함되어 있습니다.")
            self.update_status("모든 패키지가 설치되어 있습니다. 실행 가능합니다.")
            self.run_button.config(state="normal")
            self.missing_packages = []
            self.progress["value"] = 100
            return
            
        required_packages = [
            "streamlit", "pygetwindow", "pandas", "openpyxl", 
            "pyautogui", "pillow", "numpy"
        ]
        
        missing_packages = []
        total = len(required_packages)
        
        for i, package in enumerate(required_packages):
            try:
                self.update_log(f"{package} 확인 중...")
                __import__(package)
                self.update_log(f"✓ {package} 설치됨")
            except ImportError:
                self.update_log(f"✗ {package} 설치 필요")
                missing_packages.append(package)
            
            self.progress["value"] = (i + 1) * 100 / total
            self.root.update()
            time.sleep(0.1)  # UI 업데이트를 위한 지연
        
        if missing_packages:
            self.update_status(f"{len(missing_packages)}개 패키지 설치 필요")
            self.run_button.config(state="disabled")
        else:
            self.update_status("모든 패키지가 설치되어 있습니다. 실행 가능합니다.")
            self.run_button.config(state="normal")
        
        self.missing_packages = missing_packages
    
    def setup_environment(self):
        """환경 설정 - 필요한 패키지 설치"""
        if not hasattr(self, 'missing_packages') or not self.missing_packages:
            messagebox.showinfo("환경 설정", "모든 필수 패키지가 이미 설치되어 있습니다.")
            return
        
        self.update_status("패키지 설치 중...")
        self.progress["value"] = 0
        self.run_button.config(state="disabled")
        self.setup_button.config(state="disabled")
        
        def install_thread():
            total = len(self.missing_packages)
            
            for i, package in enumerate(self.missing_packages):
                try:
                    self.update_log(f"{package} 설치 중...")
                    
                    # pip 명령어 실행
                    process = subprocess.Popen(
                        [sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                    
                    stdout, stderr = process.communicate()
                    
                    if process.returncode == 0:
                        self.update_log(f"✓ {package} 설치 완료")
                    else:
                        self.update_log(f"✗ {package} 설치 실패: {stderr}")
                
                except Exception as e:
                    self.update_log(f"✗ {package} 설치 중 오류: {str(e)}")
                
                self.progress["value"] = (i + 1) * 100 / total
            
            # 설치 완료 후 상태 업데이트
            self.check_requirements()
            self.setup_button.config(state="normal")
        
        # 별도 스레드로 실행
        threading.Thread(target=install_thread, daemon=True).start()
    
    def run_program(self):
        """프로그램 실행"""
        self.update_status("프로그램 실행 중...")
        self.run_button.config(state="disabled")
        
        def run_thread():
            try:
                main_script = os.path.join(self.script_dir, "main.py")
                self.update_log(f"프로그램 실행: {main_script}")
                
                # 실행 환경 확인
                if getattr(sys, 'frozen', False):
                    # PyInstaller로 패키징된 경우, Python 실행 파일은 함께 번들링된 버전 사용
                    python_exe = os.path.join(self.script_dir, "python")
                    if platform.system() == "Windows":
                        python_exe += ".exe"
                    
                    if not os.path.exists(python_exe):
                        python_exe = sys.executable
                else:
                    python_exe = sys.executable
                
                # Streamlit 실행 - PyInstaller 패키징 환경에 맞게 최적화
                if getattr(sys, 'frozen', False):
                    try:
                        # 패키지 경로 설정
                        streamlit_dir = os.path.join(self.script_dir, "streamlit")
                        
                        # 환경 변수 설정 - Streamlit이 필요한 리소스 찾을 수 있도록
                        env = os.environ.copy()
                        env["PYTHONPATH"] = self.script_dir
                        
                        self.update_log("패키징된 모드에서 직접 실행 시도...")
                        # 직접 main.py 실행 시도
                        process = subprocess.Popen(
                            [python_exe, main_script],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            env=env
                        )
                    except Exception as e:
                        self.update_log(f"실행 오류: {str(e)}")
                        messagebox.showerror("오류", f"프로그램 실행 중 오류가 발생했습니다: {str(e)}")
                        raise
                else:
                    # 일반 Python 환경에서는 기존 방식대로 Streamlit 실행
                    try:
                        self.update_log(f"Python 경로: {python_exe}")
                        process = subprocess.Popen(
                            [python_exe, "-m", "streamlit", "run", main_script],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                    except Exception as e:
                        self.update_log(f"Streamlit 실행 오류: {str(e)}")
                        # 백업 방법: 직접 Python 스크립트 실행
                        try:
                            self.update_log("대체 방법으로 직접 실행 시도...")
                            process = subprocess.Popen(
                                [python_exe, main_script],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True
                            )
                        except Exception as e2:
                            self.update_log(f"대체 실행 방법도 실패: {str(e2)}")
                            raise
                
                # 초기 출력 몇 줄 읽기
                for _ in range(10):
                    line = process.stdout.readline()
                    if line:
                        self.update_log(line.strip())
                        # 로컬 URL을 찾으면 표시
                        if "Local URL:" in line:
                            url = line.strip().split("Local URL:")[1].strip()
                            self.update_status(f"실행 중: {url}")
                            break
                
                # 메인 프로세스가 끝날 때까지 기다리지 않고 계속 실행
                self.update_log("프로그램이 새 창에서 실행되었습니다.")
                
            except Exception as e:
                self.update_log(f"프로그램 실행 중 오류: {str(e)}")
                messagebox.showerror("오류", f"프로그램 실행 중 오류가 발생했습니다: {str(e)}")
            
            self.run_button.config(state="normal")
        
        # 별도 스레드로 실행
        threading.Thread(target=run_thread, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()