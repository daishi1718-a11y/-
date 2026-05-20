# Cursor 実装プロンプト集

---

## 【1】バックエンド実装プロンプト

```
@00_project_overview.md と @20_backend_design.md に従って backend/ を実装してください。

以下の実装要件を厳守してください：

### ディレクトリ構成
backend/
  app/
    __init__.py
    main.py
    database.py
    models.py
    schemas.py
    routers/
      __init__.py
      employees.py
      clients.py
      projects.py
      assignments.py
      staffing.py
      search.py
  requirements.txt

### requirements.txt の内容（バージョン固定なし）
fastapi
uvicorn[standard]
sqlalchemy
pydantic

### database.py の必須実装
- SQLiteのDBファイルパスは絶対パスで指定すること（相対パスだと起動ディレクトリによってDBが見つからない）
- SQLiteの外部キー制約はデフォルトOFFのため、以下のイベントリスナーで必ず有効化すること：
  @event.listens_for(engine, "connect")
  def set_sqlite_pragma(dbapi_connection, connection_record):
      cursor = dbapi_connection.cursor()
      cursor.execute("PRAGMA foreign_keys=ON")
      cursor.close()

### schemas.py の必須実装（Pydantic v2）
- field_validator と model_validator を使用
- utilization: 0より大きく1.0以下でなければ422エラー
- unit_price: 0以上でなければ422エラー（nullは許容）
- start_date <= end_date でなければ422エラー（model_validator(mode='after')で実装）
- 文字列必須フィールドは空文字を拒否すること
- バリデーションエラーメッセージはすべて日本語にすること

### main.py の必須実装
- CORSのallow_originsは ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"] の3つを許可すること（Viteがポートを自動インクリメントする場合があるため）
- SQLAlchemyのIntegrityErrorをグローバルキャッチして409レスポンスを返すこと：
  - "UNIQUE constraint failed" が含まれる場合：「同じコードがすでに登録されています（{field}）」
  - それ以外：「データの整合性エラーが発生しました」

### routers/projects.py の必須実装
- POST/PUTの際に end_client_id, prime_client_id, mid1_client_id, mid2_client_id, contract_client_id の5つのFK列について、非NULLの場合はclientsテーブルに存在するか確認し、存在しなければ404を返すこと

### routers/staffing.py の必須実装
- from_month > to_month の場合は422エラーを返すこと
- 同一月に複数のアサインが存在する場合：
  - statusは優先度順（契約期間中 > 内諾）で最上位を採用
  - project_nameは「 / 」区切りで結合
  - countフィールドに件数を設定すること

### routers/assignments.py の必須実装
- GET一覧はjoinedload(employee)・joinedload(project)でN+1問題を回避すること
- レスポンスにemployee_name・project_nameを含めること

### routers/search.py の必須実装
- クライアント情報のN+1を防ぐため、使用されているclient_idを事前に一括取得してdictに格納してから使用すること
- SearchResultはrouters/search.py内のローカルPydanticモデルとして定義すること（schemas.pyには入れない）

### 出力順序
1. 作業計画
2. 作成するファイル一覧
3. 各ファイルの完全な実装コード
4. 起動手順と動作確認手順（Swagger URLを含む）
```

---

## 【2】フロントエンド実装プロンプト

