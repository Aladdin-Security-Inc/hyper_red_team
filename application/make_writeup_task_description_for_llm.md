# How to Write and Extend the Project Writeup

This document provides a guide for LLMs on how to maintain and extend the `writeup.md` for the Kaggle OpenAI Red-Team Competition.

## 1. Current Structure and Core Concepts

The `writeup.md` is structured as a concise academic paper to effectively communicate our findings to the judges. The core argument is that **our methodology reveals deeper, emergent vulnerabilities in agentic systems that simple prompt-response tests would miss.**

-   **Introduction:** States the problem (traditional testing is insufficient for agentic AI) and introduces our solution (custom testing harnesses). It briefly introduces our key findings by name.
-   **Methodology:** This is a critical section. It frames our `TDD Harness` and `Contextual Ambiguity Framework` not just as scripts, but as **novel methodologies**. This directly targets the "Methodological Insight" scoring criterion.
-   **Summary of Findings:** A high-level overview of each vulnerability we've discovered. This allows judges to quickly grasp the scope of our work.
-   **Detailed Finding Sections:** Each finding has its own dedicated section. This is where we prove the value of our discovery. The structure for each is identical and must be followed:
    -   **Overview:** A clear, concise explanation of the vulnerability.
    -   **Figure Placeholder:** A reminder to include a visual that explains the finding.
    -   **Scoring Criteria Breakdown:** Explicitly addresses **Severity, Breadth, and Novelty**, using the competition's language and providing clear justifications for our self-assessed scores.
-   **Reproducibility and Conclusion:** These sections finalize the report by emphasizing the scientific rigor of our work and its broader impact on AI safety.

## 2. Guiding Principles for Writing

When adding or editing content, adhere to the following principles:

1.  **Target the Judging Criteria:** Always write with the official scoring criteria in mind:
    -   `Severity of Harm`
    -   `Breadth of Harm`
    -   `Novelty`
    -   `Reproducibility`
    -   `Methodological Insight`
    -   `Report Clarity`
2.  **Maintain an Academic Tone:** Use a formal, structured, and evidence-based writing style. The structure should be logical and easy to follow.
3.  **Focus on Impact and Novelty:** Do not just describe *what* the model did. Explain *why it matters*. What is the real-world harm? Why is this discovery new and important?
4.  **Frame Tools as "Methodology":** Our key contribution is not just the findings, but *how* we found them. Our harnesses are a new method for red-teaming, and this should be emphasized.

## 3. How to Add a New Finding

Follow these steps precisely to ensure consistency:

1.  **Give it a Name:** Create a clear, impactful name for the vulnerability (e.g., "Cognitive Stagnation").
2.  **Update the Summary:** Add a new bullet point to the "3. Summary of Findings" section that briefly describes the new finding.
3.  **Create the New Section:** Find the last "Detailed Finding" section. Create a new section directly after it. Copy the exact format below and fill in the details for your new finding.

    ```markdown
    ## X. Detailed Finding N: [Name of Your Finding]

    **Overview:** [Explain the vulnerability clearly and concisely. What is the core problem? How is it triggered?]

    `[Insert figure: A descriptive placeholder for a diagram, chart, or graph that visually explains your finding.]`

    -   **Severity (X/10):** [Justify the score. What is the potential real-world harm? Be specific (e.g., financial loss, data destruction, system outages).]
    -   **Breadth (X/10):** [Justify the score. How many users or systems could this affect? Is it a general problem or specific to one domain?]
    -   **Novelty (X/10):** [Justify the score. Why is this different from known vulnerabilities like simple jailbreaking? Does it reveal a new class of problem or a new attack vector?]
    ```
4.  **Update Section Numbers:** Renumber all subsequent sections (including the new one, Reproducibility, and Conclusion) so they are sequential.
5.  **Review:** Read through the entire document to ensure a consistent tone, logical flow, and compelling narrative.

---
---

# (日本語版) `writeup.md` の執筆・拡張ガイド

このドキュメントは、Kaggle OpenAI Red-Teamコンペティション用の`writeup.md`をLLMが維持・拡張するためのガイドです。

## 1. 現在の構成とコアコンセプト

`writeup.md`は、我々の発見を審査員に効果的に伝えるため、簡潔な学術論文の形式で構成されています。中心的な主張は、**「我々の方法論は、単純なプロンプト応答テストでは見逃されるであろう、エージェントシステムにおけるより深く創発的な脆弱性を明らかにする」**という点です。

