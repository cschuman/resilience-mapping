# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously, especially given that this project handles research data about communities.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:
1. **Email**: Contact the repository owner directly
2. **GitHub Security Advisories**: Use the "Security" tab to report privately

### What to Include

- Type of vulnerability
- Full paths of source file(s) related to the issue
- Steps to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Target**: Dependent on severity

### What to Expect

1. Acknowledgment of your report
2. Assessment of the vulnerability
3. Plan for addressing the issue
4. Credit in the fix (unless you prefer to remain anonymous)

## Security Considerations

### Data Handling

- All data used is publicly available (CDC PLACES, USDA FARA, Census)
- No personally identifiable information (PII) is collected or stored
- Census tract data is aggregated at the population level

### Application Security

- The application follows OWASP security guidelines
- Dependencies are regularly scanned for vulnerabilities
- API endpoints are rate-limited and validated

## Scope

The following are in scope for security reports:
- The web application at resilience-mapping.fly.dev
- API endpoints
- Data processing pipelines
- Authentication/authorization issues

The following are out of scope:
- Denial of service attacks
- Social engineering
- Physical security
- Issues in third-party services

Thank you for helping keep this research platform secure.
