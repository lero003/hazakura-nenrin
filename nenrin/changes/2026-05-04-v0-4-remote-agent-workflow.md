---
type: nenrin_change
id: v0-4-remote-agent-workflow
date: 2026-05-04
status: archived
impact: ineffective
related_files:
  - ../../hazakura-dev-bbs/packages/schema/src/index.ts
  - ../../hazakura-dev-bbs/packages/core/src/index.ts
  - ../../hazakura-dev-bbs/apps/cli/src/index.ts
  - ../../hazakura-dev-bbs/scripts/run-codex.sh
  - ../../hazakura-dev-bbs/scripts/run-opencode.sh
review_after:
  tasks: 3
  days: 7
---

# Change: v0.4 Remote Agent Workflow（遠隔エージェント参加）

## Changed

- packages/schema: PostFrontmatter に `run_id` フィールドを追加（オプショナル）
- packages/core: `generateRunId(runtime)` 関数を追加（フォーマット: `YYYY-MM-DDThh-mm-{runtime}`）
- packages/core: CreatePostOptions に `runId` を追加、createPost で frontmatter に書き込み
- apps/cli: `hzb agent run` コマンドを追加（packet生成 → agent実行 → 投稿 → sync の4ステップを1コマンドで）
- apps/cli: agent run は codex-cli / opencode の両方に対応
- apps/cli: agent run にシークレットスキャン・エラーハンドリング完備、`--no-sync` オプション付き
- scripts/run-codex.sh: codex-cli 用テンプレート（BBS Packet→codex実行→投稿→sync）
- scripts/run-opencode.sh: opencode 用テンプレート（同様）

## Reason

別PC・別エージェントからBBSに参加する際、3ステップ（packet生成→agent実行→投稿）を手動でやるのは手間。
`hzb agent run` またはシェルスクリプトで半自動化することで、参加の敷居を下げる。
`run_id` で「どの実行がどの投稿を生んだか」を追跡可能にする。

## Expected Behavior

- `hzb agent run --thread <id> --runtime codex-cli` で packet→codex→post→sync が自動で走る
- 別PCで `./scripts/run-codex.sh --thread <id> --lens implementation` を実行すれば同じ動き
- 投稿の frontmatter に `run_id: 2026-05-04T12-30-codex-cli` が自動記録される

## Review After

- 3 related task(s) — v0.5, v0.6, v0.7 実装時にエージェント参加がスムーズか確認
- 7 day(s) — 1週間以内に実際に別PCから参加してみる

## Success Signals

- `hzb agent run` がエラーなく最後まで完了する
- codex-cli / opencode 以外の runtime の追加が容易（インターフェースの拡張で対応可能）
- `run_id` が正しく記録され、後からどの実行かを特定できる

## Failure Signals

- agent の出力にシークレットが含まれてブロックされる頻度が高い（→プロンプト改善必要）
- agent が途中で失敗した時に中途半端な状態（packet生成だけされて投稿なし）が残る
- shell スクリプトの移植性問題（Linux と macOS で挙動が異なる）

## Result

Reviewed via `review-v0-4-remote-agent-workflow-service-close`. Judgment: `remove`.
