# Google Maps レビュー スクレイパー
[Original English Version](README.md)

## 概要

このPythonスクリプトは、Playwrightライブラリを使用して、指定された場所のGoogle Mapsレビューをスクレイピングするプロセスを自動化します。各場所のページに移動し、レビューア名、コメント数、星評価、レビュー日時、レビューテキスト、レビューURLなどのレビュー情報を抽出し、データをCSVファイルに保存します。

## 特徴

-   **自動スクレイピング:** Playwrightを使用して、Google Mapsの場所への移動、ボタンのクリック、レビューをロードするためのスクロールなどのブラウザ操作を自動化します。
-   **データ抽出:** レビューア名、コメント数、星評価、レビュー日時、レビューテキスト、レビューURLなどの主要なレビュー情報を抽出します。
-   **CSVエクスポート:** 抽出されたデータをCSVファイル（`google_maps_reviews.csv`）に保存し、簡単な分析と保存を可能にします。
-   **エラー処理:** Google Mapsインターフェースの問題を処理するために、レビューURLを抽出するための再試行ロジックを実装します。

## 必要条件

-   Python 3.6+
-   Playwrightライブラリ
-   Pandasライブラリ
-   `requirements.txt`で指定されたその他の依存関係

## インストール

1.  このリポジトリをクローンします。

    ```bash
    git clone https://github.com/masykur8d/google_maps_reviews_scraper.git
    cd google_maps_reviews_scraper
    ```

2.  依存関係をインストールします。

    ```bash
    pip install -r requirements.txt
    ```

## 使い方

1.  **入力データの変更:**
    -   `main.py`ファイルを編集して、目的のGoogle Mapsの場所と共有URLで`input_data`リストを更新します。

    ```python
    input_data = [
        {
            'location_name': 'マティーニバーガー',
            'share_url': 'https://maps.app.goo.gl/3L9NpDhg1y7VPEBw8'
        },
        {
            'location_name': 'ランタンバｰガｰ＆ステーキ Lantern burger＆steak',
            'share_url': 'https://maps.app.goo.gl/VLPT47gZSaVbcrN69'
        }
    ]
    ```

2.  **スクリプトの実行:**

    ```bash
    python main.py
    ```

3.  **結果の表示:**
    -   スクレイピングされたデータは、スクリプトと同じディレクトリにある`google_maps_reviews.csv`という名前のCSVファイルに保存されます。

## Docker

Dockerを使用してこのアプリケーションを実行するには、次の手順に従います。

1.  **Dockerイメージのビルド:**

    ```bash
    docker build -t google-maps-reviews .
    ```

2.  **Dockerコンテナの実行:**

    ```bash
    docker run google-maps-reviews
    ```

    このコマンドは、指定されたDockerfileを使用して、Dockerコンテナ内でスクリプトを実行します。結果の`google_maps_reviews.csv`ファイルは、コンテナのファイルシステム内に作成されます。このファイルにアクセスするには、コンテナからホストマシンにコピーする必要がある場合があります。

## コードの説明

-   **ライブラリのインポート:** `re`、`playwright`、`time`、`pandas`などの必要なライブラリをインポートします。
-   **`run`関数:**
    -   Playwrightを使用してChromiumブラウザインスタンスを起動します。
    -   スクレイピングタスクごとに新しいブラウザコンテキストを作成します。
    -   場所のリストを反復処理し、各場所のページに移動して、レビュー情報を抽出します。
    -   抽出されたデータをCSVファイルに保存します。
-   **メイン実行ブロック:**
    -   `sync_playwright`を使用してPlaywrightを起動し、`run`関数を実行します。

## ベストプラクティス

-   **`robots.txt`の尊重:** Google Maps Webサイトの`robots.txt`ファイルを確認して、スクレイピングが許可されていることを確認してください。
-   **遅延の追加:** `time.sleep()`を使用してリクエスト間に遅延を追加し、サーバーの過負荷を回避し、IPが禁止されないようにします。
-   **エラー処理:** 例外をキャッチし、スクリプトがクラッシュするのを防ぐための堅牢なエラー処理を実装します。
-   **ユーザーエージェント:** カスタムユーザーエージェントを設定してスクリプトを識別し、ブロックされないようにします。
-   **レート制限:** レート制限を実装して、単位時間あたりのリクエスト数を制御します。
-   **ヘッドレスモード:** リソース消費を削減するために、ブラウザをヘッドレスモードで実行します。
-   **データ検証:** 抽出されたデータを検証して、その正確性と完全性を確認します。

## 免責事項

このスクリプトは、教育および研究目的のみを目的としています。Google Mapsのレビューをスクレイピングすると、Google Maps Webサイトの利用規約に違反する可能性があります。ご自身の責任においてこのスクリプトを使用してください。
