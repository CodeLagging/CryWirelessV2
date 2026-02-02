# main.py
import os
import sys
import signal
from time import sleep as wait
from colorama import Fore, Style, init
init()

LCD_AVAILABLE = False

def startup():
    global debug, banner, WiFiAttackModule, BLEAttackModule, BluetoothScanModule, HandshakeCaptureModule, IRExplorer, LCD_AVAILABLE
    
    # Add current directory and core directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(current_dir, 'core')
    
    for path in [current_dir, core_dir]:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    try:
        import banner
        from debugs import debug
        debug("info", "Core Modules Loaded")
        if os.path.exists(core_dir):
            debug("ok", f"Core directory: {core_dir}")
    except ImportError as critical:
        print(f"{Fore.RED}[CRITICAL]: Core Module {critical.name}.py is missing{Style.RESET_ALL}")
        exit(1)
    
    try:
        from core.LCD_Module import display_message, clear_display, standby_message
        globals()['display_message'] = display_message
        globals()['clear_display'] = clear_display
        globals()['standby_message'] = standby_message
        LCD_AVAILABLE = True
        debug("ok", "LCD Module loaded")
    except ImportError:
        debug("warn", "LCD Module not found. Continuing without LCD support.")
        globals()['display_message'] = lambda msg, row, duration=None: None
        globals()['clear_display'] = lambda: None
        globals()['standby_message'] = lambda: None
    
    missing = []
    try: 
        from core.wifi_module import WiFiAttackModule
        globals()['WiFiAttackModule'] = WiFiAttackModule
    except ImportError: 
        WiFiAttackModule = None
        missing.append("wifi")
    
    try: 
        from core.ble_module import BLEAttackModule
        globals()['BLEAttackModule'] = BLEAttackModule
    except ImportError: 
        BLEAttackModule = None
        missing.append("ble")
    
    try: 
        from core.bt_module import BluetoothScanModule
        globals()['BluetoothScanModule'] = BluetoothScanModule
    except ImportError: 
        BluetoothScanModule = None
        missing.append("bt")
    
    try: 
        from core.handshake_module import HandshakeCaptureModule
        globals()['HandshakeCaptureModule'] = HandshakeCaptureModule
    except ImportError: 
        HandshakeCaptureModule = None
        missing.append("handshake")
    
    try: 
        from core.IResp import IRExplorer
        globals()['IRExplorer'] = IRExplorer
    except ImportError: 
        IRExplorer = None
        missing.append("iresp")
    
    if missing == ['wifi', 'ble', 'bt', 'handshake', 'iresp']:
        debug("critical", "No attack modules available. Exiting.")
        exit(1)
    if missing:
        debug("warn", "Core Modules Limited:")
        for i in missing:
            debug("warn", f"Core Module '{i}' unavailable.")
    else: debug("ok", "All modules loaded")
    main()


def main():
    try:
        if LCD_AVAILABLE:
            display_message(" Core Modules ", 0)
            display_message("    Loaded!   ", 1)
        banner.check_os()
        wait(3)
        os.system("clear")
        banner.print_banner()
        cli_mode()
            
    except KeyboardInterrupt:
        debug("warn", "Interrupted by user")
    except Exception as e:
        debug("critical", f"Fatal error: {e}")

def cli_mode():
    try:
        if LCD_AVAILABLE:
            standby_message()
        
        print("\nSelect Module:")
        if 'WiFiAttackModule' in globals() and WiFiAttackModule:
            print("1. WiFi Attack Module")
            if LCD_AVAILABLE:
                clear_display()
                display_message("  WiFi Module ", 0)
                display_message("   Available  ", 1)
                wait(2)
        if 'BLEAttackModule' in globals() and BLEAttackModule:
            print("2. BLE Attack Module")
            if LCD_AVAILABLE:
                clear_display()
                display_message("   BLE Module ", 0)
                display_message("   Available   ", 1)
                wait(2)
        if 'BluetoothScanModule' in globals() and BluetoothScanModule:
            print("3. Bluetooth Scanner Module")
            if LCD_AVAILABLE:
                clear_display()
                display_message("   BT Scanner   ", 0)
                display_message("   Available   ", 1)
                wait(2)
        if 'HandshakeCaptureModule' in globals() and HandshakeCaptureModule:
            print("4. Handshake Capture Module")
            if LCD_AVAILABLE:
                clear_display()
                display_message(" Handshake Cap ", 0)
                display_message("   Available   ", 1)
                wait(2)
        if 'IRExplorer' in globals() and IRExplorer:
            print("5. IR Explorer Module")
            if LCD_AVAILABLE:
                clear_display()
                display_message("  IResp Module ", 0)
                display_message("   Available   ", 1)
                wait(2)
        print("0. Exit")
        wait(2)
        if LCD_AVAILABLE:
            clear_display()
            standby_message()
        
        choice = input("\nModule: ").strip()
        
        if choice == "1" or choice.lower() == "wifi":
            if 'WiFiAttackModule' not in globals() or not WiFiAttackModule:
                debug("critical", "WiFi module not loaded")
                return
            wifi = WiFiAttackModule()
            wifi.run()
        elif choice == "2" or choice.lower() == "ble":
            if 'BLEAttackModule' not in globals() or not BLEAttackModule:
                debug("critical", "BLE module not loaded")
                return
            ble = BLEAttackModule()
            ble.run()
        elif choice == "3" or choice.lower() == "bluetooth" or choice.lower() == "bt":
            if 'BluetoothScanModule' not in globals() or not BluetoothScanModule:
                debug("critical", "Bluetooth module not loaded")
                return
            bt = BluetoothScanModule()
            bt.run()
        elif choice == "4" or choice.lower() == "handshake":
            if 'HandshakeCaptureModule' not in globals() or not HandshakeCaptureModule:
                debug("critical", "Handshake Capture module not loaded")
                return
            if LCD_AVAILABLE:
                clear_display()
                display_message(" Starting HSK  ", 0)
                display_message("    Capture    ", 1)
                wait(2)
            hc = HandshakeCaptureModule()
            hc.run()
        elif choice == "5" or choice.lower() == "iresp" or choice.lower() == "ir":
            if 'IRExplorer' not in globals() or not IRExplorer:
                debug("critical", "IR Explorer module not loaded")
                return
            if LCD_AVAILABLE:
                clear_display()
                display_message(" Starting IR  ", 0)
                display_message("   Explorer   ", 1)
                wait(2)
            ir = IRExplorer()
            ir.run()
        elif choice == "0":
            debug("info", "Exiting...")
            if LCD_AVAILABLE:
                clear_display()
                display_message("   Exiting...  ", 0)
                wait(2)
        else:
            debug("error", "Invalid choice")
    
    except KeyboardInterrupt:
        debug("warn", "Interrupted by user")
        if LCD_AVAILABLE:
            display_message("  Interrupted  ", 0, 2)
    except Exception as e:
        debug("critical", f"Fatal error: {e}")
        if LCD_AVAILABLE:
            display_message("   Fatal Error  ", 0)
    finally:
        debug("info", "Cleanup complete. Exiting.")
        wait(2)
        if LCD_AVAILABLE:
            clear_display()
            display_message(" Device Standby ", 0)

if __name__ == "__main__":
    startup()