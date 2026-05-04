---
type: nenrin_change
id: agents-roadmap-v0-3-x-update
date: 2026-05-04
status: observing
impact: unknown
related_files:
  - ../../hazakura-dev-bbs/AGENTS.md
  - ../../hazakura-dev-bbs/ROADMAP.md
  - ../../hazakura-dev-bbs/docs/development.md
  - ../../hazakura-dev-bbs/README.md
review_after:
  tasks: 3
  days: 7
---

# Change: AGENTS.md + ROADMAP.md + development docs 整備

## Changed

- AGENTS.md: 開発補助ツール（Habitat / Nenrin）の参照を追加。現在の状態を v0.3.x に更新。ROADMAP.md と docs/development.md へのリンク追加
- ROADMAP.md: 新規作成。チカちゃん案ベースの3フェーズ・10バージョンロードマップ
- docs/development.md: 新規作成。Habitat + Nenrin を使った開発ワークフロー手順
- README.md: 開発状況テーブルを拡張、ROADMAP.md へのリンク追加

## Reason

セッションをまたぐ継続開発で、エージェントが「どこまでできていて次に何をすべきか」を自己判断できるようにするため。Habitat と Nenrin を実際の開発フローに組み込むための手順を明文化した。

## Expected Behavior

- 新しいエージェントが AGENTS.md を読めば、パッケージ構成・命名規則・コマンド一覧がわかる
- ROADMAP.md を見れば次のバージョンの要件がわかる
- docs/development.md のチェックリストに従えば、Habitat スキャン → 実装 → Nenrin 記録 が習慣化される

## Review After

- 3 related task(s) — 次の3バージョン（v0.4, v0.5, v0.6）の実装後に振り返る
- 7 day(s) — 1週間後に実際に使われているか確認

## Success Signals

- エージェントが AGENTS.md を読んで自発的に正しいコマンド（pnpm, tsc, hzb）を選択する
- セッション開始時に Habitat スキャンが実行される
- AGENTS.md/ROADMAP.md 変更時に Nenrin 記録が残される

## Failure Signals

- AGENTS.md が参照されず、エージェントが npm や yarn を使おうとする
- ロードマップと実装が乖離する（ROADMAP.md が更新されない）
- Nenrin 記録が一度も残されない

## Result

Unjudged.
