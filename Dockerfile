# seleniume2e/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 컨테이너가 켜지면 테스트 실행 (옵션)
# CMD ["pytest", "-v"]