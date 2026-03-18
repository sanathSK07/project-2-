# VPN Setup and Configuration

## Overview

All remote employees must connect through the corporate VPN (Cisco AnyConnect) to access internal resources. This guide covers installation, configuration, and troubleshooting for all platforms.

## Prerequisites

- An active corporate account with VPN access enabled (request via ServiceNow if needed).
- Multi-factor authentication configured on your account.
- Administrator rights on your device for initial installation.

## Installation

### Windows

1. Download Cisco AnyConnect from **https://vpn.company.com** using your browser.
2. Run the installer and accept the license agreement.
3. Select **VPN Security Module** and optionally **Web Security Module**.
4. Click **Install** and restart when prompted.

### macOS

1. Navigate to **https://vpn.company.com** in Safari or Chrome.
2. Download the macOS installer package (.pkg).
3. Open the package, follow the wizard, and grant the required system extension permissions under **System Settings > Privacy & Security**.
4. Approve the system extension when prompted by macOS.

### Linux (Ubuntu/Fedora)

1. Install OpenConnect: `sudo apt install openconnect` (Ubuntu) or `sudo dnf install openconnect` (Fedora).
2. Connect via terminal: `sudo openconnect vpn.company.com --user=your_username`.
3. Enter your password and approve the MFA prompt when asked.

## Configuration

1. Open Cisco AnyConnect and enter the server address: **vpn.company.com**.
2. Click **Connect** and authenticate with your corporate credentials.
3. Approve the MFA push notification on your authenticator app.
4. Once connected, verify by accessing an internal resource such as **https://intranet.company.com**.

## Troubleshooting

### Connection Drops Frequently
- Ensure your local internet connection is stable.
- Disable any personal firewall or competing VPN client.
- Switch between TCP and UDP in AnyConnect Preferences under the **VPN** tab.

### "Login Failed" Error
- Verify your password has not expired by signing into the SSO portal.
- Confirm VPN access is enabled on your account by checking ServiceNow entitlements.

### "Unable to Establish VPN" on macOS
- Go to **System Settings > Privacy & Security** and approve the Cisco system extension.
- Reboot after granting the permission.

### Split Tunnel vs. Full Tunnel
- By default, the corporate VPN uses **split tunnel** — only internal traffic routes through VPN. If you need full tunnel for compliance, request it through your manager in ServiceNow.