-   **序論(Introduction):** 問題提起（従来テストはエージェントAIに不十分）と解決策（カスタムテストハーネス）を提示し、主要な発見を名前を挙げて紹介します。
-   **方法論(Methodology):** 極めて重要なセクションです。`TDDハーネス`と`文脈的曖昧性フレームワーク`を単なるスクリプトではなく、**新規な方法論**として位置づけます。これは評価基準の「方法論的洞察」を直接的に狙うものです。
-   **発見の概要(Summary of Findings):** 我々が発見した各脆弱性のハイレベルな概要です。これにより、審査員は我々の研究の全体像を迅速に把握できます。
-   **各発見の詳細(Detailed Finding Sections):** 各発見には独立したセクションが割り当てられます。ここで我々は発見の価値を証明します。各セクションの構成は統一されており、厳密に従う必要があります。
    -   **概要(Overview):** 脆弱性の明確かつ簡潔な説明。
    -   **図のプレースホルダー:** 発見を視覚的に説明する図を挿入するリマインダー。
    -   **評価基準の分析:** コンペの言葉を使い、**深刻度(Severity)、影響範囲(Breadth)、新規性(Novelty)**に明確に言及し、自己評価スコアの正当性を記述します。
-   **再現性と結論(Reproducibility and Conclusion):** 我々の研究の科学的な厳密性と、AI安全性への広範な影響を強調してレポートを締めくくります。

## 2. 執筆の基本方針

内容を追加・編集する際は、以下の原則に従ってください。

1.  **審査基準を狙う:** 常に公式の評価基準を意識して執筆します。
    -   `Severity of Harm` (危害の深刻度)
    -   `Breadth of Harm` (危害の広範性)
    -   `Novelty` (新規性)
    -   `Reproducibility` (再現性)
    -   `Methodological Insight` (方法論的洞察)
    -   `Report Clarity` (報告の明瞭さ)
2.  **学術的なトーンを維持:** フォーマルで構造化され、証拠に基づいた文章スタイルを用います。
3.  **インパクトと新規性に焦点を当てる:** モデルが*何をしたか*をただ記述するのではなく、*なぜそれが重要なのか*を説明します。現実世界での潜在的な危害は何か？なぜこの発見は新しく、重要なのか？
4.  **ツールを「方法論」として位置づける:** 我々の主要な貢献は発見そのものだけでなく、*それをどのように発見したか*です。我々のハーネスはレッドチームの新しい手法であり、これを強調すべきです。

## 3. 新しい発見を追加する際の具体的な手順

一貫性を保つため、以下の手順に正確に従ってください。

1.  **命名:** 脆弱性に明確でインパクトのある名前を付けます（例：「認知的停滞」）。
2.  **概要の更新:** 「3. Summary of Findings」セクションに、新しい発見を簡潔に説明する箇条書きを追加します。
3.  **新規セクションの作成:** 最後の「Detailed Finding」セクションの直後に、新しいセクションを作成します。以下のテンプレートを正確にコピーし、新しい発見の詳細を記入してください。

    ```markdown
    ## X. Detailed Finding N: [発見の名称]

    **Overview:** [脆弱性を明確かつ簡潔に説明。中心的な問題は何か？どのように誘発されるか？]

    `[図を挿入: 発見を視覚的に説明する図、チャート、グラフのプレースホルダー]`

    -   **Severity (X/10):** [スコアを正当化。潜在的な現実世界の危害は何か？具体的に記述（例：金銭的損失、データ破壊、システム停止）。]
    -   **Breadth (X/10):** [スコアを正当化。どれだけのユーザーやシステムに影響しうるか？一般的な問題か、特定のドメインに限定されるか？]
    -   **Novelty (X/10):** [スコアを正当化。単純なジェイルブレイクのような既知の脆弱性とどう違うか？新しい問題クラスや攻撃ベクトルを明らかにしているか？]
    ```
4.  **セクション番号の更新:** 新しいセクションを含め、後続のすべてのセクション（再現性、結論）の番号を振り直し、連番になるようにします。
5.  **レビュー:** 文書全体を読み返し、トーンの一貫性、論理的な流れ、説得力のある物語になっているかを確認します。