# BCP vs APNIC CPS Consistency Analysis

## Executive Summary

Your proposed BCP "Operational Guidelines for RPKI Delegated Certification Authorities" shows **strong alignment** with APNIC's Certification Practice Statement (CPS) in most areas, with several **complementary relationships** rather than conflicts. The BCP addresses operational gaps that the CPS doesn't cover while respecting existing APNIC practices.

## Key Findings

### ✅ **Strong Alignments**

1. **Availability Standards**: Your BCP's >99.5% availability requirement aligns well with APNIC's commitment to high availability services
2. **Publication Timelines**: Your 4-8 hour manifest intervals are compatible with APNIC's 2-day CRL update schedule
3. **Monitoring Philosophy**: Both documents emphasize proactive monitoring and rapid response to issues
4. **Security Controls**: Your operational requirements complement APNIC's existing security framework

### ⚠️ **Areas Requiring Attention**

1. **Enforcement Timelines**: Some discrepancies between your proposed timelines and existing APNIC practices
2. **Self-hosted vs Hosted CA Distinctions**: Your BCP could better address APNIC's dual model
3. **Business Relationship Dependencies**: APNIC's process integration needs consideration

### 🔄 **Complementary Relationships**

Your BCP fills operational gaps that APNIC's CPS doesn't address, creating a complementary rather than competing framework.

---

## Detailed Analysis

### 1. Publication and Repository Requirements

#### **APNIC CPS Requirements:**
- Certificates published within 24 hours of issuance
- CRLs published before "nextUpdate" value (2 days for production/hosted CAs)
- Repository available via rsync and RRDP protocols

#### **Your BCP Requirements:**
- Manifests updated every 4-8 hours for active CAs
- >99.5% availability over 30-day periods
- Response times within 10 seconds

#### **Consistency Assessment:** ✅ **COMPATIBLE**
Your requirements are more stringent but compatible. APNIC's 24-hour publication window allows for your 4-8 hour manifest intervals.

#### **Recommendations:**
- Acknowledge APNIC's existing 24-hour publication SLA
- Clarify that your manifest timing applies to ongoing operations, not initial publication

### 2. Availability and Reliability Standards

#### **APNIC CPS Infrastructure:**
- Redundant data centers with UPS and backup generators
- N+1 CRAC systems for environmental control
- Offsite backups within 24 hours
- External vulnerability assessments

#### **Your BCP Requirements:**
- >99.5% availability requirement
- Redundant publication infrastructure with automatic failover
- Multiple geographic endpoints
- Comprehensive monitoring with automated alerting

#### **Consistency Assessment:** ✅ **ALIGNED**
Your requirements align with APNIC's existing infrastructure commitments.

### 3. Certificate Lifecycle Management

#### **APNIC CPS Processes:**
- Certificate processing within 1 business day
- Revocation processing within 1 business day
- 4-month advance notice for expiration
- Resource modification triggers new certificate issuance

#### **Your BCP Requirements:**
- 30-day certificate renewal initiation
- 90-day advance notice for CA shutdown
- Progressive enforcement with 60-90 day timelines

#### **Consistency Assessment:** ⚠️ **REQUIRES HARMONIZATION**
Some timeline differences need reconciliation:

**Potential Conflicts:**
- Your 30-day renewal vs APNIC's 4-month notice period
- Your 90-day shutdown notice vs APNIC's 1 business day processing

**Recommendations:**
- Align renewal timelines with APNIC's existing 4-month notice period
- Clarify that shutdown procedures apply to delegated CAs, not APNIC operations

### 4. Monitoring and Enforcement Framework

#### **APNIC CPS Monitoring:**
- Weekly audit log reviews
- Automated monitoring of CA systems
- External vulnerability assessments
- Staff training and documentation requirements

#### **Your BCP Framework:**
- Automated monitoring of delegated CAs
- Progressive enforcement escalation
- Community reporting mechanisms
- Performance standards and alerting

#### **Consistency Assessment:** ✅ **COMPLEMENTARY**
Your framework extends APNIC's internal monitoring to cover delegated CAs.

