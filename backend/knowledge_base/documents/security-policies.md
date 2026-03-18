# Security Policies and Best Practices

## Overview

Information security is everyone's responsibility. This guide covers multi-factor authentication setup, phishing identification, incident reporting, and data classification policies that all employees must follow.

## Multi-Factor Authentication (MFA) Setup

1. Navigate to **https://aka.ms/mfasetup** or go to **Okta > Settings > Extra Verification**.
2. Download the **Microsoft Authenticator** app (preferred) or **Google Authenticator** on your mobile device.
3. Click **Add method** and select **Authenticator app**.
4. Scan the QR code displayed on screen with your authenticator app.
5. Enter the 6-digit verification code to confirm pairing.
6. Set up a backup method: register a phone number for SMS codes or print recovery codes and store them securely.

**Policy:** MFA is mandatory for all corporate accounts. Sessions expire after 12 hours of inactivity. Re-authentication is required for sensitive actions such as password changes and admin console access.

## Identifying Phishing Emails

Watch for these red flags:

- **Urgency or threats** — "Your account will be closed in 24 hours."
- **Suspicious sender address** — e.g., support@c0mpany-security.com instead of support@company.com.
- **Unexpected attachments** — especially .exe, .zip, or macro-enabled Office files.
- **Mismatched links** — hover over links before clicking to verify the actual URL.
- **Requests for credentials** — IT will never ask for your password via email.

## Reporting Suspicious Activity

1. **Phishing emails:** Click the **Report Phishing** button in Outlook or forward the email to **phishing@company.com**.
2. **Suspicious software or pop-ups:** Do not interact. Disconnect from the network and call the Security Operations Center (SOC) at **x7233**.
3. **Lost or stolen device:** Report immediately via ServiceNow under **Security Incident** and call the SOC to initiate a remote wipe.
4. **Unauthorized access:** If you notice unfamiliar login activity in your account, change your password and report to SOC.

## Data Classification

All company data falls into four categories:

| Classification | Description | Handling |
|---|---|---|
| **Public** | Marketing materials, published content | No restrictions |
| **Internal** | Company announcements, policies | Do not share externally |
| **Confidential** | Customer data, financials, HR records | Encrypted storage and transfer required |
| **Restricted** | Trade secrets, security keys, PII | Access on need-to-know basis, audit-logged |

## Key Policies

- **Clean desk:** Lock your screen (Win+L or Cmd+Ctrl+Q) when stepping away. Never leave sensitive documents visible.
- **Removable media:** USB drives are blocked on corporate devices. Use approved cloud storage for file transfers.
- **Password policy:** Minimum 12 characters, changed every 90 days, no reuse of the last 10 passwords.
- **Encryption:** All laptops must have BitLocker (Windows) or FileVault (macOS) enabled. IT verifies compliance weekly.