```
@00_project_overview.md と @10_frontend_design.md に従って frontend/ を実装してください。
バックエンドAPI（http://localhost:8000/api/）に疎通すること。

以下の実装要件を厳守してください：

### vite.config.ts の必須設定
- サーバーポートを5173に固定すること（ポートがズレるとCORSエラーになる）：
  server: {
    port: 5173,
    strictPort: true,
  }

### src/api/client.ts の必須実装
- axiosのbaseURLは 'http://localhost:8000' に設定
- extractError(e: unknown): string を実装すること：
  - AxiosErrorのresponse.data.detailが文字列 → そのまま返す
  - detailが配列（Pydantic 422） → msg を結合して返す
  - ERR_NETWORK → 'バックエンドに接続できません。サーバーが起動しているか確認してください。'
  - それ以外 → '操作に失敗しました'

### App.vue の必須実装
- シェルレイアウト：固定サイドバー（220px）＋メインコンテンツエリア
- グローバルCSSをstyleタグに定義（scoped不要）
- CSSカスタムプロパティ（:root）でデザイントークンを定義
- 以下の共通クラスをグローバルに定義すること：
  .page / .page-header / .page-title / .page-desc / .count-badge
  .card / .card-header / .card-title / .card-body
  .btn / .btn-primary / .btn-secondary / .btn-danger / .btn-ghost / .btn-sm
  .form-grid / .field / .span2 / .span3 / .req
  .data-table / .row-clickable / .row-selected / .row-detail
  .badge / .badge-active / .badge-pending / .badge-done / .badge-info
  .empty-state / .error-banner / .inline-label / .form-actions

### src/components/AppNav.vue の必須実装
- 固定サイドバー（左固定、幅220px、ダーク背景 #0f172a）
- セクション：OVERVIEW（ダッシュボード/ナレッジ検索/稼働マトリクス）とMASTER DATA（社員/顧客/案件/アサイン管理）
- RouterLinkでアクティブ状態を視覚的に区別（左ボーダー＋背景色変化）

### router/index.ts の必須実装
- '/' → '/dashboard' にリダイレクト
- 全7ルートを定義：/dashboard, /search, /staffing, /employees, /projects, /clients, /assignments

### 各Viewの必須実装
- すべてのViewで <script setup lang="ts"> を使用
- エラー表示は error-banner クラスを使用
- データ取得失敗は extractError() で日本語メッセージを表示
- テーブル行クリックでフォームに値を展開する編集フロー

### src/utils/csv.ts の実装
以下の関数を実装すること：
export function downloadCsv(headers: string[], rows: string[][], filename: string) {
  // UTF-8 BOM付きCSVをブラウザダウンロード
  // BOM: '﻿' をファイル先頭に付与すること（Excelで文字化けを防ぐ）
}

### AssignmentView の必須実装
- 稼働率は Math.round(utilization * 100) + '%' で表示
- フロントバリデーション：utilization(0<v≤1.0)、start_date≤end_date、unit_price≥0

### 出力順序
1. 作業計画
2. 作成するファイル一覧
3. 各ファイルの完全な実装コード
4. 起動手順と動作確認手順
```

---

## 【3】README作成プロンプト

```
@00_project_overview.md をもとに README.md を作成してください。

以下の内容を含めること：

### 必須セクション
1. プロジェクト概要（1〜2行）
2. 技術スタック
3. 初回セットアップ手順（Windows向け。コマンドはコピペで実行できる形式）
   - Git / Python / Node.js のインストール案内（URLつき）
   - git clone のコマンド（<>などの記号を使わないこと）
   - フォルダ移動は cd コマンドのフルパスで記載すること（cd - は使わない）
4. 毎回の起動手順
   - ターミナル①（バックエンド）
   - ターミナル②（フロントエンド）
5. アクセスURL一覧
   - アプリ: http://localhost:5173
   - API Swagger: http://localhost:8000/docs
6. 画面一覧と各画面の説明

### 注意事項として明記すること
- バックエンドとフロントエンドは別々のターミナルで起動すること
- バックエンドが起動していないとフロントに「バックエンドに接続できません」と表示される
- Viteのポートは5173に固定されているため、他のプロセスが5173を使用中の場合はエラーになる
```

---

## 【4】検証項目・Playwright セットアップ プロンプト

### Step 1: Playwright導入（先に実行）
```
Playwrightをこのプロジェクトに導入してください。E2Eテストが実行できる状態までセットアップしてください。

条件：
- テストファイルの配置場所は frontend/e2e/ とすること
- テスト対象URL: http://localhost:5173
- バックエンドURL: http://localhost:8000
- TypeScriptで記述すること
- package.json にテスト実行スクリプト（"test:e2e"）を追加すること
- セットアップ後、動作確認用のサンプルテスト（ダッシュボードが表示されるか確認するだけのもの）を1つ作成すること
```

### Step 2: 検証項目一覧作成（Step 1完了後に実行）
```
@00_project_overview.md / @10_frontend_design.md / @20_backend_design.md に基づいて
PoC向けの検証項目一覧をMarkdown形式で docs/test_cases.md に作成してください。

条件：
- フロントエンド検証項目とバックエンド検証項目を分けて記載
- CRUD（一覧・新規登録・更新・削除）をすべて網羅すること
- 正常系だけでなく異常系（空入力・不正値・存在しないID等）も網羅すること
- PoC前提のため粒度は実務的に過剰にならないよう調整すること（1機能あたり5〜10項目程度）
- MECE（漏れなくダブりなく）を意識すること
- 各項目は「操作手順 / 期待結果」の形式で記載すること

対象画面（フロントエンド）：
- ダッシュボード
- ナレッジ検索
- 稼働マトリクス
- 社員管理
- 顧客管理
- 案件管理
- アサイン管理

対象API（バックエンド）：
- /api/employees
- /api/clients
- /api/projects
- /api/assignments
- /api/staffing/matrix
- /api/search
```
