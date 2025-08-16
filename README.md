# Operational Guidelines for RPKI Delegated Certification Authorities

An IETF Internet-Draft proposing comprehensive operational guidelines for Resource Public Key Infrastructure (RPKI) delegated certification authorities and the registry operators that manage them.

## Overview

This document addresses operational challenges in the RPKI ecosystem where poorly managed delegated CAs can cause significant resource waste for validators, degrade system performance, and undermine confidence in RPKI deployment. The guidelines establish operational standards that go beyond simple "dead CA" detection to address flapping behaviors, publication quality, and comprehensive lifecycle management.

## Problem Statement

Current RPKI delegation practices allow for several problematic scenarios:

- **Dead CAs**: Completely offline CAs causing hundreds of thousands of failed validator synchronization attempts
- **Flapping CAs**: Intermittent availability patterns causing cache thrashing and validator instability
- **Poor Publication Practices**: Stale manifests, inconsistent updates, and malformed objects
- **Operational Anti-patterns**: Resource churn, publication storms, and inconsistent policies

## Key Features

### Comprehensive Coverage
- Addresses multiple CA pathologies beyond simple availability issues
- Provides guidance for CA operators, registry operators, and validator operators
- Covers complete lifecycle from pre-delegation to graceful shutdown

### Operational Standards
- Specific availability requirements (>99.5% uptime)
- Publication discipline (4-8 hour manifest intervals)
- Performance standards (10-second response times)
- Monitoring and alerting frameworks

### Enforcement Framework
- Progressive enforcement escalation procedures
- Clear timelines for detection and remediation
- Balance between operational flexibility and ecosystem protection

## Document Structure

```
1. Introduction
2. Terminology
3. Problem Statement
4. Operational Requirements for Delegated CAs
5. Addressing Problematic CA Behaviors
6. Monitoring and Alerting Framework
7. CA Lifecycle Management
8. Registry Operator Responsibilities
9. Implementation Considerations
10. Security Considerations
11. IANA Considerations
12. References
Appendix A. Operational Checklists
```

## Policy vs. Technical Standards

**Important Note**: This document establishes **technical and operational standards** while leaving **policy decisions** to individual RIRs and NIRs. 

The operational requirements (marked with MUST/SHOULD/MAY per RFC 2119) are designed to maintain reasonable technical standards for ecosystem health:

- **Technical MUSTs**: Ensure basic functionality and prevent resource waste (e.g., manifest publication, availability monitoring)
- **Operational SHOULDs**: Provide best practice guidance while allowing implementation flexibility
- **Policy Decisions**: Left to RIRs including enforcement timelines, revocation procedures, and specific delegation requirements

### RIR Policy Autonomy

Regional Internet Registries retain full autonomy over:
- Specific enforcement timelines and procedures
- Delegation approval criteria and processes
- Community notification and engagement procedures
- Appeal and remediation processes
- Integration with existing policy frameworks

## Relationship to Regional Policies

This work complements and provides technical foundation for regional policy initiatives such as:
- **APNIC prop-166**: Revocation of Persistently Non-functional RPKI Certification Authorities
- **RIPE 2025-02**: Similar CA lifecycle management proposals
- Other regional initiatives addressing RPKI operational issues

## Implementation Considerations

### Phased Deployment
1. **Phase 1**: Establish monitoring and measurement baseline
2. **Phase 2**: Implement basic operational standards
3. **Phase 3**: Deploy advanced operational features

### Stakeholder Responsibilities

**CA Operators**:
- Implement robust infrastructure and monitoring
- Follow publication discipline and operational procedures
- Maintain emergency contacts and incident response capabilities

**Registry Operators**:
- Monitor delegated CAs and enforce operational standards
- Provide support and guidance to CA operators
- Coordinate enforcement actions and community communication

**Validator Operators**:
- Implement monitoring to identify problematic CAs
- Report persistent issues to registry operators
- Participate in community feedback mechanisms

## Contributing

This is an active Internet-Draft under development. Contributions are welcome:

### Feedback Areas
- Operational experience with problematic CAs
- Specific metrics and thresholds based on real-world data
- Implementation challenges and solutions
- Integration with existing operational tools and procedures

### How to Contribute
1. **Issues**: Report problems, suggest improvements, or discuss specific requirements
2. **Pull Requests**: Propose specific text changes or additions
3. **Discussion**: Participate in mailing list discussions and working group meetings

### Review Process
- Technical review by SIDROPS working group
- Operational review by RIR technical communities
- Security review by relevant expert groups
- Community feedback from RPKI operators

## Current Status

**Draft Status**: Internet-Draft (work in progress)
**Target**: IETF Best Current Practice (BCP)
**Working Group**: SIDROPS (Secure Inter-Domain Routing Operations)

### Recent Updates
- Initial draft incorporating lessons from APNIC prop-166
- Comprehensive operational framework covering multiple CA pathologies
- Balanced approach preserving RIR policy autonomy

### Upcoming Milestones
- Working group adoption
- Community review and feedback incorporation
- Technical validation with operational data
- Coordination with RIR policy development

## References and Related Work

### IETF Standards
- [RFC 6480](https://tools.ietf.org/html/rfc6480): RPKI Architecture
- [RFC 9286](https://tools.ietf.org/html/rfc9286): RPKI Manifests and CRLs
- [RFC 8182](https://tools.ietf.org/html/rfc8182): RPKI Repository Delta Protocol

### Regional Policies
- [APNIC prop-166](https://www.apnic.net/wp-content/uploads/2025/07/prop-166-v001.txt): Revocation of Persistently Non-functional RPKI CAs
- [RIPE 2025-02](https://www.ripe.net/community/policies/proposals/2025-02/): Similar CA management proposal

### Operational Tools
- [rpki-client](https://www.rpki-client.org/): Reference validator implementation
- [RPKI Console](https://console.rpki-client.org/nonfunc.html): Non-functional CA tracking

## License

This document is subject to the rights, licenses and restrictions contained in BCP 78, and except as set forth therein, the authors retain all their rights.

## Contact

For questions, comments, or contributions, please:
- Open an issue in this repository
- Contact the document authors
- Participate in SIDROPS working group discussions

---

*This Internet-Draft provides technical and operational guidance while respecting Regional Internet Registry policy autonomy. The operational requirements are designed to maintain ecosystem health while allowing flexibility in policy implementation.*