# ==========================================
# STAGE 1: Builder (cài đặt dependency)
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements.txt TRƯỚC để tận dụng Docker layer cache
COPY requirements.txt .

# Cài đặt dependency vào thư mục riêng /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==========================================
# STAGE 2: Runtime (Image tối giản cho production)
# ==========================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Tạo non-root user để chạy ứng dụng (bảo mật)
RUN useradd --create-home --uid 10001 appuser

# Chỉ copy kết quả dependency từ stage builder sang runtime
COPY --from=builder /install /usr/local

# Copy mã nguồn ứng dụng SAU khi đã cài đặt dependencies
COPY app/ ./app
COPY utils/ ./utils

# Chuyển quyền sở hữu thư mục làm việc cho non-root user và switch user
RUN chown -R appuser:appuser /app
USER appuser

# Cấu hình HEALTHCHECK kiểm tra endpoint /health định kỳ
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + str('${PORT:-8000}') + '/health').read()" || exit 1

EXPOSE 8000

# Chạy app qua shell để đọc được biến môi trường PORT (cloud tự gán port)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]