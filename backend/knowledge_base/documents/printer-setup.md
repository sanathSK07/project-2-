# Printer Setup and Troubleshooting

## Overview

The company uses networked multifunction printers (MFPs) on each floor for printing, scanning, and copying. All printers require badge authentication for print job release to maintain document security.

## Adding a Network Printer

### Windows

1. Open **Settings > Devices > Printers & Scanners**.
2. Click **Add a printer or scanner** and wait for the scan to complete.
3. Select your floor's printer from the list (naming convention: **PRN-FLOOR-LOCATION**, e.g., PRN-3-EAST).
4. If the printer is not found, click **The printer that I want isn't listed**, select **Add a printer using a TCP/IP address**, and enter the IP from the printer label.
5. Windows installs the driver automatically. If prompted, select the **HP Universal Print Driver** or download from the Company Portal.

### macOS

1. Open **System Settings > Printers & Scanners**.
2. Click the **+** button and browse the network.
3. Select the printer and choose **HP Jetdirect** as the protocol.
4. The driver installs automatically via AirPrint. For advanced features, install the driver from Company Portal.

### Linux

1. Open **Settings > Printers** or use CUPS at `http://localhost:631`.
2. Click **Add Printer**, select **Network Printer**, and enter the printer's IP address.
3. Choose the IPP protocol and select the appropriate PPD driver file.

## Print Queue Issues

- **Job stuck in queue:** Open the print queue, cancel the stuck job, and resend. If the queue is frozen, restart the Print Spooler service: `net stop spooler && net start spooler` (Windows, run as admin).
- **Prints blank pages:** Check toner levels on the printer display. Try a different print driver.
- **Wrong paper size:** Verify the paper tray settings in both the print dialog and the printer's control panel.

## Badge-Release Printing

1. Send your print job to the printer as usual.
2. Walk to any floor printer and tap your employee badge on the card reader.
3. Your queued jobs appear on the touch screen. Select the jobs to print and tap **Release**.
4. Unclaimed jobs are automatically deleted after 24 hours.

## Scanning to Email

1. Tap your badge on the printer's card reader.
2. Select **Scan to Email** on the touch screen.
3. Your corporate email is pre-populated. Add additional recipients if needed.
4. Place the document on the flatbed or in the automatic feeder.
5. Choose scan settings (color, resolution, file format) and tap **Send**.

## Common Issues

- **Scanner not sending email:** Verify the printer has network connectivity. Contact IT if the SMTP relay is down.
- **Poor scan quality:** Clean the scanner glass. Increase resolution to 300 DPI for text documents.
- **Badge not recognized:** Re-register your badge at the Help Desk or try a different printer to rule out a reader issue.
