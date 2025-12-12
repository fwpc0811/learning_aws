import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS  # 追加

app = Flask(__name__)
CORS(app)  # 追加: すべてのオリジンからのアクセスを許可

# 環境変数からDB接続情報を取得
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

@app.route('/')
def hello():
    """ヘルスチェック用"""
    return jsonify({
        "status": "ok",
        "message": "Hello from Flask on ECS!"
    })

@app.route('/db-check')
def db_check():
    """RDS接続確認用"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # RDSから現在時刻を取得するクエリを実行
        cur.execute('SELECT NOW();')
        db_time = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "db_time": db_time,
            "message": "Connected to RDS successfully!"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # ECS/Dockerで外部からアクセスできるように 0.0.0.0 で起動
    app.run(host='0.0.0.0', port=80)