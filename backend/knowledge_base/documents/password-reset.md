# Password Reset Guide

## Overview

This guide covers how to reset passwords across all corporate systems including email, VPN, Active Directory, and Single Sign-On (SSO). All passwords must meet the company policy: minimum 12 characters, at least one uppercase letter, one number, and one special character.

## Self-Service Password Reset Portal

1. Navigate to **https://passwordreset.company.com** from any browser.
2. Enter your corporate username (e.g., jdoe@company.com).
3. Complete the multi-factor authentication challenge — approve the push notification on your authenticator app or enter the SMS code.
4. Choose a new password that meets complexity requirements.
5. Confirm the new password and click **Reset**.
6. Allow up to 5 minutes for the change to propagate across all connected systems.

**Note:** You must have previously registered your MFA device to use the self-service portal. If you have not, contact the IT Help Desk.

## Admin-Assisted Password Reset

If you are locked out of MFA or the self-service portal is unavailable:

1. Call the IT Help Desk at **x4357** or submit a ticket via ServiceNow under **Access Management > Password Reset**.
2. Verify your identity by providing your employee ID and answering your security questions.
3. The technician will issue a temporary password sent to your verified personal email.
4. Log in with the temporary password and set a new permanent password immediately.

## Resetting Specific System Passwords

### Email (Microsoft 365)
- Use the self-service portal; the change applies automatically to Outlook and OWA.

### VPN (Cisco AnyConnect)
- VPN credentials sync with Active Directory. After resetting your AD password, use the new password on your next VPN connection.

### Active Directory
- Press **Ctrl + Alt + Delete** on your Windows workstation and select **Change a Password**. Enter the old password and the new password twice.

### SSO (Okta)
- Navigate to **https://company.okta.com**, click **Need help signing in?**, then **Forgot password**. Follow the email link to create a new password.

## Troubleshooting

- **Account locked after multiple attempts:** Wait 30 minutes for automatic unlock or call the Help Desk.
- **Password change not syncing:** Sign out of all devices, wait 10 minutes, then sign back in.
- **MFA device lost or replaced:** Contact the Help Desk to register a new device before resetting your password.
