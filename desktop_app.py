import os
import sys
import threading
import webview
import uvicorn

# バックエンドをインポートする前にパスを調整
sys.path.insert(0, os.path.dirname(__file__))

# bcryptモジュールが正しくロードされているか確認
try:
    import bcrypt
    import passlib.handlers.bcrypt
    print("BCrypt modules loaded successfully")
except ImportError as e:
    print(f"Warning: {e}")
    print("Trying alternative import method...")
    # PyInstallerでの実行時に必要な場合がある特別な処理
    if getattr(sys, 'frozen', False):
        # sys.frozenはPyInstallerで実行している場合にTrueになる
        print("Running in PyInstaller bundle, adjusting imports...")
        # 必要に応じて追加のパスやモジュール読み込み処理

# アプリのインポート
from backend.main import app as fastapi_app

# フロントエンドのビルドディレクトリ
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend", "dist")

# バックエンドサーバーの設定
HOST = "127.0.0.1"
PORT = 8000

def run_backend():
    """バックエンドのFastAPIサーバーを実行"""
    uvicorn.run(fastapi_app, host=HOST, port=PORT)

def get_frontend_url():
    """フロントエンドURL（ビルドファイルまたは開発サーバー）を取得"""
    if os.path.exists(FRONTEND_DIR):
        # プロダクションモード: ビルドされたファイルを使用
        return f"http://{HOST}:{PORT}"
    else:
        # 開発モード: Vite開発サーバーを使用
        return f"http://localhost:5173"

def main():
    # バックエンドを別スレッドで起動
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # ウィンドウタイトル
    title = "JWT認証アプリケーション"
    
    # WebViewを初期化
    webview.create_window(
        title=title,
        url=get_frontend_url(),
        width=1024,
        height=768,
        resizable=True,
        min_size=(800, 600),
        text_select=True
    )
    
    # WebViewを実行
    webview.start(debug=True)

if __name__ == "__main__":
    main()
