# GitHub Actions Workflow Documentation

## Self-Healing Multi-Domain Architecture

### Overview

This document describes the GitHub Actions workflow (`main.yml`) that implements automated domain health verification, IPFS synchronization, and autonomous multi-domain orchestration for the Bakhmach-Business-Hub project.

### Workflow Configuration

**File Location**: `.github/workflows/main.yml`

**Trigger Events**:
- **Scheduled**: Every 6 hours via cron `0 */6 * * *`
- **Manual Dispatch**: Via `workflow_dispatch` event
- **On Push**: When docs/ or .github/workflows/ paths change

### Jobs

#### 1. Domain Health Check
Verifies DNS configuration and system health across:
- `bbbhhai.com` - Primary domain (GitHub Pages)
- `auditorsec.com` - Primary audit security domain  
- `audityzer.com` - Web3 mirror domain

#### 2. IPFS Synchronization
Synchronizes documentation to IPFS network
Depends on: domain-health-check

#### 3. Autonomous Processes
Executes self-organizing autonomous agents
Depends on: domain-health-check, ipfs-sync

### Related Documentation
- [DNS Configuration](./DNS.md)
- [Web3/IPFS & Blockchain Architecture](./WEB3_IPFS_BLOCKCHAIN.md)
- [Architecture Overview](./ARCHITECTURE.md)

**Last Updated**: December 22, 2025  
**Version**: 1.0  
**Status**: Active
