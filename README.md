# 概要

ソートアルゴリズムの可視化・比較・保存・統計取得ができる Web アプリケーションです。  
フロントエンドでソートの動きを視覚的に確認できるだけでなく、C++ ソートエンジンによるベンチマーク実行、Flask API による結果保存、MySQL / Amazon RDS によるデータ管理まで含めて構築しています。  

現在は AWS 上にデプロイしており、Route 53・ALB・ACM を用いた HTTPS 公開に対応しています。

---

6種類のソートアルゴリズムを対象に、以下の機能を提供しています。

- ソートアルゴリズムの可視化
- C++ エンジンによるベンチマーク実行
- 実行結果の保存
- 過去のバトル履歴取得
- 統計データ取得
- Swagger UI による API 確認

### 対応アルゴリズム

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort

このプロジェクトは、単なるアルゴリズム可視化に留まらず、**フロントエンド・バックエンド API・DB 設計・Docker・OpenAPI・AWS インフラ**まで一貫して設計・実装したポートフォリオです。

---

## 主な機能

- ソートアルゴリズムの可視化
- C++ エンジンによるベンチマーク実行
- バトル結果の保存
- 保存済みバトル履歴の取得
- アルゴリズム別統計の集計
- OpenAPI による API ドキュメント表示
- AWS 本番環境での HTTPS 公開
- `/health` によるヘルスチェック対応

---

## 使用技術

### フロントエンド
- HTML
- CSS
- JavaScript

### バックエンド
- Python
- Flask
- Gunicorn
- Nginx

### ソートエンジン
- C++

### データベース
- MySQL 8
- Amazon RDS for MySQL

### API / ドキュメント
- REST API
- OpenAPI 3.0.2
- Flasgger
- Swagger UI

### インフラ
- Docker
- Docker Compose
- AWS EC2
- AWS ALB
- AWS ACM
- AWS Route 53
- AWS VPC

### テスト / 品質管理
- pytest
- pytest-cov
- coverage
- Flask test client
- GitHub Actions

### 開発ツール
- Git
- GitHub
- VS Code
- DBeaver

---

## システム構成

本番環境では以下の構成で動作しています。

```text
Route 53
  ↓
Application Load Balancer (HTTPS / ACM)
  ↓
Nginx (EC2)
  ↓
Gunicorn
  ↓
Flask Application
  ↓
Amazon RDS for MySQL
```

## 工夫した点

- C++ ベンチマークエンジンと Flask API を連携し、処理責務を分離した
- ALB + ACM + Route 53 により HTTPS 公開を実現した
- EC2 を直接公開せず、ALB 経由のみアクセス可能な構成にした
- `/health` を用意し、ALB のヘルスチェックに対応した
- API を OpenAPI で管理し、Swagger UI から確認できるようにした

---

## API 一覧

| Method | Endpoint | 内容 |
|---|---|---|
| POST | `/api/run-battle` | ソートベンチマーク実行 |
| POST | `/api/battles` | バトル結果保存 |
| GET | `/api/battles` | バトル履歴取得 |
| GET | `/api/statistics` | 統計取得 |
| GET | `/health` | ヘルスチェック |

---

## DB 設計概要

### 主なテーブル

- `users`
- `algorithms`
- `battles`
- `battle_results`

### 設計ポイント

- 外部キー制約による整合性維持
- 重複防止を意識した設計
- 集計しやすいテーブル分割
- バトル保存時のトランザクション管理
- アルゴリズムマスタの分離

---

## 今後の改善点

- JWT 認証導入
- ユーザー機能追加
- CI/CD 導入
- 監視強化
- フロントエンド改善
- 統計画面の可視化強化
- コード整理・テスト拡充