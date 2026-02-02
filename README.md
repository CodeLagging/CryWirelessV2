# CryWireless V2

**WiFi & BLE Penetration Testing Tool**

A comprehensive wireless penetration testing toolkit designed for security researchers and network administrators. CryWireless V2 provides a modular command-line interface for WiFi attacks, Bluetooth scanning, BLE spam attacks, WPA handshake capture, and IR signal transmission.

---

## Legal Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

This tool is designed for:
- Security research in controlled environments
- Authorized penetration testing with explicit permission
- Educational purposes to understand wireless security

**Unauthorized access to computer networks is illegal.** Always obtain written permission before testing any network you do not own. The developers are not responsible for misuse of this tool.

---

## Features

### 1. WiFi Attack Module
Comprehensive WiFi attack capabilities using dual-band scanning and monitor mode.

**Capabilities:**
- **Dual-band scanning** (2.4GHz & 5GHz) with automatic channel hopping
- **Monitor mode** - Automatic detection and setup
- **Network discovery** - Scan and identify all nearby WiFi networks with SSID, BSSID, and channel info
- **Multiple attack vectors:**
  - **Authentication DoS** - Denial of Service via authentication flood
  - **Michael Countermeasures DoS** - Exploit TKIP weaknesses
  - **Packet Fuzzer** - Fuzz wireless packets to crash APs
  - **Deauth Attack** - Deauthentication flood
  - **Network Flood** - SSID beacon spam
  - **WIDS Confusion** - Wireless Intrusion Detection System evasion

**Attack Tools Used:**
- `mdk4` - For various WiFi attacks
- `aircrack-ng` suite - Monitor mode management
- `scapy` - Custom packet crafting

---

### 2. BLE Attack Module
Bluetooth Low Energy spam attacks via UART-connected hardware.

**Capabilities:**
- **SourApple Spam** - iOS device popup spam
- **Samsung BLE Spam** - Samsung device notification spam
- **Google BLE Spam** - Android Fast Pair popup spam
- **SwiftPair Spam** - Windows SwiftPair notification spam
- **Attack All** - Cycle through all BLE spam attacks

**Requirements:**
- ESP32/compatible device with BLE spam firmware
- Serial connection via `/dev/ttyUSB0` (or custom port)

**Use Cases:**
- Testing BLE advertisement filtering
- Demonstrating proximity-based attack vectors
- Security awareness training

---

### 3. Bluetooth Scanner Module
Dual-mode Bluetooth/BLE device scanner with real-time updates.

**Capabilities:**
- **Classic Bluetooth scanning** - Discover Bluetooth Classic devices
- **BLE scanning** - Discover Bluetooth Low Energy devices
- **Dual-mode detection** - Identify devices supporting both protocols
- **Real-time display** - Live updates every 5 seconds
- **Device information:**
  - MAC address
  - Device name
  - Device type (BT/BLE/BT+BLE)
  - RSSI signal strength (for BLE)
- **Stale device removal** - Auto-remove devices not seen in 30 seconds

**Optional Dependencies:**
- `pybluez` - For Classic Bluetooth scanning
- `bluepy` - For BLE scanning
- Works with either or both libraries installed

---

### 4. Handshake Capture Module
WPA/WPA2 handshake capture with automatic conversion to hashcat format.

**Capabilities:**
- **Dual-band network scanning** - Find networks on 2.4GHz and 5GHz
- **Targeted handshake capture** - Select specific network to attack
- **Automatic deauthentication** - Force client reconnection to capture handshake
- **EAPOL packet capture** - Captures all 4-way handshake packets
- **Beacon frame capture** - Ensures complete handshake data
- **Hashcat conversion** - Automatic conversion to WPA*22000 format
- **File export** - Save handshakes for offline cracking

**Workflow:**
1. Scan for WiFi networks
2. Select target network
3. Automatic deauth + packet capture
4. Verify 4/4 EAPOL packets captured
5. Convert to hashcat format
6. Save to file for cracking

**Cracking Command:**
```bash
hashcat -m 22000 handshake.hc22000 wordlist.txt
```

**Requirements:**
- `hcxpcapngtool` - For hashcat conversion
- `scapy` - For packet capture
- Monitor mode capable WiFi adapter

---

### 5. IR Explorer Module
Infrared signal database browser and transmitter.

**Capabilities:**
- **IR database browser** - Navigate folder structure of IR signal files
- **Protocol support:**
  - Parsed protocols (NEC, RC5, Samsung, etc.)
  - Raw signal data
- **Serial transmission** - Send IR signals via UART device
- **Batch execution** - Execute all functions in a file sequentially
- **Command copying** - Copy IR commands to clipboard
- **Configuration system:**
  - Persistent serial port settings
  - Configurable database path
  - Adjustable timeout and delay settings

**Configuration Options:**
- `serial_port` - Default serial device path
- `database` - IR signal database directory
- `serial_timeout` - Serial communication timeout (default: 3.0s)
- `exec_all_delay` - Delay between batch commands (default: 1.0s)

**File Format:**
Supports Flipper Zero `.ir` file format with both parsed and raw signals.

**Requirements:**
- IR transmitter hardware (ESP32/Arduino with IR LED)
- Serial connection
- IR signal database (Flipper Zero format)

---

### 6. LCD Display Support (Optional)
16x2 I2C LCD display integration for status updates.

**Capabilities:**
- Real-time status messages
- Attack progress indicators
- Network scan results
- EAPOL packet counts
- Error notifications
- Standby mode display

**Requirements:**
- 16x2 I2C LCD (PCF8574 controller)
- I2C enabled on Raspberry Pi
- `RPLCD` Python library

**Supported Displays:**
- Standard 16x2 character LCD
- I2C address: 0x27 (default)

---

## 📋 System Requirements

### Hardware
- **WiFi adapter** capable of monitor mode (for WiFi attacks)
- **Optional:** ESP32/compatible device for BLE attacks
- **Optional:** IR transmitter for IR module
- **Optional:** 16x2 I2C LCD display

### Operating System
- **Raspberry Pi OS Lite** (64-bit recommended)
- **Kali Linux**
- **Ubuntu/Debian** based distributions
- **Not supported:** Windows

### WiFi Adapter Compatibility
Monitor mode support required. Recommended chipsets:
- Atheros AR9271
- Ralink RT3070/RT5370
- Realtek RTL8812AU/RTL8814AU
- MediaTek MT7612U

---

## Project Structure

```
CryWireless-V2/
├── main.py              # Main entry point
├── banner.py            # Banner and OS checks
├── debugs.py            # Colored debug/logging system
├── core/
│   ├── wifi_module.py       # WiFi attack module
│   ├── ble_module.py        # BLE spam attack module
│   ├── bt_module.py         # Bluetooth scanner
│   ├── handshake_module.py  # Handshake capture
│   ├── IResp.py             # IR Explorer
│   └── LCD_Module.py        # LCD display (optional)
└── README.md            # This file
```