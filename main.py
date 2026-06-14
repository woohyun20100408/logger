import os
import traceback
from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 1. Supabase 정보 입력
SUPABASE_URL = "https://vfsuctmqwweqlvfhzahh.supabase.co"

# 🌟 중요: RLS 에러(500)를 해결하기 위해 'service_role' 키를 사용합니다.
# Supabase 대시보드 -> Settings -> API -> Project API keys 에서 service_role (secret) 키를 복사해서 아래에 넣으세요.
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZmc3VjdG1xd3dlcWx2Zmh6YWhoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MTQxMzg5MywiZXhwIjoyMDk2OTg5ODkzfQ.jv_aMwmwJQfoZrmUK0i-fi87RsBzjf0CJZFCSG-Ry6I"

# 2. Supabase 클라이언트 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/log', methods=['POST'])
def receive_log():
    try:
        data = request.json
        client_text = data.get('text', '')

        # 데이터가 비어있으면 400 에러 반환
        if not client_text:
            return jsonify({"status": "error", "message": "No data"}), 400

        # 데이터베이스에 삽입
        result = (
            supabase
            .table("web_logs")
            .insert({"content": client_text})
            .execute()
        )

        print("INSERT RESULT:", result)

        return jsonify({"status": "success"})

    except Exception as e:
        print("ERROR:", repr(e))
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
