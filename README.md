# Advanced Techniques of Visual Cryptography and Steganography for Sharing of Medical Images

In the realm of medical data security, the confidentiality and integrity of diagnostic exam results are paramount. However, the use of DICOM files, which are not subject to encryption requirements, can pose significant security challenges. These files rely heavily on the security measures implemented within the healthcare institution's networks and databases. Unfortunately, these measures often prove inadequate in protecting against potential unauthorized access and malicious data injection or tampering.

## Objective
The goal of this project is to create a tool that enables the secure sharing and storage of diagnostic exam results, ensuring the confidentiality of the information while safeguarding patient privacy. This tool will operate directly on DICOM files, utilizing steganography and visual cryptography to protect and preserve the security of metadata and pixel data.

## Architecture
The proposed secure architecture involves splitting diagnostic reports into two distinct parts: one stored in the facility's archive and the other delivered directly to the patient. Access to the complete report requires the approval of the patient, represented by the obtainment of their share of the report.
