# Cloud Services Guide

## Overview

The company uses Microsoft 365 as its primary cloud productivity platform, supplemented by select Google Workspace tools for specific teams. This guide covers cloud service setup, storage policies, collaboration tools, and file recovery procedures.

## Microsoft 365 Suite

### Access
1. Navigate to **https://portal.office.com** and sign in with your corporate credentials.
2. All standard apps are available: Word, Excel, PowerPoint, OneNote, and SharePoint.
3. Install desktop apps by clicking **Install Office** in the top-right corner of the portal and running the installer.

### OneDrive for Business
- Each employee gets **1 TB** of cloud storage.
- OneDrive syncs automatically with your desktop via the OneDrive client (pre-installed).
- Store work files in OneDrive, not on the local desktop or Downloads folder, to ensure backup and accessibility.
- Share files by right-clicking in OneDrive and selecting **Share**. Set permissions to **People in your organization** by default.

## Google Workspace (Select Teams)

- Teams using Google Workspace receive a secondary account (user@company-gws.com).
- Access at **https://workspace.google.com** using your provisioned credentials.
- Google Drive storage: **15 GB** per user. For larger needs, use OneDrive or request a quota increase.
- Do not store confidential data in Google Workspace unless your team has been approved for it by IT Security.

## Collaboration Tools

### Microsoft Teams
1. Download from the Company Portal or use the web version at **https://teams.microsoft.com**.
2. Sign in with your corporate credentials.
3. Your department team and channels are pre-assigned. Request additional channels through your team owner.
4. Use Teams for internal meetings, chat, and file collaboration within channels.

### Slack
1. Accept the Slack workspace invitation sent to your corporate email.
2. Download the desktop or mobile app from **https://slack.com/downloads** or the Company Portal.
3. Join channels relevant to your role. Mandatory channels: **#announcements**, **#it-support**.
4. Slack is approved for internal communication only. Do not share confidential data in Slack.

## Cloud Storage Policies

- **Do not** use personal cloud storage (personal Google Drive, Dropbox, iCloud) for company data.
- All cloud-stored files are subject to the company data classification policy (see security-policies guide).
- Files shared externally require **Confidential** classification or lower. Restricted data must never be shared externally via cloud links.
- IT runs quarterly audits of externally shared files and may revoke access if sharing policies are violated.

## File Recovery

### Accidentally Deleted Files
1. **OneDrive:** Open OneDrive in a browser, click **Recycle Bin** in the left panel. Select the file and click **Restore**. Files remain in the recycle bin for 93 days.
2. **SharePoint:** Navigate to the SharePoint site, click **Recycle Bin** in the left navigation. Restore the file. Site collection admins can recover from the second-stage recycle bin.
3. **Google Drive:** Open Google Drive, click **Trash**, right-click the file, and select **Restore**. Trash is emptied after 30 days.

### Version History
- In OneDrive or SharePoint, right-click a file and select **Version History** to view and restore previous versions.
- Google Docs: Go to **File > Version history > See version history** to browse and restore past edits.

### Beyond Recovery?
- If files are permanently deleted or corrupted, submit a ServiceNow ticket under **Data Recovery**. IT can restore from backup within the last 90 days for OneDrive and SharePoint.
