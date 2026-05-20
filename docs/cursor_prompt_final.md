# 最終仕様プロンプト（現状の画面を再現する）

---

## 【完成版】フロントエンド実装プロンプト

```
@00_project_overview.md と @10_frontend_design.md に従って frontend/ を実装してください。
バックエンドAPI（http://localhost:8002/api/）に疎通すること。

以下の実装要件をすべて厳守してください。

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ vite.config.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━
- ポートは 5173 を指定するが strictPort は設定しない（競合時に自動インクリメントさせる）
  server: {
    port: 5173,
  }

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ src/api/client.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━
- baseURL: 'http://localhost:8002'
- extractError(e: unknown): string を実装
  - ERR_NETWORK → 'バックエンドに接続できません。サーバーが起動しているか確認してください。'
  - response.data.detail が文字列 → そのまま返す
  - response.data.detail が配列（Pydantic 422） → msg を結合して返す
  - それ以外 → '操作に失敗しました'

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ App.vue（シェルレイアウト＋グローバルCSS）
━━━━━━━━━━━━━━━━━━━━━━━━━━
レイアウト：
- 固定サイドバー（幅220px）＋右側メインコンテンツエリア
- <div class="shell"> → <AppNav /> + <div class="main"><RouterView /></div>

CSSカスタムプロパティ（:root）：
--sidebar-w: 220px
--sidebar-bg: #0f172a（濃紺）
--bg: #f1f5f9
--surface: #ffffff
--border: #e2e8f0
--border-strong: #cbd5e1
--text: #0f172a
--text-2: #475569
--text-3: #94a3b8
--primary: #2563eb
--primary-dark: #1d4ed8
--primary-bg: #eff6ff
--green: #16a34a
--green-bg: #f0fdf4
--green-text: #166534
--amber: #d97706
--amber-bg: #fffbeb
--amber-text: #78350f
--red: #dc2626
--red-bg: #fef2f2
--red-text: #991b1b
--slate-bg: #f1f5f9
--slate-text: #475569
--radius: 6px
--radius-lg: 10px
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)

グローバル共通クラス（すべてApp.vueのstyleに定義）：
.page / .page-header / .page-title / .page-desc / .count-badge
.card / .card-header / .card-title / .card-body
.btn / .btn-primary / .btn-secondary / .btn-danger / .btn-ghost / .btn-sm
.form-grid（3カラム） / .field / .span2 / .span3 / .req（赤い*）
.data-table / .row-clickable / .row-selected / .row-detail
.badge / .badge-active（緑）/ .badge-pending（黄）/ .badge-done（グレー）/ .badge-info（青）
.empty-state / .error-banner / .inline-label / .form-actions

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ AppNav.vue（固定ダークサイドバー）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- 背景色：#0f172a（濃紺）
- 上部ブランド：「M」青四角バッジ ＋「要員管理」「Knowledge System」
- セクション1「OVERVIEW」：ダッシュボード / ナレッジ検索 / 稼働マトリクス
- セクション2「MASTER DATA」：社員管理 / 顧客管理 / 案件管理 / アサイン管理
- アクティブ状態：左側に青いボーダー ＋ 薄青背景
- 最下部：「v1.0.0」テキスト

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ router/index.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━
- '/' → '/dashboard' にリダイレクト
- /dashboard / /search / /staffing / /employees / /projects / /clients / /assignments

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ DashboardView（ダッシュボード）
━━━━━━━━━━━━━━━━━━━━━━━━━━
統計カード4枚（横並び）：
- 在籍社員：status≠退職の件数
- 契約期間中：アサインstatus=契約期間中の件数（数字を緑色で表示）
- 内諾：アサインstatus=内諾の件数（数字を黄色で表示）
- 登録案件：案件の総数

下部2カラムレイアウト：
左：「直近のアサイン」テーブル（status≠完了の上位6件）
  列：社員 / 案件 / 期間 / 稼働率 / ステータス
右：「稼働スナップショット（3ヶ月）」
  - 当月〜2ヶ月先の3ヶ月分をマトリクス表示
  - セル色：契約期間中=緑、内諾=黄、空き=ピンク
  - 凡例：契約期間中 / 内諾 / 複数 / 空き

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ StaffingView（稼働マトリクス）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- ページ上部右側に「開始月」「〜」「終了月」のinput[type=month]と「表示」ボタン
- デフォルト：開始月=当月、終了月=当月+5ヶ月（JavaScriptで動的に設定）
- input[type=month]にmin/maxは設定しない
- マトリクス表：行=社員名、列=月名（〇月形式）
- セル表示：
  - 契約期間中：緑背景 ●
  - 内諾：黄背景 ●
  - 複数アサイン：黄背景 ×n
  - 空き：ピンク背景（空白）
- 凡例バーを表の下に表示

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ EmployeeView（社員管理）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- 在籍状況フィルターバー（ピルボタン）：すべて / 在籍 / 退職 / 入社見込み
- テーブル列：社員番号 / 氏名 / クラス / 在籍状況（バッジ）/ 入社日 / 退職日
- バッジ色：在籍=緑 / 入社見込み=青 / 退職=グレー
- 行クリックでフォームに値展開して編集

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ ClientView（顧客管理）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- テーブル列：顧客コード / 顧客名 / 業種 / 従業員規模 / ステータス（バッジ）
- バッジ色：利用=緑 / 利用停止=グレー

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ ProjectView（案件管理）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- テーブル列：案件コード / 案件名 / 役割 / エンド顧客 / 契約企業
- 想定工程はチェックボックス複数選択（カンマ区切りで保存）
- 商流FK（エンド/プライム/中間1/中間2/契約企業）は顧客マスタから選択

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ AssignmentView（アサイン管理）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- ステータスフィルターバー（ピルボタン）：すべて / 契約期間中 / 内諾 / 完了
- フィルターバー右端にCSV出力ボタン
- テーブル列：社員名 / 案件名 / ランク / 稼働率（%表示）/ 開始日 / 終了日 / ステータス / 単価
- 稼働率は Math.round(utilization * 100) + '%' で表示
- フロントバリデーション：稼働率(0<v≤1.0)・開始日≤終了日・単価≥0

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ SearchView（ナレッジ検索）
━━━━━━━━━━━━━━━━━━━━━━━━━━
- 検索条件：フリーワード / 社員（セレクト）/ 顧客（セレクト）/ ステータス（セレクト）
- 検索結果テーブル列：社員名 / クラス / 案件名 / エンド顧客 / 役割 / 期間 / ステータス
- 行クリックで詳細パネルを展開（社員情報・案件情報・商流）
- 結果がある場合にCSV出力ボタンを表示

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ src/utils/csv.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━
export function downloadCsv(headers: string[], rows: string[][], filename: string)
- UTF-8 BOM（﻿）付きCSVをブラウザダウンロード
- セル値はダブルクォートで囲み、値内のダブルクォートはエスケープ

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 出力順序
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 作業計画
2. 作成するファイル一覧
3. 各ファイルの完全な実装コード
4. 起動手順と動作確認手順
```
