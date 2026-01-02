# Disaster Recovery & Business Continuity

## RTO/RPO Targets

| Component | RTO | RPO | Strategy |
|-----------|-----|-----|----------|
| Database | 15 min | 5 min | Multi-region replication |
| Application | 5 min | N/A | Container orchestration |
| Data | 1 hour | 15 min | Automated backups |
| DNS | 5 min | N/A | Route 53 failover |

## Backup Strategy

### Database Backups
```bash
# Automated daily backups
WAL-G backup-push gs://bakhmach-backups/db/

# Point-in-time recovery
WAL-G wal-fetch 000000010000000000000001 /tmp/
```

### Application State
- Container images in Docker Hub (immutable)
- Infrastructure as Code in Git (versioned)
- Secrets in AWS Secrets Manager (encrypted)

## Failover Procedures

### Database Failover
1. Detect primary failure
2. Promote read replica to primary (30s)
3. Update connection strings
4. Verify replication health
5. Monitor queries

```bash
# Promote replica to primary
aws rds promote-read-replica db-replica

# Update DNS/connection
kubectl patch deployment bakhmach-backend \
  -p '{"spec":{"template":{"spec":{"env":[{"name":"DB_PRIMARY","value":"new-primary-endpoint"}]}}}}'
```

### Application Failover
- Kubernetes auto-restarts failed pods
- Traffic redirects to healthy instances
- Auto-scaling triggers if needed

### Regional Failover
```bash
# Switch to backup region
kubectl config use-context bakhmach-east

# Failover DNS
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123 \
  --change-batch file://failover.json
```

## Recovery Runbooks

### Complete Data Loss
1. Restore from backup (15 min)
2. Verify data integrity
3. Update replication
4. Resume transactions

### Corrupted Database
1. Restore to clean point-in-time (20 min)
2. Validate critical data
3. Reindex if necessary
4. Monitor performance

### Network Outage
1. Activate backup network (immediate)
2. Failover to secondary region (5 min)
3. Verify connectivity
4. Resume operations

## Testing Schedule

- Weekly: Backup restoration test
- Monthly: Full failover drill
- Quarterly: Multi-region failover
- Annually: Complete DR exercise

## Monitoring & Alerts

- Backup completion: Email alert if failed
- Replication lag: Alert if > 1 minute
- RTO/RPO breaches: Critical alert
- Failover health: Continuous monitoring
