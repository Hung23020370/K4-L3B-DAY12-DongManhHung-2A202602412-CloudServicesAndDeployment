# Thông Tin Deploy — Checkpoint 5

> Service đã deploy trên Render và được kiểm tra trực tiếp ngày 2026-09-29.
>
> **Chỉ ghi TÊN biến môi trường, tuyệt đối không dán giá trị API key vào đây.**
> Repo này công khai — dán khóa vào là mất khóa.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Dong Manh Hung |
| Mã học viên | 2A202602412 |
| Repo | https://github.com/Hung23020370/K4-L3B-DAY12-DongManhHung-2A202602412-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://day12-agent-83ki.onrender.com |
| Platform | Render |
| Ngày kiểm tra | 2026-09-29 |

## Biến Môi Trường Đã Set Trên Render

Ghi tên biến và **nguồn giá trị**, không ghi giá trị:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | Render tự gán |
| `AGENT_API_KEY` | ✅ | đặt trong Render dashboard, không ghi giá trị vào repo |
| `REDIS_URL` | ✅ | Redis service của Render Blueprint |
| `RATE_LIMIT_PER_MINUTE` | ✅ | 10 |
| `MONTHLY_BUDGET_USD` | ✅ | 10.0 |
| `LOG_LEVEL` | ✅ | INFO |

## Lệnh Kiểm Tra

Các lệnh smoke test service public:

```bash
# 1. Liveness
curl.exe -i https://day12-agent-83ki.onrender.com/health

# 2. Readiness (đã nối được Redis)
curl.exe -i https://day12-agent-83ki.onrender.com/ready

# 3. Không có API key — mong đợi 401
curl.exe -i -X POST https://day12-agent-83ki.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

```

## Kết Quả Chạy Thật

Kiểm tra trực tiếp ngày 2026-09-29:

```
/health: 200, {"status":"ok","service":"day12-agent","version":"1.0.0"}
/ready: 200, {"status":"ready","redis":true}
POST /ask without API key: 401
POST /ask with local AGENT_API_KEY: 200
```

`pytest tests/test_cp5.py -v`: 9 passed, 4 skipped. Đường `/ask` có xác thực
cũng trả 200; bốn bài local fallback được skip vì đang kiểm tra cloud.

## Ảnh Chụp Màn Hình

Ảnh bằng chứng được lưu trong `screenshots/`:

- `screenshots/render-dashboard.png` — cần chụp từ trang quản lý Render
- `screenshots/render-health.png` — endpoint `/health` public trên Render

---

## Nếu Dùng Phương Án Dự Phòng

Không đăng ký được tài khoản cloud? Vẫn nộp được bài, nhưng CP5 tối đa 60% điểm:

1. Đặt `LOCAL_FALLBACK=true` trong `.env`
2. Chạy `docker compose up -d` rồi kiểm tra `docker compose ps`
3. Chụp màn hình vào `screenshots/`
4. Chạy `pytest tests/test_cp5.py -v` — bộ test sẽ tự chuyển sang kiểm tra
   `http://localhost:8000`
5. Ghi rõ lý do không deploy được vào phần dưới đây:

```
Chỉ dùng phần này nếu deployment cloud không còn hoạt động; ghi rõ lý do và
không thay thông tin Render ở trên bằng URL mẫu.
```
