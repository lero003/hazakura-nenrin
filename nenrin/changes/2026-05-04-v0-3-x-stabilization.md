---
type: nenrin_change
id: v0-3-x-stabilization
date: 2026-05-04
status: observing
impact: unknown
related_files:
  - ../../hazakura-dev-bbs/packages/core/src/index.ts
  - ../../hazakura-dev-bbs/apps/cli/src/index.ts
  - ../../hazakura-dev-bbs/apps/web/src/server.ts
  - ../../hazakura-dev-bbs/packages/indexer/src/index.ts
review_after:
  tasks: 3
  days: 7
---

# Change: v0.3.x 安定化（エラー耐性・シークレットスキャン・gitSync安全性）

## Changed

- packages/core: 全YAMLパーサーに try-catch 追加（1ファイルの破損で全読み込みが停止しなくなった）
- packages/core: Windows改行（\r\n）に対応（frontmatter正規表現を正規化）
- packages/core: readAllThreads / readThread に per-item レジリエンス（壊れたスレッド/投稿をスキップ）
- packages/core: gitSync() が GitSyncResult を返すように変更（成功/失敗を呼び出し側が判断可能に）
- packages/core: gitSync() にコンフリクト検出と中断ロジックを追加
- packages/core: scanForSecrets() 関数を追加（14パターン: OpenAI, Anthropic, GitHub各種, JWT, AWS, Slack, HuggingFace）
- apps/cli: hzb post にシークレットスキャン追加（CLI側でもブロック）
- apps/cli: レンズ一覧をファイルシステムから動的取得（ハードコード廃止）
- apps/cli: hzb sync --dry-run 追加
- apps/cli: バージョン文字列 v0.3.x に更新、HZB_DEBUG でスタックトレース表示
- apps/web: コードブロックレンダリング修正（開閉状態を追跡）
- apps/web: Markdownレンダラ改善（インラインコード、リンク、引用、太字、順序付きリスト）
- apps/web: シークレットスキャンを scanForSecrets() に差し替え（パターン拡充）
- apps/web: 認証情報のログ出力停止
- apps/web: モバイルレイアウト修正（フロートボタン、レスポンシブテーブル）
- apps/web: コピーボタンにトースト通知追加
- apps/web: 代理投稿フォームにレンズ説明を表示、submitted_by のデフォルトを BBS_USER に
- packages/indexer: needsRebuild() が投稿数も検出するよう修正、検索のLIKEワイルドカードエスケープ

## Reason

コード監査で発見された Critical/High な問題（YAMLパースでクラッシュ、gitSyncがコンフリクトを検出せずpush、CLIにシークレットスキャン欠如、コードブロック表示崩れ）を修正。ロードマップのv0.3.x「足場固め」フェーズ。

## Expected Behavior

- 破損したYAMLファイルがあってもBBS全体がクラッシュしない
- gitSync がコンフリクト時に中断し、競合状態のままpushされない
- CLI・Web両方でシークレットがブロックされる
- Web UIでコードブロックが正しく表示される

## Review After

- 3 related task(s) — v0.4, v0.5, v0.6 の実装時に安定性が維持されているか確認
- 7 day(s) — 1週間の運用で新たな問題が出ていないか

## Success Signals

- 破損データによるクラッシュ報告がない
- gitSync のコンフリクトが検出されユーザーに通知される
- シークレットスキャンの誤検出（false positive）が少ない

## Failure Signals

- シークレットスキャンが正当な投稿をブロックしすぎる
- gitSync の新ロジックがエッジケースで失敗する
- needsRebuild が再構築ループを引き起こす

## Result

Unjudged.
