# ランダム病気（randomdisease）

ボタンを押すと、病気をランダムで1件表示する小さなツールです。既存の random 系列（randomwikipedia / randompixiv / randomsiteblog）の病気版です。

## 使い方

- **🎲 ランダムで病気を表示**：収録した全60件の病気からランダムに1件を選び、病名と一緒に基本的な情報（分類・概要・主な症状・原因・一般的なポイント）を表示します。
- **Wikipediaで詳しく見る**：その病気の Wikipedia ページを新しいタブで開きます。
- もう一度ボタンを押すと、別の病気が表示されます。

病気の情報は、一般的な知識をこのツール用に書き起こした内蔵データから表示します（外部サイトの本文の転載はしていません）。外部通信をしなくても動作します。

> ⚠️ このツールは一般的な情報提供・学習のためのものです。診断や治療の代わりにはなりません。気になる症状がある場合は、自己判断せず医療機関に相談してください。

## ローカル実行

```bash
pip install -r requirements.txt
python app.py
# http://localhost:5000
```

## テスト

```bash
python -m pytest tests/
# または
python -m unittest discover -s tests
```

※ テストでは外部通信を行わず、内蔵データと画面表示を検証します。

## Render へのデプロイ

`render.yaml` 同梱。無料プラン（free）の Web Service としてデプロイできます（healthCheckPath: `/healthz`）。

## ライセンス

MIT License
