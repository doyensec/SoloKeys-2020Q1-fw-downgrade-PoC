from intelhex import IntelHex
import json
import base64
from solo import helpers
import solo.client
import io
from tqdm import tqdm

FW_FILE = "../firmware-3.0.0.json"

with open(FW_FILE) as f:
    data = json.load(f)

fw = base64.b64decode(helpers.from_websafe(data["firmware"]).encode()).decode("utf-8")
fw_file = io.StringIO(fw)
ih = IntelHex(fw_file)

sig = base64.b64decode(helpers.from_websafe(data["versions"][">2.5.3"]["signature"]).encode())

client = solo.client.find()
client.use_hid()

if not client.is_solo_bootloader():
    print("[!] Please put the SoloKey in bootloader mode")
    exit(1)

# desired_version = b"\x03\x00\x00\x00"    # make the bootloader believe we're flashing 3.0.0.0
# desired_version = b"\x03\x00\x00\x02"    # make the bootloader believe we're flashing 3.0.0.2
desired_version = b"\x03\x00\x25\x00"  # make the bootloader believe we're flashing 3.0.37.0

version_offset = ih.tobinstr().find(desired_version)
correct_version_offset = ih.tobinstr().rfind(b"\x03\x00\x00\x00")
if version_offset == -1:
    print("Cannot find version bytes!")
    exit(1)

print("[+] Using version bytes at offset 0x{:x} instead of 0x{:x}".format(version_offset, correct_version_offset))

print("[+] Flashing firmware...")
chunk_size = 2048
start_address, end_address = ih.segments()[0]
version_bytes_address = start_address + version_offset

for chunk_start in tqdm(range(start_address, end_address, chunk_size)):
    chunk_end = min(chunk_start + chunk_size, end_address)
    data = ih.tobinarray(start=chunk_start, size=chunk_end - chunk_start)
    client.write_flash(chunk_start, data)

print("\n[+] Rewriting version bytes...")

for chunk_start in tqdm(range(version_bytes_address, version_bytes_address + 4, chunk_size)):
    chunk_end = min(chunk_start + chunk_size, version_bytes_address + 4)
    data = ih.tobinarray(start=chunk_start, size=chunk_end - chunk_start)
    client.write_flash(chunk_start, data)

client.verify_flash(sig)
