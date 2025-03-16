import PyInstaller.__main__
import os

# 現在のディレクトリを基準にする
base_path = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'desktop_app.py',
    '--onefile',
    '--windowed',
    '--name=JWT認証アプリ',
    # 隠れた依存関係を明示的に含める
    '--hidden-import=passlib.handlers.bcrypt',  
    '--hidden-import=bcrypt',
])
