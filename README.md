# JWT認証アプリ

このプロジェクトはVite + Reactのフロントエンドと、FastAPIバックエンドを使用したシンプルなJWT認証システムを実装したサンプルアプリケーションです。

## 機能

- ユーザー登録機能
- ユーザーログイン機能（JWTトークン発行）
- 認証が必要なダッシュボード画面
- JWTを使った保護されたAPIエンドポイント

## 技術スタック

### フロントエンド
- Vite
- React
- JavaScript
- axios（APIリクエスト用）

### バックエンド
- FastAPI
- SQLAlchemy（ORM）
- PyJWT（JWTの生成・検証）
- passlib（パスワードハッシュ化）

## セットアップ手順

### バックエンド

1. 必要なパッケージのインストール
```bash
cd backend
pip install -r requirements.txt
```

2. サーバーの起動
```bash
uvicorn main:app --reload
```
バックエンドは http://localhost:8000 で起動します。
APIドキュメントは http://localhost:8000/docs で閲覧できます。

### フロントエンド

1. 必要なパッケージのインストール
```bash
cd frontend
npm install
```

2. 開発サーバーの起動
```bash
npm run dev
```
フロントエンドは通常 http://localhost:5173 で起動します。

## フロントエンドのセットアップ手順

1. Viteを使ってReactプロジェクトを作成
```bash
npm create vite@latest frontend -- --template react
```

2. プロジェクトディレクトリに移動
```bash
cd frontend
```

3. 必要なパッケージのインストール
```bash
npm install
npm install axios react-router-dom
```

4. 開発サーバーの起動
```bash
npm run dev
```

5. ブラウザで http://localhost:5173 を開くとアプリケーションが表示されます

## APIエンドポイント

- `POST /api/register` - ユーザー登録
- `POST /api/login` - ユーザーログイン（JWTトークン取得）
- `GET /api/users/me` - 現在のユーザー情報取得（要認証）

## JWTの仕組み

1. ユーザーがログインすると、サーバーはJWTトークンを発行します
2. クライアントはトークンをローカルストレージに保存します
3. 保護されたリソースにアクセスする際、トークンをAuthorizationヘッダーに含めます
4. サーバーはトークンを検証し、有効であればリクエストを処理します
5. トークンの有効期限が切れると、ユーザーは再度ログインする必要があります

## フォルダ構造の説明

### バックエンド
- `main.py` - FastAPIのメインアプリケーション
- `auth.py` - 認証関連のロジックとJWT処理
- `models.py` - データベースモデル
- `schemas.py` - Pydanticスキーマ（リクエスト/レスポンスモデル）

### フロントエンド
- `src/components/` - Reactのコンポーネント
  - `Login.jsx` - ログインフォームのコンポーネント
  - `Register.jsx` - 登録フォームのコンポーネント
  - `Dashboard.jsx` - ダッシュボードのコンポーネント
- `src/services/` - APIとの通信を行うサービス
- `src/App.js` - メインのReactアプリケーション
