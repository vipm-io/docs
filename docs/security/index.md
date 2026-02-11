---
title: Security Overview
---

# VIPM Platform Security

[JKI](https://jki.net/) is committed to the security of the [vipm.io](https://vipm.io) platform and helping LabVIEW software package publishers and users navigate the evolving software security landscape. As regulations like the [EU Cyber Resilience Act](https://jki.net/cra/) introduce new requirements for software products, VIPM provides platform infrastructure to support publishers in meeting their security obligations, as well as [static-analysis and other security tools](https://jki.net/security/) for their software application development.

## EU Cyber Resilience Act (CRA)

The CRA introduces mandatory security requirements for software products sold in the EU, with the first compliance deadline in **September 2026**. If you publish LabVIEW-based software or components, [read our CRA overview](https://jki.net/cra/) to understand what this means for you.

!!! tip "Need help with CRA compliance?"
    JKI provides security consulting and tooling for LabVIEW-based systems.
    [Learn more at jki.net/cra](https://jki.net/cra/){ .md-button }

## Static Analysis Tools and SBOM Generation for LabVIEW Software

The [JKI Security Suite](https://jki.net/security/) provides static analysis for LabVIEW applications — scanning for vulnerabilities, identifying broken VIs, and tagging findings by CWE severity for triage and remediation. It integrates into CI/CD pipelines for continuous security validation and helps organizations meet requirements such as NIST 800-53, NASA NPR 7150.2, and DISA STIG.

VIPM also supports **Software Bill of Materials (SBOM)** generation for LabVIEW software, giving packages publishers a machine-readable inventory of their LabVIEW software components and dependencies. SBOMs are a key requirement of the [EU Cyber Resilience Act](https://jki.net/cra/) and are increasingly expected across regulated industries. Combined with static analysis, SBOM generation gives teams visibility into both the code they write and the components they depend on. 

[Learn more at jki.net/security](https://jki.net/security/){ .md-button }

## Contact

For security-related questions or to report a vulnerability in VIPM itself, contact [security@jki.net](mailto:security@jki.net).
