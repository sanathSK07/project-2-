# WiFi Troubleshooting Guide

## Overview

The corporate campus operates three wireless networks: **Corp-Secure** (802.1X enterprise), **Corp-IoT** (device registration required), and **Corp-Guest** (visitor access). This guide covers common connection issues and their resolutions.

## Connecting to Corp-Secure

1. Open your device's WiFi settings and select **Corp-Secure**.
2. When prompted, choose **EAP-TLS** or **PEAP** as the authentication method.
3. Enter your corporate username (format: DOMAIN\username) and password.
4. Accept the server certificate from **radius.company.com** if prompted.
5. Once authenticated, the network assigns an IP automatically via DHCP.

## Certificate Errors

### "Server Certificate Not Trusted"
1. Ensure the company root CA is installed on your device. Download it from **https://certs.company.com/rootCA.crt**.
2. On Windows, double-click the file and install to **Trusted Root Certification Authorities**.
3. On macOS, open the file and add to the **System** keychain, then set it to **Always Trust**.
4. On Linux, copy to `/usr/local/share/ca-certificates/` and run `sudo update-ca-certificates`.

### Certificate Expired
- Submit a ticket to IT Security to request a renewed device certificate. Temporary workaround: use Corp-Guest and VPN.

## MAC Address Registration

Some managed devices require MAC address whitelisting:

1. Find your MAC address: run `ipconfig /all` (Windows), `ifconfig en0` (macOS), or `ip link` (Linux).
2. Submit the MAC address via ServiceNow under **Network Access > MAC Registration**.
3. Allow up to 2 hours for the registration to propagate to all access points.

## Guest Network Access

1. Connect to **Corp-Guest** (open network).
2. A captive portal opens automatically in your browser.
3. Enter the guest access code provided by your host or reception.
4. Guest sessions last 24 hours with a 50 Mbps bandwidth cap.
5. No access to internal resources is available on the guest network; use VPN if needed.

## General Troubleshooting

- **No networks visible:** Toggle WiFi off and on. Check that airplane mode is disabled.
- **Connected but no internet:** Run `nslookup google.com` to test DNS. Try DNS servers 8.8.8.8 or 10.0.0.1.
- **Slow performance:** Move closer to an access point. Avoid crowded 2.4 GHz channels by preferring 5 GHz if available.
- **Repeatedly asked for credentials:** Delete the saved Corp-Secure profile, restart WiFi, and reconnect from scratch.
