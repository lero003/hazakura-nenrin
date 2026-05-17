---
type: nenrin_change
id: v0-6-cloudflare-backend-abstraction
date: 2026-05-04
status: archived
impact: ineffective
related_files:
  - ../../hazakura-dev-bbs/packages/git-backend/src/index.ts
  - ../../hazakura-dev-bbs/packages/indexer/src/index.ts
  - ../../hazakura-dev-bbs/apps/web/src/server.ts
  - ../../hazakura-dev-bbs/apps/cli/src/index.ts
review_after:
  tasks: 3
  days: 14
---

# Change: v0.6 Cloudflare Backend Abstraction

## Changed

- packages/git-backend: 新規パッケージ。GitBackendインターフェース + LocalGitBackend (child_process) + GitHubApiBackend (REST API)
- packages/indexer: IndexerBackendインターフェース + LocalSQLiteIndexer (better-sqlite3) + D1IndexerStub (骨格)
- apps/web: `gitSync` 呼び出しを `getGitBackend().sync()` に差し替え（factory経由）
- apps/cli: 同上
- 環境変数: `BBS_GIT_BACKEND=local|github-api` でGitBackend切替、`BBS_INDEXER=local|d1` でIndexerBackend切替
- GitHubApiBackend: ファイルの読み書きをGitHub Contents API経由で実行（fetchベース、Workers互換）

## Reason

Cloudflare Workers では better-sqlite3 (C++ネイティブ) と child_process が使えない。
backendをインターフェースで抽象化し、環境に応じて差し替え可能にする。
v0.6は抽象化層の実装、v0.7でCloudflare上での動作確認。

## Expected Behavior

- デフォルト (BBS_GIT_BACKEND未設定) では既存のLocalGitBackendが使われ、挙動は変わらない
- BBS_GIT_BACKEND=github-api で GitHubApiBackend が使われる（v0.7でCloudflare上で確認）
- IndexerBackendも同様に切替可能（D1はv0.7で実装）

## Review After

- 3 related task(s) — v0.7でCloudflare実デプロイ、v0.8でView拡張
- 14 day(s)

## Result

Reviewed via `review-v0-6-cloudflare-backend-abstraction-service-close`. Judgment: `remove`.
