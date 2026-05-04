---
type: nenrin_change
id: clarify-tool-roles-agents-primary
date: 2026-05-04
status: observing
impact: unknown
related_files:
  - ../../hazakura-dev-bbs/AGENTS.md
  - ../../hazakura-dev-bbs/docs/development.md
review_after:
  tasks: 5
  days: 14
---

# Change: ツール役割の明確化（AGENTS.md 主役・Habitat 実体差分・Nenrin 後日剪定）

## Changed

- docs/development.md: 冒頭に「開発ツールの役割」セクションを追加
- AGENTS.md: 開発補助ツールの説明に「役割分担」を追記

## Reason

v0.4 までの開発と Habitat/Nenrin の実地テストを通じて、3ツールの関係性が見えた。
それぞれを「全部毎回やる」のではなく、役割に応じた使い分けが必要。

## Expected Behavior

- エージェントはまず AGENTS.md を読み、それで十分なら Habitat はスキップする
- 新しいエージェントが初参加する時だけ Habitat を使う
- Nenrin は後日（変更が5件以上溜まったら）剪定のために使う

## Review After

- 5 related task(s)
- 14 day(s) — 2週間後にこの役割分担が定着しているか確認

## Success Signals

- AGENTS.md が常に最新に保たれている
- Habitat を使わなくても開発がスムーズに進む
- Nenrin に溜まった変更のうち、不要と判断されるものが出てくる（剪定が機能している証拠）

## Failure Signals

- AGENTS.md が更新されず、Habitat の出力と乖離する
- Nenrin の記録だけが増え、一度も剪定されない（レビューサイクルが回っていない）
- ツールの過剰使用（毎回全部やる）で開発速度が落ちる

## Result

Unjudged.
