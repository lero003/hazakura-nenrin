---
type: nenrin_change
id: v0-5-compaction-summary-decisions
date: 2026-05-04
status: archived
impact: ineffective
related_files:
  - ../../hazakura-dev-bbs/packages/core/src/index.ts
  - ../../hazakura-dev-bbs/apps/cli/src/index.ts
  - ../../hazakura-dev-bbs/apps/web/src/server.ts
review_after:
  tasks: 5
  days: 14
---

# Change: v0.5 Compaction — summary/decisions/open_questions + Compact View

## Changed

- packages/core: readSummary/readDecisions/readOpenQuestions — ファイルシステムから各ファイル読み取り
- packages/core: generateSummaryDraft — スレッド文脈+キーポイント+抽出決定事項+抽出質問を含むテンプレート生成
- packages/core: generateDecisionsDraft — 投稿から決定文を抽出したドラフト
- packages/core: generateOpenQuestionsDraft — 投稿から質問文を抽出したドラフト
- packages/core: extractQuestionsFromPosts/extractDecisionLines — 投稿解析ヘルパー
- apps/cli: hzb summarize / hzb decisions / hzb questions コマンド（標準出力にドラフト）
- apps/web: Compact View（?view=compact、投稿を1行に折りたたみ・クリックで展開）
- apps/web: summary.md / decisions.md / open_questions.md が存在すればスレッド詳細に表示

## Reason

投稿が増えると全文を読むのが困難になるため、要約・決定事項・未解決論点の補助生成が必要。
ただしAIが直接正本を書き換えるのではなく「ドラフト生成→人間が確認→反映」のフローを守る。

## Expected Behavior

- hzb summarize <id> でスレッド文脈を含む要約テンプレートが出力される
- Web UIで ?view=compact により投稿が折りたたまれ、見通しが良くなる
- summary.md を手動で設置すれば Web UI に自動表示される

## Review After

- 5 related task(s)
- 14 day(s)

## Result

Unjudged.
