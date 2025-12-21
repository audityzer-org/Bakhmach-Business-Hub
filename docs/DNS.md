# DNS & SSL Infrastructure Registry

## Managed Domains (Cloudflare)

| Domain | Role | Focus | Status |
| :--- | :--- | :--- | :--- |
| `auditorsec.com` | Security & Audit Core | Policy, Monitoring, API Gateway | [ ] Audit Pending |
| `auditorsec.hub` | Internal Collaborative Portal | Workflows, Task Management | [ ] Audit Pending |
| `auditorsec.web3` | Decentralized Security Identity | IPFS, Web3 Credentials | [ ] Audit Pending |
| `audityzer.com` | ML & Simulation Engine | Predictive Analysis, Threat Modeling | [ ] Audit Pending |
| `audityzer.web3` | Web3 Analytics Manifest | Analytics Portfolio, Verification | [ ] Audit Pending |
| `bbbhai.com` | Bakhmach Community Hub | Public Portal, Engagement | [ ] Audit Pending |

## Cloudflare Infrastructure
- **Zones Status**: Need to verify SSL Full (Strict) for all zones.
- **WAF/Firewall**: Basic protection enabled.
- **Page Rules**: Check for HTTP -> HTTPS redirects.

## Integration Checklist (Proton)
- [ ] **MX Records**: auditorsec.com -> Proton Mail
- [ ] **SPF/DKIM/DMARC**: Verify for all sending domains.
- [ ] **Custom Domains**: Link auditorsec.hub to internal services.
