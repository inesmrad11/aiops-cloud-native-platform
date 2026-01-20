# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**DO NOT** report security vulnerabilities through public GitHub issues.

Instead, please report them via email to: ines.mrad@esprit.tn

### Response Timeline
- **24 hours**: Initial acknowledgment
- **72 hours**: Preliminary assessment
- **7 days**: Detailed analysis and patch plan
- **30 days**: Security advisory and fix release

## Security Best Practices for This Project

### 1. Credential Management
- Never commit `terraform.tfvars` or `.env` files
- Use Azure Key Vault for production secrets
- Rotate service principal credentials quarterly

### 2. Infrastructure Security
- Network Security Groups restrict traffic to minimum required
- Azure Policy enforcement for compliance
- Regular security scanning with Azure Defender

### 3. Container Security
- Scan Docker images for vulnerabilities
- Use non-root users in containers
- Implement Pod Security Policies in AKS

### 4. Monitoring & Incident Response
- Centralized logging with Log Analytics
- Alerting for suspicious activities
- Incident response runbook in `docs/incident-response.md`

## Compliance Standards
- Aligned with CIS Azure Foundations Benchmark
- Follows Azure Well-Architected Framework Security Pillar
- Implements principle of least privilege
