import http from 'k6/http';
import { check, sleep } from 'k6';

const VUS = Number(__ENV.VUS || 500);

export const options = {
  stages: [
    { duration: '20s', target: VUS },
    { duration: '40s', target: VUS },
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<50'],
  },
};

const TEXTS = [
  'I love this amazing product',
  'This is the worst service ever',
  'The delivery arrived on tuesday',
  'you are a stupid idiot',
];

export default function () {
  const body = JSON.stringify({
    task: Math.random() < 0.5 ? 'sentiment' : 'toxicity',
    text: TEXTS[Math.floor(Math.random() * TEXTS.length)],
  });
  const res = http.post('http://127.0.0.1:8000/api/v1/predict', body, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, { 'status is 201': (r) => r.status === 201 });
  sleep(1 + Math.random() * 2);
}