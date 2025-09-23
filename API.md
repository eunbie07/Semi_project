# API 문서

청소년 스마트폰 과의존 분석 대시보드 API 상세 문서

## 기본 정보

- Base URL: `http://localhost:3001`
- Content-Type: `application/json`
- CORS: 모든 도메인 허용

## API 엔드포인트

### 1. 청소년 우울감 데이터

#### GET /depression

청소년의 연령별, 성별, 연도별 우울감 경험률 데이터를 조회합니다.

**Parameters:**
- `age` (integer, required): 연령 (13-18)
- `gender` (string, required): 성별 ("male", "female", "전체")
- `year` (integer, required): 조회 연도 (2020-2024)

**Request Example:**
```
GET /depression?age=16&gender=male&year=2023
```

**Response Example:**
```json
{
  "result": true,
  "depression_rate": 28.5
}
```

**Error Response:**
```json
{
  "result": false,
  "depression_rate": null
}
```

### 2. 아침결식률 데이터

#### GET /breakfast_skip_rate

청소년의 아침결식률 데이터를 조회합니다.

**Parameters:**
- `age` (integer, required): 연령 (13-18)
- `gender` (string, required): 성별 ("male", "female", "전체")
- `year` (integer, required): 조회 연도 (2020-2024)

**Request Example:**
```
GET /breakfast_skip_rate?age=17&gender=female&year=2024
```

**Response Example:**
```json
{
  "result": true,
  "breakfast_skip_rate": 15.2
}
```

### 3. 사교육 참여율

#### GET /private_edu

연령대별 사교육 참여율 데이터를 조회합니다.

**Parameters:**
- `age` (integer, required): 연령 (8-19)
- `year` (integer, required): 조회 연도 (2020-2024)

**Age-School Level Mapping:**
- 8-13세: 초등학교
- 14-16세: 중학교
- 17-19세: 고등학교

**Request Example:**
```
GET /private_edu?age=15&year=2023
```

**Response Example:**
```json
{
  "result": true,
  "school_level": "중학교",
  "private_edu_rate": 67.8
}
```

### 4. 스트레스 최고 관심사

#### GET /stress_top_issue

해당 연도의 청소년 최고 스트레스 요인을 조회합니다.

**Parameters:**
- `year` (integer, required): 조회 연도 (2020-2024)

**Request Example:**
```
GET /stress_top_issue?year=2024
```

**Response Example:**
```json
{
  "result": true,
  "top_issue": "학업문제",
  "concern_rate(%)": 45.3
}
```

### 5. 지역별 스트레스율

#### GET /stress_region

지역별 청소년 스트레스율 데이터를 조회합니다.

**Parameters:**
- `region` (string, required): 지역명 (서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주)
- `year` (integer, required): 조회 연도 (2020-2024)

**Request Example:**
```
GET /stress_region?region=서울&year=2023
```

**Response Example:**
```json
{
  "result": true,
  "region": "서울",
  "year": 2023,
  "stress_rate": 32.1
}
```

### 6. 스트레스 이슈 목록

#### GET /stress_issues

특정 연도의 모든 스트레스 요인과 관심율을 조회합니다.

**Parameters:**
- `year` (float, required): 조회 연도 (2020.0-2024.0)

**Request Example:**
```
GET /stress_issues?year=2023.0
```

**Response Example:**
```json
[
  {
    "issue": "학업문제",
    "concern_rate": 45.3
  },
  {
    "issue": "외모",
    "concern_rate": 23.7
  },
  {
    "issue": "건강",
    "concern_rate": 18.2
  }
]
```

### 7. 지역별 아침결식률

#### GET /breakfast_region

지역별 아침결식률 데이터를 조회합니다.

**Parameters:**
- `region` (string, required): 지역명
- `year` (integer, required): 조회 연도 (2020-2024)

**Request Example:**
```
GET /breakfast_region?region=경기&year=2024
```

**Response Example:**
```json
{
  "result": true,
  "region": "경기",
  "year": 2024,
  "breakfast_rate": 14.8
}
```

## 에러 코드

### HTTP 상태 코드
- `200 OK`: 요청 성공
- `500 Internal Server Error`: 백엔드 서버 오류

### 응답 에러 메시지
- `result: false`: 해당 조건에 맞는 데이터가 없음
- `message: "백엔드 오류 발생"`: 서버 연결 실패

## 데이터 스키마

### Depression Data
```json
{
  "age": "integer",
  "gender": "string",
  "year": "integer",
  "depression_rate": "float"
}
```

### Breakfast Skip Data
```json
{
  "age": "string",
  "gender": "string",
  "year": "string",
  "breakfast_skip_rate": "string"
}
```

### Private Education Data
```json
{
  "year": "string",
  "school_level": "string",
  "private_edu_rate": "float"
}
```

### Stress Data
```json
{
  "year": "float",
  "issue": "string",
  "concern_rate(%)": "float"
}
```

### Regional Data
```json
{
  "region": "string",
  "year": "integer",
  "stress_rate": "float",
  "breakfast_rate": "float"
}
```

## 사용 예시

### JavaScript Fetch 예시
```javascript
// 2023년 16세 남학생 우울감률 조회
fetch('/api/depression?age=16&gender=male&year=2023')
  .then(response => response.json())
  .then(data => {
    if (data.result) {
      console.log(`우울감률: ${data.depression_rate}%`);
    } else {
      console.log('데이터를 찾을 수 없습니다.');
    }
  })
  .catch(error => {
    console.error('API 호출 오류:', error);
  });
```

### Python Requests 예시
```python
import requests

url = "http://localhost:3001/stress_region"
params = {
    "region": "서울",
    "year": 2023
}

response = requests.get(url, params=params)
data = response.json()

if data["result"]:
    print(f"서울 지역 스트레스율: {data['stress_rate']}%")
else:
    print("데이터를 찾을 수 없습니다.")
```

## 주의사항

1. **데이터 타입**: 일부 API에서 숫자 데이터가 문자열로 저장되어 있어 타입 변환이 필요할 수 있습니다.
2. **지역명**: 정확한 지역명을 사용해야 합니다. 공백이나 오타가 있으면 데이터를 찾을 수 없습니다.
3. **연도 범위**: 2020-2024년 데이터만 제공됩니다.
4. **서버 연결**: FastAPI 서버(3001포트)가 실행 중이어야 합니다.