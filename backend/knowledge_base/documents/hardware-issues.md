# Hardware Troubleshooting Guide

## Overview

This guide covers common hardware problems with corporate laptops, monitors, and peripherals. Before contacting the Help Desk, try the relevant troubleshooting steps below to resolve the issue quickly.

## Laptop Won't Boot

1. **Check power:** Connect the charger and verify the LED indicator lights up. Try a different power outlet and cable if available.
2. **Hard reset:** Disconnect the charger, hold the power button for 15 seconds, reconnect the charger, and press the power button normally.
3. **External display test:** Connect an external monitor to rule out a failed laptop screen.
4. **BIOS access:** If the device powers on but does not boot into Windows/macOS, press **F2** or **Esc** at startup to enter BIOS and check that the boot drive is detected.
5. If none of these work, submit a hardware ticket in ServiceNow with the asset tag number found on the bottom of the device.

## Blue Screen of Death (BSOD)

1. Note the **stop code** displayed on the blue screen (e.g., CRITICAL_PROCESS_DIED, MEMORY_MANAGEMENT).
2. Restart the device. If it boots normally, check **Event Viewer > Windows Logs > System** for related errors.
3. Run `sfc /scannow` in an elevated Command Prompt to repair system files.
4. Update drivers via **Device Manager** or the Company Portal's driver update tool.
5. If BSODs recur, submit a ticket with the stop code and any recent changes you made (software installs, updates).

## Slow Performance

1. Restart the device — many issues clear after a fresh boot.
2. Check **Task Manager** (Ctrl+Shift+Esc) or **Activity Monitor** for processes consuming excessive CPU or memory.
3. Verify free disk space: maintain at least 10% free. Use **Disk Cleanup** (Windows) or clear caches on macOS.
4. Ensure Windows Update or macOS Software Update is not running in the background.
5. If the device is older than 3 years, request a hardware refresh through your manager in ServiceNow.

## External Monitor Setup

1. Connect the monitor using the appropriate cable (USB-C, HDMI, or DisplayPort). Use a docking station if your laptop has limited ports.
2. On Windows, press **Win+P** and select **Extend** or **Duplicate**.
3. On macOS, go to **System Settings > Displays** and arrange the monitor layout.
4. If the monitor is not detected, try a different cable or port. Update the graphics driver if necessary.

## Keyboard and Mouse Pairing (Bluetooth)

1. Put the peripheral into pairing mode (usually hold the Bluetooth button for 3-5 seconds until the LED flashes).
2. On your laptop, go to **Settings > Bluetooth & Devices** (Windows) or **System Settings > Bluetooth** (macOS).
3. Select the device from the discovered list and click **Pair**.
4. If pairing fails, remove the device from the Bluetooth list, restart Bluetooth, and try again.
5. For USB receiver peripherals, plug the receiver into a USB-A port and install any required drivers from the Company Portal.

## When to Request a Replacement

- Device is more than 4 years old and experiencing chronic issues.
- Physical damage to the screen, keyboard, or chassis.
- Battery health below 60% (check in BIOS or system report).

Submit a **Hardware Replacement Request** in ServiceNow with your asset tag and a description of the issue.
