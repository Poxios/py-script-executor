import os
import subprocess
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# .env 파일의 환경 변수를 로드합니다.
load_dotenv()

app = Flask(__name__)

@app.route('/make-pull', methods=['POST'])
def make_pull():
    data = request.get_json()
    env_password = os.getenv('PASSWORD')
    if data and 'password' in data and data['password'] == env_password:
        try:
            result = subprocess.run(['./commands.sh'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return jsonify({'status': 'success', 'output': result.stdout.decode('utf-8')})
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'error', 'output': e.stderr.decode('utf-8')}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid password'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
