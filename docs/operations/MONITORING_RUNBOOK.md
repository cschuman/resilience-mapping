# Monitoring & Operations Runbook
## Health Resilience Mapping Platform

> **Last Updated**: December 30, 2025
> **On-Call**: Currently single operator (Corey)

---

## Quick Reference

### Health Check Endpoints

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `GET /health` | Full health check (includes DB) | `200` + JSON with status |
| `GET /api/tracts?limit=1` | API connectivity | `200` + JSON |

### Key Commands

```bash
# App status
fly status -a resilience-mapping

# Health checks
fly checks list -a resilience-mapping

# View logs (last 100 lines)
fly logs -a resilience-mapping -n 100

# View errors only
fly logs -a resilience-mapping | grep '"level":"error"'

# Database connection
fly postgres connect -a resilience-mapping-db

# Restart app
fly apps restart resilience-mapping
```

---

## Monitoring Stack

### Current (Basic)

| Component | Status | Notes |
|-----------|--------|-------|
| Fly.io Health Checks | ✅ Active | 10s interval, auto-restart on failure |
| Structured Logging | ✅ Active | JSON to stdout, viewable via `fly logs` |
| External Uptime | ⚠️ Not configured | See setup below |
| Error Tracking | ⚠️ Not configured | Sentry recommended |
| Metrics Dashboard | ⚠️ Not configured | Grafana Cloud free tier option |

### Health Check Configuration

From `fly.toml`:
```toml
[[http_service.checks]]
  interval = "10s"
  timeout = "2s"
  grace_period = "5s"
  method = "GET"
  path = "/health"
```

Fly.io will automatically restart unhealthy instances.

---

## Setting Up External Monitoring

### Option 1: UptimeRobot (Free Tier)

1. Sign up at https://uptimerobot.com
2. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://resilience-mapping.fly.dev/health`
   - Interval: 5 minutes
3. Configure alerts (email, Slack, etc.)

### Option 2: Better Stack (Formerly Logtail)

1. Sign up at https://betterstack.com
2. Create uptime monitor for `/health`
3. Optionally set up log forwarding from Fly.io

### Option 3: Fly.io Prometheus + Grafana

```bash
# Fly.io exposes Prometheus metrics
# Access via: https://fly-metrics.net/

# To set up Grafana Cloud:
# 1. Create free Grafana Cloud account
# 2. Add Fly.io as data source
# 3. Import Fly.io dashboard template
```

---

## Incident Response

### Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| P0 | Complete outage | Immediate | Site down, data loss |
| P1 | Major degradation | <1 hour | API errors, slow load |
| P2 | Minor issues | <4 hours | One feature broken |
| P3 | Cosmetic | Next business day | UI glitch |

### P0/P1 Response Checklist

1. **Acknowledge** - Note the time and symptoms
2. **Assess** - Run diagnostics:
   ```bash
   fly status -a resilience-mapping
   fly checks list -a resilience-mapping
   fly logs -a resilience-mapping -n 200
   ```
3. **Mitigate** - Try quick fixes:
   ```bash
   # Restart app
   fly apps restart resilience-mapping

   # If DB issue, check DB status
   fly status -a resilience-mapping-db
   ```
4. **Communicate** - Update status (if public status page exists)
5. **Resolve** - Implement fix
6. **Document** - Write postmortem

---

## Common Issues & Fixes

### Issue: Health Check Failing

**Symptoms**: `fly checks list` shows failing/warning

**Diagnosis**:
```bash
# Check logs for errors
fly logs -a resilience-mapping -n 100 | grep error

# Check if DB is reachable
fly postgres connect -a resilience-mapping-db
```

**Common Causes**:
1. Database connection pool exhausted
2. Memory limit exceeded
3. Network partition

**Fix**:
```bash
# Restart the app
fly apps restart resilience-mapping

# If persistent, scale up memory
fly scale memory 2048 -a resilience-mapping
```

### Issue: Slow Response Times

**Symptoms**: Health check shows high `responseTimeMs`

**Diagnosis**:
```bash
# Check current load
fly status -a resilience-mapping

# Check database query times
fly postgres connect -a resilience-mapping-db
# Then: SELECT * FROM pg_stat_activity;
```

**Common Causes**:
1. Missing database indexes
2. Large tile requests
3. Memory pressure

**Fix**:
```bash
# Scale horizontally
fly scale count 2 -a resilience-mapping

# Or vertically
fly scale memory 2048 -a resilience-mapping
```

### Issue: Database Connection Errors

**Symptoms**: Logs show database connection failures

**Diagnosis**:
```bash
# Check database status
fly status -a resilience-mapping-db

# Check if machines are running
fly machines list -a resilience-mapping-db
```

**Fix**:
```bash
# Restart database if needed
fly postgres restart -a resilience-mapping-db
```

### Issue: Machine Not Starting

**Symptoms**: `fly status` shows stopped machines

**Diagnosis**:
```bash
# Check machine logs
fly logs -a resilience-mapping --machine <machine-id>
```

**Common Causes**:
1. Environment variable missing
2. Build failed
3. Port binding issue

**Fix**:
```bash
# Force start
fly machines start <machine-id> -a resilience-mapping

# Or redeploy
fly deploy -a resilience-mapping
```

---

## Recovery Procedures

### Database Restore

```bash
# List available backups
fly postgres backup list -a resilience-mapping-db

# Restore from backup (DESTRUCTIVE)
fly postgres backup restore <backup-id> -a resilience-mapping-db
```

### Full Redeploy

```bash
cd app/web
fly deploy -a resilience-mapping
```

### Data Re-import

If data is corrupted or needs refresh:
```bash
# Start proxy
fly proxy 5434:5432 -a resilience-mapping-db &

# Run import
DATABASE_URL="postgres://resilience_mapping:PASSWORD@localhost:5434/resilience_mapping?sslmode=disable" \
  npx tsx scripts/import-data.ts
```

---

## Key Metrics to Watch

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Health check pass rate | 100% | <99% |
| Response time (P99) | <500ms | >2000ms |
| Error rate | 0% | >1% |
| Database connections | <20 | >80% of max |
| Memory usage | <70% | >90% |

---

## Contact & Escalation

| Role | Contact | When to Contact |
|------|---------|-----------------|
| Primary On-Call | Corey | All P0/P1 incidents |
| Fly.io Support | support@fly.io | Infrastructure issues |
| Database Issues | Fly Postgres docs | Connection/backup issues |

---

## Log Analysis

### Viewing Logs

```bash
# Real-time logs
fly logs -a resilience-mapping

# Last N lines
fly logs -a resilience-mapping -n 500

# Filter for errors (after fetching)
fly logs -a resilience-mapping -n 500 | grep '"level":"error"'
```

### Log Format

Logs are JSON structured:
```json
{
  "timestamp": "2025-12-30T15:30:00.000Z",
  "level": "info",
  "message": "Health check passed",
  "context": {
    "responseTimeMs": 34
  }
}
```

### Common Log Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `"level":"error"` | Application error | Investigate |
| `Health check failed` | DB unreachable | Check database |
| `connection refused` | Network issue | Check connectivity |
| `out of memory` | Memory pressure | Scale up |

---

## Scheduled Maintenance

### Weekly Tasks

- [ ] Review error logs for patterns
- [ ] Check disk usage on database
- [ ] Verify backup integrity

### Monthly Tasks

- [ ] Test disaster recovery procedure
- [ ] Review and update runbook
- [ ] Check for dependency updates

---

*Document created: December 30, 2025*
*Next review: January 30, 2026*
