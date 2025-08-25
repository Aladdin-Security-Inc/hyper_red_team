# LLMレッドチーム実験フレームワーク

このプロジェクトは、大規模言語モデル（LLM）に対するレッドチーム実験を実施するための、構造化されたフレームワークを提供します。拡張性を考慮して設計されており、さまざまな実験、データセット、設定を容易に管理できます。

## 概要

主な目的は、LLMに存在する以下のような潜在的な脆弱性をテストし、特定することです。
- **不適切なツール使用 (Inappropriate Tool Use):** 有害または意図しない目的でツールを使用するように、モデルを誘導できるかを評価します。
- **認知的停滞と妨害行為 (Cognitive Stagnation & Sabotage):** テスト駆動開発（TDD）の文脈で、モデルが意図的に非効率なコードやバグを埋め込むといった、欺瞞的な振る舞いを示すかを評価します。

このフレームワークは柔軟に構築されており、研究者は新しい実験やデータセットを簡単に追加できます。

## ディレクトリ構造

プロジェクトは以下のディレクトリで構成されています。

```
.
├── data/
│   └── <dataset_name>/         # 生データおよび処理済みデータ（COCO形式JSON）
├── experiments/
│   └── <experiment_name>/      # 特定の実験コードと設定ファイル
│       ├── config.yaml         # 実験固有の設定
│       └── run.py              # 実験実行用のメインスクリプト
├── src/
│   ├── data_loaders.py         # データ読み込み・変換用ユーティリティ
│   ├── llm_client.py           # LLM API（例: Groq）連携用クライアント
│   └── wandb_logger.py         # Weights & Biasesへのロギング用ラッパー
├── scripts/
│   └── convert_datasets.py     # 生データを標準フォーマットへ変換するスクリプト
├── .env                        # APIキーなどの秘密情報を格納（git管理外）
├── requirements.txt            # Pythonパッケージの依存関係リスト
└── README.md                   # このファイル
```

## セットアップとインストール

以下の手順でプロジェクト環境をセットアップします。高速なパッケージ管理ツール `uv` を使用します。

1.  **リポジトリをクローンします（まだの場合）:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **仮想環境を作成します:**
    ```bash
    uv venv
    ```

3.  **仮想環境を有効化（アクティベート）します:**
    ```bash
    source .venv/bin/activate
    ```

4.  **必要なパッケージをインストールします:**
    ```bash
    uv pip install -r requirements.txt
    ```

5.  **APIキーを設定します:**
    環境ファイルのサンプルをコピーし、ご自身の秘密鍵を設定します。
    ```bash
    cp .env.example .env
    ```
    その後、`.env` ファイルを編集し、`GROQ_API_KEY` と `WANDB_API_KEY` を追記してください。

## データセット管理

異なる実験で様々なデータソースを標準化された方法で利用できるよう、このフレームワークではCOCOライクなJSON形式を全データセットの標準として採用しています。

### 標準データフォーマット

処理済みの各データセットは、COCOフォーマットと同様に `images`, `annotations`, `categories` というキーを持つJSONファイルです。これにより、データローダーは異なるデータ型（テキストプロンプト、コード問題など）を一貫して扱うことができます。

### 新しいデータセットの追加手順

1.  **生データを追加:** 新しい生データ（例: CSV, Pythonファイル）を `data/` 内の新しいサブディレクトリに配置します。例: `data/my_new_dataset/`

2.  **変換関数を作成:** `src/data_loaders.py` を開き、生データを読み込んで標準のCOCOライクな辞書形式で出力する新しい関数（例: `convert_my_dataset_to_coco_like`）を追加します。

3.  **変換スクリプトを更新:** `scripts/convert_datasets.py` を開き、新しく作成した変換関数の呼び出し処理を追加します。

4.  **変換スクリプトを実行:**
    以下のコマンドを実行し、最終的なJSONデータセットを生成します。
    ```bash
    python scripts/convert_datasets.py
    ```

## 実験の実行方法

### 既存の実験

-   **`hunnypod`**: 「不適切なツール使用」をテストします。場所: `experiments/hunnypod/`
-   **`tdd_sabotage_experiment`**: 「認知的停滞と妨害行為」をテストします。場所: `experiments/tdd_sabotage_experiment/` (注意: こちらの `run.py` はまだ完全には実装されていません)

### 実験の実行手順

すべての実験は、それぞれのディレクトリ内から実行します。

1.  **実験ディレクトリに移動します:**
    ```bash
    cd experiments/hunnypod
    ```

2.  **仮想環境を有効化します（まだの場合）:**
    ```bash
    source ../../.venv/bin/activate
    ```

3.  **実験を実行します:**
    ```bash
    python run.py
    ```
    スクリプトは自動的に `config.yaml` を読み込み、データを取得し、実験を実行して、結果をWeights & Biasesに記録します。

### 新しい実験の作成手順

1.  **新しいディレクトリを作成:**
    `mkdir experiments/my_new_experiment`

2.  **`config.yaml` を作成:**
    新しいディレクトリ内に `config.yaml` を作成します。`data.path`, `model` パラメータ, `logging` 設定などを記述します。独自のカスタム設定を追加することも可能です。

3.  **`run.py` を作成:**
    `run.py` スクリプトを作成します。`experiments/hunnypod/run.py` をテンプレートとして利用できます。新しい実験計画に合わせてロジックを修正してください。

この構造化されたアプローチにより、すべての実験の再現性と管理の容易性が保証されます。