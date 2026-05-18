-- データベース全体のデフォルト文字セットと照合順序を設定
ALTER DATABASE main CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- users テーブルの作成
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- 主キー、自動増分ID
    email VARCHAR(255) UNIQUE NOT NULL,       -- メールアドレス（ユニーク、必須）
    hashed_password VARCHAR(255) NOT NULL,    -- ハッシュ化されたパスワード（必須）
    is_active BOOLEAN DEFAULT TRUE,           -- アカウントが有効かどうか（デフォルトTRUE）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 作成日時（自動挿入）
);

-- items テーブルの作成
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- 主キー、自動増分ID
    title VARCHAR(100) NOT NULL,              -- 商品名（必須、最大100文字）
    description VARCHAR(500),                 -- 商品説明（最大500文字）
    price INT NOT NULL,                       -- 価格（必須）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 作成日時（自動挿入）
);

-- 初期ユーザーデータの投入
-- パスワード 'password123' が bcrypt でハッシュ化されています
INSERT INTO users (email, hashed_password) VALUES
('test@example.com', '$2b$12$824JqBdB6ToEapbNE.wFeefA.SKIBCvbH0w3nlqVqSZ36ajaaNTwm');

-- 初期商品データの投入
INSERT INTO items (title, description, price) VALUES
('はじめての商品', 'これはテストデータです', 1000),
('便利なツール', 'エンジニア必携のアイテム', 2500),
('FastAPI本', '最速で学ぶAPI開発', 3800);