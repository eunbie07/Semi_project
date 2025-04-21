const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();

// 1. 정적 파일 서빙 (프론트 HTML, JS, CSS 등)
app.use(express.static(path.resolve(__dirname, '../public')));

// 2. 백엔드 프록시 API (FastAPI 호출)
app.get('/api/depression', async (req, res) => {
  const { age, gender, year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.23:3001/depression', {
      params: { age, gender, year }
    });
    res.send(response.data); // 프론트엔드에 그대로 전달
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});

// 3. 서버 실행
app.listen(8000, function() {
  console.log("8000 port : Server Started~!!");
})
