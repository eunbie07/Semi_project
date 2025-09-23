# 배포 가이드

청소년 스마트폰 과의존 분석 대시보드 배포 및 운영 가이드

## 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [환경 설정](#환경-설정)
3. [로컬 개발 환경](#로컬-개발-환경)
4. [프로덕션 배포](#프로덕션-배포)
5. [환경변수 설정](#환경변수-설정)
6. [트러블슈팅](#트러블슈팅)
7. [모니터링](#모니터링)

---

## 시스템 요구사항

### 최소 요구사항
- **OS**: Ubuntu 18.04+ / CentOS 7+ / Windows 10+
- **Memory**: 최소 2GB RAM (권장 4GB+)
- **Storage**: 최소 5GB 여유 공간
- **Network**: 외부 API 접근을 위한 인터넷 연결

### 소프트웨어 요구사항
- **Python**: 3.7 이상
- **Node.js**: 14.0 이상
- **npm**: 6.0 이상

---

## 환경 설정

### 1. Python 환경 설정

```bash
# Python 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 필요한 패키지 설치
pip install fastapi uvicorn pandas matplotlib seaborn
```

### 2. Node.js 환경 설정

```bash
# Node.js 버전 확인
node --version
npm --version

# 프로젝트 디렉토리로 이동
cd web/node-server

# 의존성 설치
npm install
```

---

## 로컬 개발 환경

### 1. FastAPI 백엔드 실행

```bash
# FastAPI 디렉토리로 이동
cd web/fastapi

# 개발 서버 실행 (자동 리로드)
uvicorn main:app --reload --host 0.0.0.0 --port 3001

# 또는 Python으로 직접 실행
python main.py
```

### 2. Express.js 프론트엔드 서버 실행

```bash
# Node 서버 디렉토리로 이동
cd web/node-server

# 개발 서버 실행
npm start

# 또는 직접 실행
node server.js
```

### 3. 접속 확인

- **프론트엔드**: http://localhost:80
- **백엔드 API**: http://localhost:3001
- **API 문서**: http://localhost:3001/docs

---

## 프로덕션 배포

### 1. Docker를 이용한 배포

#### Dockerfile 생성 (FastAPI)

```dockerfile
# web/fastapi/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
```

#### Dockerfile 생성 (Express.js)

```dockerfile
# web/node-server/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 80

CMD ["node", "server.js"]
```

#### Docker Compose 설정

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./web/fastapi
    ports:
      - "3001:3001"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./web/fastapi/json:/app/json
    restart: unless-stopped

  frontend:
    build: ./web/node-server
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:3001
    restart: unless-stopped
```

### 2. 배포 명령어

```bash
# Docker Compose 빌드 및 실행
docker-compose up -d --build

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

### 3. Nginx 리버스 프록시 설정

```nginx
# /etc/nginx/sites-available/youth-dashboard
server {
    listen 80;
    server_name your-domain.com;

    # 프론트엔드
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 백엔드 API
    location /api/ {
        proxy_pass http://localhost:3001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 정적 파일 캐싱
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 환경변수 설정

### 1. 필수 환경변수

#### .env 파일 생성 (FastAPI)

```bash
# web/fastapi/.env
DEBUG=False
HOST=0.0.0.0
PORT=3001
CORS_ORIGINS=["http://localhost:80", "https://your-domain.com"]
```

#### .env 파일 생성 (Express.js)

```bash
# web/node-server/.env
NODE_ENV=production
PORT=80
BACKEND_HOST=localhost
BACKEND_PORT=3001
```

### 2. API 키 설정

#### Kakao Map API 키

```bash
# web/public/homepage.html 수정 필요
# 11번째 줄의 YOUR_KEY를 실제 키로 교체
<script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=YOUR_ACTUAL_KEY&autoload=false&libraries=services"></script>
```

#### 기상청 API 키

```bash
# web/public/weather.js 수정 필요
# 3번째 줄의 serviceKey를 실제 키로 교체
const serviceKey = "YOUR_ACTUAL_SERVICE_KEY";
```

### 3. IP 주소 설정

#### server.js IP 주소 수정

```javascript
// web/node-server/server.js
// 하드코딩된 IP 주소를 환경변수로 변경
const BACKEND_HOST = process.env.BACKEND_HOST || 'localhost';
const BACKEND_PORT = process.env.BACKEND_PORT || '3001';

// 기존 하드코딩된 부분 수정
// 18, 32, 46, 61, 75, 90번째 줄
const response = await axios.get(`http://${BACKEND_HOST}:${BACKEND_PORT}/depression`, {
  params: { age, gender, year }
});
```

---

## 트러블슈팅

### 일반적인 문제들

#### 1. 포트 충돌 문제

```bash
# 포트 사용 중인 프로세스 확인
sudo lsof -i :80
sudo lsof -i :3001

# 프로세스 종료
sudo kill -9 <PID>
```

#### 2. CORS 오류

```python
# web/fastapi/main.py에서 CORS 설정 확인
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:80", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. API 연결 실패

```bash
# FastAPI 서버 상태 확인
curl http://localhost:3001/

# Express 서버에서 백엔드 연결 테스트
curl http://localhost:80/api/depression?age=16&gender=male&year=2023
```

#### 4. 데이터 파일 누락

```bash
# JSON 데이터 파일 확인
ls -la web/fastapi/json/

# 필요한 파일들
- depression.json
- breakfast_skip.json
- private_edu.json
- stress_issues.json
- stress_region.json
- breakfast_region.json
```

### 로그 확인 방법

#### FastAPI 로그

```bash
# 개발 모드에서 콘솔 출력 확인
# 프로덕션에서는 로그 파일로 저장 권장
uvicorn main:app --log-level info --access-log
```

#### Express.js 로그

```bash
# PM2를 사용한 프로세스 관리 (권장)
npm install -g pm2
pm2 start server.js --name youth-dashboard
pm2 logs youth-dashboard
```

---

## 모니터링

### 1. 서버 상태 모니터링

#### 헬스 체크 엔드포인트 추가

```python
# web/fastapi/main.py에 추가
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }
```

#### 모니터링 스크립트

```bash
#!/bin/bash
# monitor.sh

# API 서버 상태 확인
curl -f http://localhost:3001/health || echo "API 서버 다운"

# 웹 서버 상태 확인
curl -f http://localhost:80 || echo "웹 서버 다운"

# 디스크 사용량 확인
df -h

# 메모리 사용량 확인
free -h
```

### 2. 성능 모니터링

#### 응답 시간 측정

```bash
# API 응답 시간 측정
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3001/depression?age=16&gender=male&year=2023
```

#### 리소스 사용량 모니터링

```bash
# top, htop으로 실시간 모니터링
htop

# Docker 컨테이너 리소스 사용량
docker stats
```

---

## 백업 및 복구

### 1. 데이터 백업

```bash
# JSON 데이터 파일 백업
tar -czf backup-$(date +%Y%m%d).tar.gz web/fastapi/json/

# 전체 프로젝트 백업
tar -czf full-backup-$(date +%Y%m%d).tar.gz --exclude=node_modules --exclude=venv .
```

### 2. 자동 백업 스크립트

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/youth-dashboard"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 데이터 백업
tar -czf $BACKUP_DIR/data_$DATE.tar.gz web/fastapi/json/

# 설정 파일 백업
cp web/node-server/.env $BACKUP_DIR/node_env_$DATE
cp web/fastapi/.env $BACKUP_DIR/fastapi_env_$DATE

# 7일 이상된 백업 파일 삭제
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "백업 완료: $DATE"
```

---

## 보안 고려사항

### 1. API 키 보안

- 환경변수를 통한 API 키 관리
- .env 파일을 .gitignore에 추가
- 프로덕션에서는 시크릿 관리 시스템 사용

### 2. 네트워크 보안

- HTTPS 사용 (Let's Encrypt 권장)
- 방화벽 설정으로 필요한 포트만 개방
- API 요청 제한 (Rate Limiting)

### 3. 데이터 보안

- 민감한 데이터 암호화
- 정기적인 보안 업데이트
- 접근 로그 모니터링

---

## 운영 체크리스트

### 배포 전 확인사항

- [ ] 모든 환경변수 설정 완료
- [ ] API 키 교체 완료
- [ ] IP 주소 하드코딩 제거
- [ ] CORS 설정 확인
- [ ] 데이터 파일 존재 확인
- [ ] 헬스 체크 엔드포인트 동작 확인

### 배포 후 확인사항

- [ ] 모든 페이지 정상 로드
- [ ] API 응답 정상
- [ ] 지도 기능 동작
- [ ] 차트 렌더링 확인
- [ ] 모바일 반응형 확인
- [ ] 외부 API 연동 확인

이 가이드를 따라 배포하면 안정적이고 확장 가능한 프로덕션 환경을 구축할 수 있습니다.