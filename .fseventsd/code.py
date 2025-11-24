# Minimal "code.py": Enable BLE status LED then reboot module
# Requires board pins: BLE_TX, BLE_RX, BLE_CLR
# Sends RN-style commands over UART as BYTES.
import time
import board
import digitalio
from busio import UART

BAUDRATE = 115200
ACTIVE_LOW_RESET = True   # BLE_CLR is active-low on many modules

def _error(msg):
    try:
        print(msg)
    except Exception:
        pass

def _enable_ble_status_led_and_reboot(
    baudrate=BAUDRATE,
    active_low_reset=ACTIVE_LOW_RESET,
    boot_delay_s=1.0
):
    # --- Resolve pins ---
    tx = getattr(board, "BLE_TX", None)
    rx = getattr(board, "BLE_RX", None)
    clr = getattr(board, "BLE_CLR", None)
    if not (tx and rx and clr):
        _error("Missing BLE pins (BLE_TX, BLE_RX, BLE_CLR). Aborting.")
        return

    # --- Reset pin setup ---
    ble_reset = digitalio.DigitalInOut(clr)
    ble_reset.direction = digitalio.Direction.OUTPUT
    # idle
    ble_reset.value = True if active_low_reset else False
    time.sleep(0.01)

    # --- Reset pulse ---
    ble_reset.value = False if active_low_reset else True
    time.sleep(0.2)
    ble_reset.value = True if active_low_reset else False
    time.sleep(boot_delay_s)  # allow module to boot fully

    # --- UART ---
    ble = UART(tx, rx, baudrate=baudrate, timeout=0.2, receiver_buffer_size=256)
    try:
        print("Entering command mode...")
        for _ in range(3):
            ble.write(b"$")
            time.sleep(0.2)
        ble.write(b"\r\n")
        time.sleep(0.5)
        _ = ble.read(64)

        print("Enabling status LED...")
        ble.write(b"SR,0001\r\n")
        time.sleep(0.5)
        _ = ble.read(64)

        print("Rebooting module...")
        ble.write(b"R,1\r\n")
        time.sleep(0.5)
        _ = ble.read(64)

        print("Done. BLE status LED should now be enabled.")
    finally:
        try:
            ble.deinit()
        except Exception:
            pass
        try:
            ble_reset.deinit()
        except Exception:
            pass

if __name__ == "__main__":
    try:
        _enable_ble_status_led_and_reboot()
    except Exception as e:
        _error("BLE status LED setup failed: {}".format(e))
