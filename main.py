import os
from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 1. Supabase 정보 입력 (오류 교정 완료)
# 🌟 끝에 /rest/v1/ 을 완전히 제거했습니다.
SUPABASE_URL = "https://vfsuctmqwweqlvfhzahh.supabase.co"

# 🌟 중요: 반드시 'eyJhb...'로 시작하는 아주 긴 Anon Public Key 전체를 입력하세요.
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZmc3VjdG1xd3dlcWx2Zmh6YWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE0MTM4OTMsImV4cCI6MjA5Njk4OTg5M30.DIEjb37bJ0Bs73dtWgDajVsWSX89Q2PQ3uk89keaQhA"

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
        # 혹시 오류가 나면 어떤 오류인지 JSON 결과로 친절히 알려줍니다.
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
