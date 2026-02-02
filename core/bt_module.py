# bt_module.py
import os
import sys
import time
import threading
from datetime import datetime

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import banner
from debugs import debug

LCD_AVAILABLE = False
try:
    from core.LCD_Module import display_message, clear_display
    LCD_AVAILABLE = True
except ImportError:
    try:
        from LCD_Module import display_message, clear_display
        LCD_AVAILABLE = True
    except ImportError:
        display_message = lambda msg, row, duration=None: None
        clear_display = lambda: None

try:
    import bluetooth
    CLASSIC_BT_AVAILABLE = True
except ImportError:
    CLASSIC_BT_AVAILABLE = False
    debug("warn", "PyBluez not installed. Classic Bluetooth scanning disabled.")
    debug("info", "Install with: pip install pybluez")

try:
    from bluepy.btle import Scanner, DefaultDelegate, BTLEException
    BLE_AVAILABLE = True
except ImportError:
    BLE_AVAILABLE = False
    debug("warn", "bluepy not installed. BLE scanning disabled.")
    debug("info", "Install with: pip install bluepy")


class BluetoothScanModule:
    def __init__(self):
        self.devices = {}
        self.stop_scan = False
        self.lock = threading.Lock()
        
    def scan_classic_bt(self):
        if not CLASSIC_BT_AVAILABLE:
            return
            
        debug("info", "Classic BT scanner started...")
        while not self.stop_scan:
            try:
                nearby_devices = bluetooth.discover_devices(
                    duration=5,
                    lookup_names=True,
                    flush_cache=True,
                    lookup_class=False
                )
                
                with self.lock:
                    for addr, name in nearby_devices:
                        addr = addr.upper()
                        if addr not in self.devices or self.devices[addr]['type'] != 'BT/BLE':
                            self.devices[addr] = {
                                'name': name if name else 'Unknown',
                                'type': 'BT',
                                'rssi': -50,
                                'last_seen': time.time()
                            }
                        else:
                            self.devices[addr]['last_seen'] = time.time()
                            if name and self.devices[addr]['name'] == 'Unknown':
                                self.devices[addr]['name'] = name
                
            except bluetooth.BluetoothError as e:
                if not self.stop_scan:
                    debug("error", f"Classic BT scan error: {e}")
                time.sleep(2)
            except Exception as e:
                if not self.stop_scan:
                    debug("error", f"Classic BT error: {e}")
                time.sleep(2)

    def scan_ble(self):
        if not BLE_AVAILABLE:
            return
            
        debug("info", "BLE scanner started...")
        
        class ScanDelegate(DefaultDelegate):
            def __init__(self, parent):
                DefaultDelegate.__init__(self)
                self.parent = parent
                
            def handleDiscovery(self, dev, isNewDev, isNewData):
                with self.parent.lock:
                    addr = dev.addr.upper()
                    name = dev.getValueText(9) or dev.getValueText(8) or 'Unknown'
                    
                    device_type = 'BLE'
                    if addr in self.parent.devices and self.parent.devices[addr]['type'] == 'BT':
                        device_type = 'BT/BLE'
                    
                    self.parent.devices[addr] = {
                        'name': name,
                        'type': device_type,
                        'rssi': dev.rssi,
                        'last_seen': time.time()
                    }
        
        scanner = Scanner().withDelegate(ScanDelegate(self))
        
        while not self.stop_scan:
            try:
                scanner.scan(5.0, passive=True)
            except BTLEException as e:
                if not self.stop_scan:
                    debug("error", f"BLE scan error: {e}")
                    debug("error", "Make sure you run with sudo and Bluetooth is enabled")
                time.sleep(2)
            except Exception as e:
                if not self.stop_scan:
                    debug("error", f"BLE error: {e}")
                time.sleep(2)

    def display_devices(self):
        while not self.stop_scan:
            time.sleep(5)
            
            with self.lock:
                current_time = time.time()
                stale_devices = [
                    mac for mac, info in self.devices.items()
                    if current_time - info['last_seen'] > 30
                ]
                for mac in stale_devices:
                    del self.devices[mac]
                
                sorted_devices = sorted(
                    self.devices.items(),
                    key=lambda x: x[1]['rssi'],
                    reverse=True
                )
            
            os.system('clear')
            banner.bluetooth()
            debug("info", f"Scanning... Found {len(sorted_devices)} device(s)")
            debug("info", f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
            debug("info", "Press Ctrl+C to stop\n")
            
            if LCD_AVAILABLE:
                clear_display()
                display_message("  Scanning... ", 0)
                display_message(f"{len(sorted_devices)} devices   ", 1)
            
            print("─" * 76)
            print(f"{'MAC Address':<20} {'Device Name':<30} {'Type':<10}")
            print("─" * 76)
            
            if sorted_devices:
                for mac, info in sorted_devices:
                    name = info['name'][:28] if len(info['name']) > 28 else info['name']
                    print(f"{mac:<20} {name:<30} {info['type']:<10}")
            else:
                debug("warn", "No devices found yet...")
            
            print("─" * 76)

    def run(self):
        if not CLASSIC_BT_AVAILABLE and not BLE_AVAILABLE:
            debug("critical", "No Bluetooth libraries available!")
            debug("error", "Install required packages:")
            debug("info", "sudo apt-get install bluetooth libbluetooth-dev")
            debug("info", "pip install pybluez bluepy")
            if LCD_AVAILABLE:
                display_message("  No BT Libs  ", 0)
                display_message(" Install Deps ", 1)
                time.sleep(3)
            return
        
        banner.bluetooth()
        debug("info", "Starting Bluetooth scanner...")
        debug("info", "Scanning for Classic BT and BLE devices")
        debug("info", "This will scan continuously until interrupted")
        debug("info", "Make sure Bluetooth is enabled on your system\n")
        
        if LCD_AVAILABLE:
            clear_display()
            display_message(" BT Scanner   ", 0)
            display_message("  Starting... ", 1)
            time.sleep(2)
        
        if not CLASSIC_BT_AVAILABLE:
            debug("warn", "Classic BT scanning disabled (PyBluez not installed)")
        if not BLE_AVAILABLE:
            debug("warn", "BLE scanning disabled (bluepy not installed)")
        
        input("Press Enter to start scanning...")
        
        if LCD_AVAILABLE:
            clear_display()
            display_message("  Scanning... ", 0)
            display_message(" 0 devices   ", 1)
        
        try:
            threads = []
            
            if CLASSIC_BT_AVAILABLE:
                bt_thread = threading.Thread(target=self.scan_classic_bt)
                bt_thread.daemon = True
                bt_thread.start()
                threads.append(bt_thread)
            
            if BLE_AVAILABLE:
                ble_thread = threading.Thread(target=self.scan_ble)
                ble_thread.daemon = True
                ble_thread.start()
                threads.append(ble_thread)
            
            display_thread = threading.Thread(target=self.display_devices)
            display_thread.daemon = True
            display_thread.start()
            threads.append(display_thread)
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            debug("info", "Stopping scan...")
            if LCD_AVAILABLE:
                clear_display()
                display_message("   Stopping   ", 0)
                display_message("    Scan...   ", 1)
            self.stop_scan = True
            time.sleep(2)
            
            banner.scan_results()
            debug("info", f"Total devices found: {len(self.devices)}")
            
            bt_count = sum(1 for d in self.devices.values() if d['type'] == 'BT')
            ble_count = sum(1 for d in self.devices.values() if d['type'] == 'BLE')
            dual_count = sum(1 for d in self.devices.values() if d['type'] == 'BT/BLE')
            
            debug("info", f"Classic BT only: {bt_count}")
            debug("info", f"BLE only: {ble_count}")
            debug("info", f"Dual mode (BT/BLE): {dual_count}")
            debug("ok", "Scan complete.")
            
            if LCD_AVAILABLE:
                clear_display()
                display_message(f"{len(self.devices)} Total Devs", 0)
                display_message(" Scan Complete ", 1)
                time.sleep(3)
            
        except Exception as e:
            debug("error", f"Error: {e}")
            if LCD_AVAILABLE:
                display_message("  Scan Error  ", 0)
                display_message(" Check Logs  ", 1)
                time.sleep(2)
            self.stop_scan = True


if __name__ == "__main__":
    debug("info", "CryWireless V2 - Bluetooth Scanner Module - Standalone Test")
    scanner = BluetoothScanModule()
    scanner.run()