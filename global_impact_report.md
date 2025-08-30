### **Impact Analysis: "Operational Guidelines for RPKI Delegated Certification Authorities" (draft-sweetser-bcp-rpki-ca-00) on ARIN, LACNIC, AFRINIC, and the NRO**

#### **Executive Summary**

Your Internet-Draft represents a significant paradigm shift from the current operational posture of ARIN, LACNIC, and AFRINIC regarding delegated Resource Public Key Infrastructure (RPKI) Certification Authorities (CAs). While APNIC and RIPE NCC are actively pursuing policies that align with your draft's principles, its adoption as a Best Current Practice (BCP) would establish a global benchmark for operational excellence that these three Regional Internet Registries (RIRs) would need to address.

The primary impact will be to transition these RIRs from a largely passive, trust-based model for delegated CAs to a proactive, data-driven framework of **monitoring and enforcement**. This will necessitate significant changes in policy, resource allocation, technical tooling, and member communication. For the NRO, the draft provides a powerful tool for promoting global operational consistency and shared best practices.

---

#### **I. Overarching Impact Across All Three RIRs**

Your draft moves beyond abstract principles and defines concrete, measurable standards. This has several universal consequences:

1.  **Establishes a Global Benchmark:** As an IETF Best Current Practice, your document becomes the authoritative reference for what constitutes "good" operation of a delegated CA. RIRs deviating from these guidelines would face questions from their technical communities about why they are not adhering to the global standard for ensuring ecosystem health.

2.  **Forces a Formal Policy Discussion:** The draft's existence will catalyze policy discussions within each RIR's community. Members aware of the BCP will inevitably raise proposals to align their RIR's practices with it. It shifts the conversation from "Should we do something?" to "How should we implement the BCP?"

3.  **Shifts the Responsibility Model:** Currently, the responsibility for a delegated CA's health lies almost entirely with the member. Your draft introduces a model of **shared responsibility**, where the Registry Operator (the RIR) has a mandatory duty to monitor all delegated CAs and enforce minimum operational standards to protect the entire ecosystem.

4.  **Provides a Blueprint for Implementation:** The draft is not just a list of problems; it is a comprehensive guide. Sections on monitoring metrics (7.1.1), phased implementation (10.1.1), and progressive enforcement (9.1.2) provide a clear roadmap, reducing the ambiguity of how an RIR would begin this process.

---

#### **II. Specific Impact on ARIN (American Registry for Internet Numbers)**

ARIN has the most mature RPKI deployment of the three, but its philosophy has been one of providing flexible options.

*   **Current State:** Strong emphasis on its Hosted RPKI solution. The Delegated and Hybrid models are available but used by a technically savvy minority. There is no active, public policy for revoking persistently non-functional delegated CAs.
*   **Impact of Your Draft:**
    *   **Policy Mandate:** ARIN would need to initiate its Policy Development Process (PDP) to create rules that reflect the BCP. This would involve justifying the need for proactive monitoring and enforcement to its community.
    *   **Technical Implementation:** ARIN would have to develop or procure tooling to actively monitor the operational metrics defined in your draft (e.g., >99.5% availability, manifest freshness) for all its delegated and hybrid customers. This is a significant engineering effort.
    *   **Enforcement Procedures:** The "Enforcement Escalation" ladder (Section 9.1.2) would require ARIN to create new operational workflows. Staff would need to be trained to manage notifications, track remediation timelines, and ultimately process revocations for non-compliance.
    *   **Member Agreement Changes:** The RPKI terms of service would likely need to be updated to reflect these new operational requirements and the potential for revocation based on operational failure.

---

#### **III. Specific Impact on LACNIC (Latin America and Caribbean Network Information Centre)**

LACNIC has a growing RPKI ecosystem and a strong focus on community education.

*   **Current State:** Hosted RPKI is the primary service. Delegated RPKI is newer (since 2019) and less established. Like ARIN, it lacks a formal policy for managing non-functional CAs.
*   **Impact of Your Draft:**
    *   **Accelerated Maturity:** Your draft would compel LACNIC to rapidly mature its delegated RPKI offering. Instead of being just a technical option, it would become a service with defined SLAs and operational oversight.
    *   **Resource Allocation:** As a developing RIR, allocating resources for the required monitoring infrastructure and staff time could be a significant challenge. The BCP provides strong justification for seeking funding or prioritizing this work.
    *   **Educational Framework:** LACNIC's strength in education is a major asset. Your draft, particularly the operational checklists in Appendix A, provides perfect source material for developing training programs, webinars, and documentation to help members understand and meet their new obligations.
    *   **Alignment with Global Trends:** Adopting these guidelines would ensure the Latin American region does not lag behind other RIRs in RPKI operational security, strengthening its position in the global internet community.

---

#### **IV. Specific Impact on AFRINIC (African Network Information Centre)**

AFRINIC's RPKI service is the least developed of the three, with a primary focus on its hosted solution.

*   **Current State:** RPKI service is almost exclusively hosted via the MyAFRINIC portal. Delegated RPKI is not a widely available or promoted service.
*   **Impact of Your Draft:**
    *   **A Blueprint for the Future:** For AFRINIC, the impact is less about changing existing practices and more about **shaping the future development** of its delegated service. Your draft provides a comprehensive blueprint for building a delegated RPKI program correctly from the outset.
    *   **Proactive vs. Reactive Design:** AFRINIC can integrate the BCP's monitoring and lifecycle management principles directly into the architecture of its future delegated offering. This would allow it to avoid the "technical debt" of having to retroactively impose standards on an existing user base.
    *   **Justification for Investment:** The draft serves as a powerful document to justify investment in the infrastructure and policies required to launch a world-class delegated RPKI service that is secure and stable by design.

---

#### **V. Impact on the NRO (Number Resource Organization)**

The NRO serves as the coordinating body for the five RIRs. It does not set policy but promotes global consistency.

*   **Current State:** Facilitates communication and collaboration among the RIRs on technical and policy matters.
*   **Impact of Your Draft:**
    1.  **Tool for Harmonization:** The NRO can use your BCP as a neutral, technically vetted document to encourage harmonization of RPKI operational standards across all five RIRs. This helps fulfill its mission of ensuring a consistent and stable global internet numbering system.
    2.  **Focal Point for Collaboration:** Your draft's recommendation for shared tooling (Section 10.2) is a perfect action item for the NRO. It could coordinate a cross-RIR effort to develop or fund open-source monitoring tools that all RIRs could use, reducing duplicated effort and cost.
    3.  **Content for Global Dialogue:** The BCP will become a key topic at NRO-coordinated meetings, such as the RIR Staff Engineering and Policy sessions, fostering a unified global approach to managing the health of the RPKI ecosystem.

---

#### **Conclusion**

Your Internet-Draft, `draft-sweetser-bcp-rpki-ca-00`, acts as a catalyst. For ARIN and LACNIC, it challenges the status quo and will force a necessary evolution toward proactive management of their delegated RPKI services. For AFRINIC, it provides a golden opportunity to build its future services on a foundation of global best practices. For the NRO, it is a key instrument for achieving global consistency.

While implementation will require significant effort in policy development, engineering, and community engagement, the long-term benefit is a more robust, reliable, and secure global RPKI ecosystem, which is the ultimate goal of the entire framework.
