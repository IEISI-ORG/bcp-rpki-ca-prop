# RPKI Validation Error Analysis

## 1. Network Connectivity Errors

### DNS Resolution Failures
- `rpki.netiface.net: no address associated with name`
- `oto.wakuwaku.ne.jp: no address associated with name`
- `rsync.rpki.tianhai.link: no address associated with name`

### Connection Timeouts
- `sakuya.nat.moe (141.193.21.22): connect timeout`
- `rpki.leitecastro.com (23.147.168.5): connect timeout`
- `repo.rpki.space (188.114.96.3): connect timeout`
- `krill.ca-bc-01.ssmidge.xyz (170.39.49.51): connect timeout`

### Connection Refused
- `sakuya.nat.moe (2602:feda:4:dead:216:3eff:fec7:efab): connect: No route to host`
- `rpki.0i1.eu (2a03:4000:20:b7::106): connect: No route to host`
- `rpki.zappiehost.com (95.211.63.25): connect refused`
- `krill.signalx.cloud (82.26.113.7): connect refused`

### Cross-Origin Redirects
- `krill.rpki-measurement.site/rrdp/notification.xml: cross origin redirect to mea-206-81-19-33.krill.rpki-measurement.site`

## 2. Certificate and CRL Expiration Issues

### Expired CRLs (Certificate Revocation Lists)
- 47+ instances of "CRL has expired" across multiple repositories
- Major affected repositories:
  - `rsync.paas.rpki.ripe.net` (multiple subdirectories)
  - `rpki.sub.apnic.net`
  - `rpki-repo.as207960.net`
  - `rpki-repo.registro.br`
  - `rpki.folf.systems`

### Expired Certificates
- 13+ instances of "certificate has expired"
- Examples:
  - `cloudie-repo.rpki.app`
  - `krill.accuristechnologies.ca`
  - Multiple certificates in `rsync.paas.rpki.ripe.net`

### Certificates Not Yet Valid
- 7 instances in AfriNIC repository where certificates are "not yet valid"
- All from `rpki.afrinic.net/repository/member_repository`

## 3. Manifest Problems

### Missing/Invalid Manifests
- 20+ instances of "no valid manifest available"
- Affected repositories include:
  - `rpki.0i1.eu`
  - `rpki.netiface.net`
  - `rpki.leitecastro.com`
  - Multiple RIPE subdirectories

### Sequence Number Gaps
- 18+ instances of "seqnum gap detected"
- Examples:
  - APNIC: `#015385 -> #015389` (gap of 3)
  - CERNET: `#10B2 -> #10C2` (gap of 15)
  - ARIN: `#010D0C9F4328584073A821AA95A719BD15D54101 -> #010D0C9F4328584073A821AA95A719BD15D54103` (gap of 1)

### Unexpected Manifest Numbers
- 2 instances in Brazilian registry where manifest numbers were lower than expected

## 4. Resource Validation Errors

### RFC 3779 Violations
- 7 instances of "RFC 3779 resource not subset of parent's resources"
- All from Chinese registry (`rpki.cnnic.cn`)
- This means ROAs were issued for IP ranges not properly delegated to the issuing CA

## 5. TLS/Certificate Verification Issues

### TLS Handshake Failures
- `rpki-repo.canops.org: TLS handshake: certificate verification failed: unable to get local issuer certificate`

### Invalid vCard Data
- `ca.rg.net: Ghostbusters record with invalid vCard`

## 6. File Transfer Issues

### Rsync Failures
- Multiple "unexpected end of file" errors
- Repository synchronization failures forcing fallback to cache

## Summary Statistics from Log

### Error Counts:
- **Route Origin Authorizations**: 318,583 total (13 failed parse, 0 invalid)
- **Certificates**: 48,034 total (12 invalid, 113 non-functional)  
- **Manifests**: 48,022 total (113 failed parse, 18 seqnum gaps)

## Impact Analysis

### High Impact Issues:
1. **Expired CRLs** - Most critical as they prevent proper revocation checking
2. **RFC 3779 violations** - Security risk as unauthorized IP ranges could be validated
3. **DNS resolution failures** - Complete loss of access to repositories

### Medium Impact Issues:
1. **Sequence number gaps** - May indicate repository synchronization issues
2. **Missing manifests** - Reduces confidence in repository integrity
3. **Connection timeouts** - Causes delays and fallback to potentially stale cache

### Low Impact Issues:
1. **Certificates not yet valid** - Temporary issue that should self-resolve
2. **Invalid vCard data** - Cosmetic issue in contact information

## Recommendations

1. **Repository operators** should prioritize fixing expired CRLs and certificates
2. **DNS issues** need immediate attention for affected domains
3. **Chinese registry** should investigate RFC 3779 violations
4. **Network connectivity** problems suggest infrastructure issues requiring investigation
5. **Manifest synchronization** gaps indicate potential repository management problems
