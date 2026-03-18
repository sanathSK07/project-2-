# Corporate Email Setup Guide

## Overview

All employees are provisioned a corporate email account (user@company.com) hosted on Microsoft 365. This guide covers setup on desktop clients, mobile devices, and the web client, along with calendar synchronization and shared mailbox access.

## Outlook Desktop (Windows / macOS)

1. Open Microsoft Outlook and go to **File > Add Account**.
2. Enter your corporate email address and click **Connect**.
3. Outlook auto-discovers the server settings via Microsoft 365.
4. Authenticate with your corporate password and approve the MFA prompt.
5. Click **Done** once the account finishes syncing.

**Troubleshooting:** If autodiscovery fails, verify that your DNS can resolve `outlook.office365.com`. Temporarily disable VPN and retry.

## Mobile Setup (iOS / Android)

### iOS (Apple Mail)
1. Go to **Settings > Mail > Accounts > Add Account > Microsoft Exchange**.
2. Enter your email address and tap **Next**.
3. Sign in with your corporate credentials and approve MFA.
4. Enable **Mail**, **Calendar**, and **Contacts** toggles as needed.

### Android (Outlook App — Recommended)
1. Install **Microsoft Outlook** from the Google Play Store.
2. Open the app and enter your corporate email address.
3. Authenticate and approve MFA.
4. The app automatically configures mail, calendar, and contacts.

**Note:** The Outlook mobile app is required for devices managed by Intune. Native mail clients may be blocked by conditional access policies.

## Web Client (Outlook Web App)

1. Navigate to **https://outlook.office365.com** in any browser.
2. Sign in with your corporate credentials and complete MFA.
3. All mail, calendar, and contacts are available immediately.

## Calendar Synchronization

- Calendar syncs automatically across all connected Outlook clients.
- To add a colleague's calendar, open Calendar view, click **Add Calendar > From Directory**, and search by name.
- Room bookings are managed through the calendar — search for rooms prefixed with **ROOM-** when creating a meeting.

## Shared Mailbox Access

1. If you have been granted access to a shared mailbox, open Outlook and go to **File > Account Settings > Account Settings**.
2. Select your account, click **Change > More Settings > Advanced**.
3. Under **Open these additional mailboxes**, click **Add** and enter the shared mailbox name.
4. Click **OK** and restart Outlook. The shared mailbox appears in the left pane.

Alternatively, open the shared mailbox in OWA by clicking your profile icon, then **Open another mailbox**.

## Common Issues

- **Emails stuck in Outbox:** Check your internet connection and ensure attachment size is under 25 MB.
- **Calendar invites not appearing:** Verify the mailbox is not full (50 GB limit). Archive old messages.
- **Sync delays on mobile:** Force-close and reopen the Outlook app, or remove and re-add the account.
