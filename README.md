# 청소년 스마트폰 과의존 분석 대시보드

청소년의 스마트폰 과의존과 관련된 다양한 지표들을 분석하고 시각화하는 웹 기반 대시보드입니다.

## 프로젝트 개요

청소년의 우울감, 스트레스, 아침결식률, 사교육 참여율 등의 데이터를 통해 스마트폰 과의존 현상을 다각도로 분석하고, 대화형 웹 대시보드로 제공합니다.

## 주요 기능

- 다차원 데이터 분석: 연령별, 성별, 지역별, 연도별 청소년 지표 분석
- 대화형 시각화: Chart.js 기반 차트와 그래프
- 지역별 맵 시각화: Kakao Map API를 활용한 지역별 데이터 표시
- 퀴즈 시스템: 사용자 참여형 인터랙티브 퀴즈
- 실시간 데이터 조회: RESTful API를 통한 동적 데이터 제공

## 기술 스택

### Backend
- FastAPI: 고성능 Python 웹 프레임워크
- Express.js: Node.js 기반 프록시 서버

### Frontend
- Vanilla JavaScript: 클라이언트 사이드 로직
- Chart.js: 데이터 시각화
- Kakao Map API: 지도 기반 시각화

### Data Analysis
- Python: 데이터 처리 및 분석
- Pandas: 데이터 조작 및 분석
- Matplotlib: 그래프 생성

## 프로젝트 구조

```
Semi_project/
├── web/                          # 웹 애플리케이션
│   ├── fastapi/                  # FastAPI 백엔드
│   │   ├── main.py              # API 엔드포인트
│   │   └── json/                # 데이터 파일들
│   ├── node-server/             # Express.js 프록시 서버
│   │   ├── server.js
│   │   └── package.json
│   └── public/                  # 프론트엔드 정적 파일
│       ├── homepage.html        # 메인 페이지
│       ├── map.html            # 지역별 맵 페이지
│       └── assets/             # 정적 리소스
└── graph/                       # 데이터 분석 및 그래프 생성
    ├── depression_data.py       # 우울감 데이터 분석
    ├── breakfast_skip.py        # 아침결식률 분석
    └── *.json                   # 분석 결과 데이터
```

## 실행 방법

### 1. FastAPI 백엔드 실행
```bash
cd web/fastapi
python main.py
```

### 2. Express.js 프록시 서버 실행
```bash
cd web/node-server
npm install
npm start
```

### 3. 웹 브라우저에서 접속
```
http://localhost:80
```

## API 엔드포인트

### 청소년 우울감 데이터
- `GET /depression?age={age}&gender={gender}&year={year}`

### 아침결식률 데이터
- `GET /breakfast_skip_rate?age={age}&gender={gender}&year={year}`

### 사교육 참여율
- `GET /private_edu?age={age}&year={year}`

### 스트레스 관련 데이터
- `GET /stress_top_issue?year={year}`
- `GET /stress_region?region={region}&year={year}`
- `GET /stress_issues?year={year}`

### 지역별 데이터
- `GET /breakfast_region?region={region}&year={year}`

## 주요 컴포넌트

### 데이터 분석 모듈
- 우울감 분석: 연도별/성별 청소년 우울감 경험률 트렌드
- 아침결식률 분석: 지역별/연령별 아침결식 현황
- 스트레스 분석: 청소년 주요 스트레스 요인 파악

### 웹 대시보드
- 메인 대시보드: 종합적인 데이터 시각화
- 지역별 맵: 대한민국 지역별 청소년 지표 시각화
- 인터랙티브 퀴즈: 사용자 참여형 교육 컨텐츠

## 데이터 소스

- 청소년건강행태조사 데이터
- 교육통계 데이터
- 지역별 청소년 복지 관련 통계

## UI/UX 특징

- 반응형 디자인: 다양한 디바이스 지원
- 직관적 네비게이션: 사용자 친화적 인터페이스
- 시각적 피드백: 데이터 기반 인사이트 제공

## 필수 요구사항

### Python 환경
- Python 3.7+
- FastAPI
- Pandas
- Matplotlib

### Node.js 환경
- Node.js 14+
- Express.js
- Axios

### API 키 설정
Kakao Map API 사용을 위해 homepage.html 파일의 YOUR_KEY를 실제 API 키로 교체해야 합니다.

```javascript
// homepage.html 11번째 줄
<script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=YOUR_KEY&autoload=false&libraries=services"></script>
```

## 주의사항

- FastAPI 서버는 기본적으로 3001 포트에서 실행됩니다
- Express.js 서버는 80 포트에서 실행됩니다
- 서버 IP 주소가 하드코딩되어 있으므로 필요시 server.js 파일에서 수정이 필요합니다

## 프로젝트 정보

- 개발 기간: 2025년 4월 21~25일
- 팀 구성: 2명
- 개발 환경: Python, JavaScript, FastAPI, Express.js
- 주요 성과: 청소년 데이터 분석을 통한 인사이트 도출 및 웹 대시보드 구현