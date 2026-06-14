import os
from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 1. Supabase 정보 입력 (본인의 정보로 변경)
SUPABASE_URL = "https://vfsuctmqwweqlvfhzahh.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_I2j4R_uDL_7YgsIXf-g-vw_c7oRC0mS"

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
        
        if not client_text:
            return jsonify({"status": "error", "message": "No data"}), 400
            
        # Supabase DB에 저장
        supabase.table("web_logs").insert({"content": client_text}).execute()
        return jsonify({"status": "success"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 🌟 Render는 PORT 환경 변수를 요구하므로 os.environ을 사용합니다.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
