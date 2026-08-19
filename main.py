import sys
import os
import tempfile
import subprocess
import hashlib
import base64
import random
import string
import uuid
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QUrl
from PyQt5.QtGui import QFont, QDesktopServices

if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class CodeSplitter:
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def _generate_uuid_name(self):
        uuid_part = str(uuid.uuid4())
        parts = uuid_part.split('-')
        if len(parts) >= 5:
            parts[3] = 'bbc5'
            parts[4] = 'pta5' + ''.join(random.choice('0123456789abcdef') for _ in range(4))
        return '-'.join(parts) + '.tmp'
    
    def _encrypt_code(self, code):
        import zlib
        compressed = zlib.compress(code.encode('utf-8'))
        key = 0x7F
        xor_data = bytearray()
        for byte in compressed:
            xor_data.append(byte ^ key)
        encrypted = base64.b64encode(xor_data).decode('ascii')
        return encrypted
    
    def create_extractor(self, file_path, output_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            encrypted_code = self._encrypt_code(code)
            code_hash = hashlib.sha256(code.encode()).hexdigest()[:8]
            
            extractor_code = self._create_extractor_code(encrypted_code, code_hash)
            extractor_path = os.path.join(output_path, "main.py")
            
            with open(extractor_path, 'w', encoding='utf-8') as f:
                f.write(extractor_code)
            
            return True, extractor_path
            
        except Exception as e:
            return False, str(e)
    
    def _create_extractor_code(self, encrypted_code, code_hash):
        return f'''import os,sys,hashlib,tempfile,random,string,uuid,base64,zlib
encrypted_code={repr(encrypted_code)}
code_hash="{code_hash}"
def decrypt_code(e):
 d=base64.b64decode(e);k=0x7F;x=bytearray()
 for b in d:x.append(b^k)
 return zlib.decompress(x).decode('utf-8')
def g():
 u=str(uuid.uuid4()).split('-')
 if len(u)>=5:u[3]='bbc5';u[4]='pta5'+''.join(random.choice('0123456789abcdef') for _ in range(4))
 return '-'.join(u)+'.tmp'
def r():
 try:
  c=decrypt_code(encrypted_code);td=tempfile.gettempdir();l=len(c);s=[];rem=l
  for i in range(99):
   sz=random.randint(50,max(50,rem//(100-i)*2))
   if sz>rem:sz=rem//2
   s.append(sz);rem-=sz
  s.append(rem);p=[];pos=0
  for sz in s:p.append(c[pos:pos+sz]);pos+=sz
  f=[]
  for i,part in enumerate(p):
   n=g();path=os.path.join(td,n)
   with open(path,'w',encoding='utf-8')as fw:fw.write(part)
   f.append(path)
  cc=''
  for path in f:
   with open(path,'r',encoding='utf-8')as fr:cc+=fr.read()
  h=hashlib.sha256(cc.encode()).hexdigest()[:8]
  if h!=code_hash:print(f"Hash mismatch: {{h}}")
  exec(cc,{{'__name__':'__main__'}})
  for path in f:
   try:os.remove(path)
   except:pass
  return True
 except Exception as e:print(f"Error: {{e}}");import traceback;traceback.print_exc();return False
if __name__=="__main__":
 r()
 try:
  if os.path.exists(__file__):os.remove(__file__)
 except:pass
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HotKit")
        self.setGeometry(500, 250, 400, 250)
        self.setFixedSize(400, 250)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.splitter = CodeSplitter()
        
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: rgb(35, 35, 35);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 12);
            }
        """)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 30);
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel("HotKit")
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: rgba(255, 255, 255, 200);
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        about_btn = QPushButton("About")
        about_btn.setFixedSize(60, 25)
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 8);
                color: rgba(255, 255, 255, 130);
                border: 1px solid rgba(255, 255, 255, 8);
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
                color: rgba(255, 255, 255, 200);
            }
        """)
        about_btn.clicked.connect(self.show_about)
        title_layout.addWidget(about_btn)
        
        min_btn = QPushButton("─")
        min_btn.setFixedSize(30, 25)
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 150);
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
                color: rgba(255, 255, 255, 220);
            }
        """)
        min_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(min_btn)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 150);
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 80);
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        title_bar.setLayout(title_layout)
        main_layout.addWidget(title_bar)
        
        self.content = QWidget()
        self.content.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 5);
            }
        """)
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 15, 20, 15)
        self.content_layout.setSpacing(10)
        self.content.setLayout(self.content_layout)
        
        self.setup_main_page()
        
        main_layout.addWidget(self.content)
        
        self.drag_pos = None
    
    def setup_main_page(self):
        self.clear_content()
        
        self.header = QLabel("HotKit")
        self.header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: rgba(255, 255, 255, 200);
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 10);
        """)
        self.content_layout.addWidget(self.header)
        
        self.file_label = QLabel("Select Python File:")
        self.file_label.setStyleSheet("color: rgba(255, 255, 255, 160); font-size: 11px;")
        self.content_layout.addWidget(self.file_label)
        
        file_row = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 8);
                color: rgba(255, 255, 255, 170);
                border: 1px solid rgba(255, 255, 255, 8);
                border-radius: 4px;
                padding: 5px;
                font-size: 11px;
            }
        """)
        self.file_path.setPlaceholderText("Select .py file...")
        file_row.addWidget(self.file_path)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 12);
                color: rgba(255, 255, 255, 160);
                border: 1px solid rgba(255, 255, 255, 8);
                border-radius: 4px;
                padding: 5px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        file_row.addWidget(browse_btn)
        self.content_layout.addLayout(file_row)
        
        build_btn = QPushButton("Build")
        build_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 12);
                color: rgba(255, 255, 255, 180);
                border: 1px solid rgba(255, 255, 255, 8);
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
            }
        """)
        build_btn.clicked.connect(self.build_file)
        self.content_layout.addWidget(build_btn)
        
        self.content_layout.addStretch()
    
    def clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    subitem = item.layout().takeAt(0)
                    if subitem.widget():
                        subitem.widget().deleteLater()
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Python File", "", "Python Files (*.py)"
        )
        if file_path:
            self.file_path.setText(file_path)
    
    def build_file(self):
        if not self.file_path.text():
            QMessageBox.warning(self, "Warning", "Please select a Python file first.")
            return
        
        try:
            output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if not output_dir:
                return
            
            success, result = self.splitter.create_extractor(self.file_path.text(), output_dir)
            
            if success:
                QMessageBox.information(
                    self, 
                    "Build Complete", 
                    f"File created successfully!\n\n{result}"
                )
            else:
                QMessageBox.critical(self, "Build Failed", result)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to build: {str(e)}")
    
    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About HotKit")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Coded By PR\n- @zlmokah")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: rgb(35, 35, 35);
            }
            QMessageBox QLabel {
                color: rgba(255, 255, 255, 200);
                font-size: 13px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 12);
                color: rgba(255, 255, 255, 180);
                border: 1px solid rgba(255, 255, 255, 8);
                border-radius: 4px;
                padding: 6px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
            }
        """)
        
        telegram_btn = msg.addButton("Telegram", QMessageBox.ActionRole)
        github_btn = msg.addButton("GitHub", QMessageBox.ActionRole)
        close_btn = msg.addButton("Close", QMessageBox.RejectRole)
        
        msg.exec_()
        
        if msg.clickedButton() == telegram_btn:
            QDesktopServices.openUrl(QUrl("https://t.me/hostcost"))
        elif msg.clickedButton() == github_btn:
            QDesktopServices.openUrl(QUrl("https://github.com/zlmokah"))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos is not None:
            delta = QPoint(event.globalPos() - self.drag_pos)
            self.move(self.pos() + delta)
            self.drag_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        self.drag_pos = None
    
    def closeEvent(self, event):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