### 5. Self-hosted vs APNIC-hosted CA Models

#### **APNIC CPS Distinctions:**
- **APNIC-hosted CAs**: Managed through MyAPNIC Resource Manager
- **Self-hosted CAs**: Use RFC 6492/8181 protocols with BPKI authentication
- Different authentication and access control mechanisms

#### **Your BCP Coverage:**
- Requirements apply to all delegated CAs
- Some requirements may be more relevant to self-hosted CAs
- Limited differentiation between models

#### **Consistency Assessment:** ⚠️ **NEEDS CLARIFICATION**
Your BCP should better acknowledge APNIC's dual model and how requirements apply differently.

**Recommendations:**
- Add section distinguishing requirements for hosted vs self-hosted CAs
- Clarify which monitoring responsibilities belong to APNIC vs CA operators
- Acknowledge APNIC's existing Resource Manager integration

### 6. Security and Access Controls

#### **APNIC CPS Controls:**
- FIPS 140-2 Level 3 cryptographic modules
- Multi-person control for offline CA
- LDAP-based access control with specific groups
- Physical security at APNIC facilities

#### **Your BCP Security:**
- Focus on operational security rather than cryptographic security
- Key management and rotation during operational issues
- Incident response procedures
- Risk management frameworks

#### **Consistency Assessment:** ✅ **COMPLEMENTARY**
Your operational security requirements complement APNIC's technical security controls.

---

## Specific Recommendations for BCP Revision

### 1. **Add APNIC Model Recognition**
```markdown
This document recognizes that APNIC operates two distinct delegation models:
- APNIC-hosted CAs managed through the MyAPNIC Resource Manager
- Self-hosted CAs using RFC 6492/8181 protocols

Requirements in this document apply appropriately to each model, with 
monitoring and enforcement responsibilities allocated accordingly.
```

### 2. **Harmonize Timeline References**
- Change renewal initiation from "30 days" to "at least 30 days, consistent with registry operator schedules"
- Reference APNIC's existing 4-month advance notice practices
- Clarify that enforcement timelines are policy suggestions, not technical requirements

### 3. **Add Registry Operator Integration**
```markdown
Registry operators implementing these guidelines should integrate them 
with existing operational frameworks, including:
- Certificate lifecycle management systems
- Customer relationship management processes
- Existing SLA and service level commitments
```

### 4. **Clarify Scope Boundaries**
Add clear statement that the BCP:
- Does NOT modify existing registry operator certificate policies
- Does NOT change technical protocol requirements (RFC 6492, 8181, etc.)
- DOES provide operational guidelines for delegation management

### 5. **Reference APNIC CPS Appropriately**
Add APNIC CPS as an informative reference and acknowledge existing practices:
```markdown
These guidelines are designed to complement existing registry operator 
certification practice statements and policies, such as APNIC's CPS, 
rather than replace or conflict with established practices.
```

---

## Integration Strategy

### Phase 1: Policy Alignment
- Work with APNIC to ensure timeline compatibility
- Clarify scope boundaries and responsibilities
- Establish enforcement procedure integration

### Phase 2: Technical Integration
- Define monitoring system interfaces
- Establish reporting formats and procedures
- Create implementation guidance for existing systems

### Phase 3: Community Coordination
- Align with prop-166 implementation
- Coordinate with other RIR initiatives
- Establish community feedback mechanisms

---

## Conclusion

Your BCP shows **strong overall consistency** with APNIC's CPS while addressing important operational gaps. The main areas requiring attention are:

1. **Timeline Harmonization**: Ensure enforcement and lifecycle timelines align with existing APNIC practices
2. **Model Recognition**: Better acknowledge APNIC's hosted vs self-hosted CA distinctions
3. **Scope Clarification**: Clearly delineate what your BCP adds vs what exists in current policy

With these adjustments, your BCP would provide valuable operational guidance while maintaining consistency with APNIC's established practices and commitment to the RPKI ecosystem.

The relationship is fundamentally **complementary** rather than conflicting - your BCP addresses operational management of delegated CAs while APNIC's CPS covers the technical and procedural aspects of certificate issuance and management.