import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// --- Cấu hình test ---
export const options = {
  vus: 15,              // số user ảo
  duration: '60s',     // thời gian test
};

// --- Đọc dữ liệu từ file JSON (một lần khi khởi chạy) ---
const customers = new SharedArray('customers', function () {
  // File phải nằm cùng thư mục, ví dụ: lotdates.json
  return JSON.parse(open('./customers.json'));
});

export default function () {
  const url = 'http://fastapi.local:8100/customers/';

  // Clone mảng SharedArray để có thể thao tác
  const cloned = [...customers];

  // Chọn ngẫu nhiên customer để insert
  const customer = cloned[Math.floor(Math.random() * cloned.length)];
  const payload = JSON.stringify(customer);

  const params = {
    headers: {
      'accept': '*/*',
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  };

  // --- Gửi request ---
  const res = http.post(url, payload, params);
  console.log(`Status: ${res.status}`);
  console.log(`Body: ${res.body}`);

  // --- Kiểm tra phản hồi ---
  check(res, {
    'status is 200': (r) => r.status === 200,
	  'response time < 2s': (r) => r.timings.duration < 2000
  });

  // Log ngắn gọn khi lỗi
  if (res.status !== 200) {
    console.error(`❌ Error: ${res.status} - ${res.body}`);
  }

  sleep(1);
}
