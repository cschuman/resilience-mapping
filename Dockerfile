# Multi-stage Docker build for Health Resilience Mapping API
# Created: January 31, 2025
# Purpose: Efficient, secure container for community-serving platform

# Build stage
FROM golang:1.21-alpine AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git ca-certificates tzdata

# Copy Go modules files first for better caching
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags='-w -s -extldflags "-static"' \
    -a -installsuffix cgo \
    -o api \
    ./cmd/server

# Final stage - minimal image
FROM scratch

# Copy CA certificates for HTTPS requests
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy timezone data
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Copy the binary
COPY --from=builder /app/api /api

# Copy configuration files
COPY --from=builder /app/.env.example /.env.example

# Create non-root user (even though scratch doesn't have users, this is for documentation)
USER 65534:65534

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["/api", "--health-check"]

# Labels for better container management
LABEL \
    org.opencontainers.image.title="Health Resilience Mapping API" \
    org.opencontainers.image.description="API serving 1,059 resilient communities with dignity" \
    org.opencontainers.image.vendor="Health Resilience Mapping Team" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.source="https://github.com/example/resilience-mapping-go" \
    maintainer="team@resilience-mapping.org" \
    community.impact="Serving resilient communities across America" \
    community.values="dignity-first,privacy-protected,community-owned"

# Run the application
ENTRYPOINT ["/api"]