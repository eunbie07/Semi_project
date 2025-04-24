const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();


app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/homepage.html'));
});


app.get('/api/depression', async (req, res) => {
  const { age, gender, year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.23:3001/depression', {
      params: { age, gender, year }
    });
    res.send(response.data); 
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});

app.get('/api/smartphone_badeffect', async (req, res) => {
  const { age, gender, year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.53:3001/smartphone_badeffect', {
      params: { age, gender, year }
    });
    res.send(response.data); 
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});

app.get('/api/stress_top_issue', async (req, res) => {
  const { year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.23:3001/stress_top_issue', {
      params: { year }
    });
    res.send(response.data); 
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});


app.get('/api/stress_region', async (req, res) => {
  const { region, year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.23:3001/stress_region', {
      params: { region, year }
    });
    res.send(response.data); 
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});

app.get('/api/breakfast_region', async (req, res) => {
  const { region, year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.23:3001/breakfast_region', {
      params: { region, year }
    });
    res.send(response.data); 
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});


app.get('/api/stress_issues', async (req, res) => {
  const { year } = req.query;

  try {
    const response = await axios.get('http://192.168.1.23:3001/stress_issues', {
      params: { year }
    });
    res.send(response.data); 
  } catch (error) {
    console.error('백엔드 호출 오류:', error.message);
    res.status(500).send({ result: false, message: '백엔드 오류 발생' });
  }
});


app.listen(80, '0.0.0.0', function() {
  console.log("80 port : Server Started~!!");
})