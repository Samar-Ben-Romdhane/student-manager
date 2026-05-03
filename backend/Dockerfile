FROM python:3.12-alpine AS builder
WORKDIR /build
RUN apk add --no-cache gcc musl-dev libpq-dev
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-alpine AS runtime
LABEL maintainer="student-manager"
RUN apk add --no-cache libpq
COPY --from=builder /root/.local /home/appuser/.local
WORKDIR /app
COPY . .
RUN addgroup -S appgroup && adduser -S appuser -G appgroup \
    && chown -R appuser:appgroup /app \
    && chown -R appuser:appgroup /home/appuser/.local
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH \
    FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "wsgi:app"]
