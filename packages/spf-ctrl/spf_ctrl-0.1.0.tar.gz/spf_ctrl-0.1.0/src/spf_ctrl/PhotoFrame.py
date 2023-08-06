import logging
import struct
import time
from typing import Optional

import usb.core
from usb.util import CTRL_TYPE_STANDARD, CTRL_IN, CTRL_RECIPIENT_DEVICE, CTRL_TYPE_VENDOR

VENDOR_ID = 0x04e8
KNOWN_MODELS = {
    'SPF-72H': 0x200a,
    'SPF-75H': 0x200e,
    'SPF-83H': 0x200c,
    'SPF-85H': 0x2012,
    'SPF-87H': 0x2033,
    'SPF-87H (old firmware)': 0x2025,
    'SPF-107H': 0x2035,
    'SPF-107H (old firmware)': 0x2027
}


class PhotoFrame:
    @staticmethod
    def find():
        dev: Optional[usb.core.Device]

        for name, product_id in KNOWN_MODELS.items():
            # find photo frame in storage mode
            dev = usb.core.find(idVendor=VENDOR_ID, idProduct=product_id)
            if dev:
                logging.info(f'found {name} in storage mode')
                logging.info(f'switch to display mode')

                # switch to display mode
                dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0xfe, 0xfe, 254)

                # wait for device to change mode
                time.sleep(3)

            # find photo frame in display mode
            dev = usb.core.find(idVendor=VENDOR_ID, idProduct=product_id + 1)
            if dev:
                logging.info(f'found {name} in display mode')
                dev.set_configuration()

                # display mode setup
                result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x04, 0x00, 0x00, 1)
                if result.tolist() != [0x03]:
                    raise ValueError('response not as expected')

                return PhotoFrame(dev)

        raise ValueError('no device found')

    def __init__(self, dev: usb.core.Device, chunk_size: int = 0x4000, buffer_size: int = 0x20000):
        self._dev: usb.core.Device = dev
        self._chunk_size: int = chunk_size
        self._buffer_size: int = buffer_size

    def send(self, data: bytes, timeout: int = 1000):
        # add header to data
        size = struct.pack('I', len(data))
        header = b'\xa5\x5a\x09\x04' + size + b'\x46\x00\x00\x00'

        data = header + data

        # send according to buffer size
        buffer_pos = 0
        while buffer_pos < len(data):
            # create buffer and add padding
            buffer = data[buffer_pos:buffer_pos + self._buffer_size]
            buffer = buffer + bytes(b'\x00') * (self._buffer_size - len(buffer))

            buffer_pos += self._buffer_size

            # write in chunks
            chunk_pos = 0
            while chunk_pos < self._buffer_size:
                chunk = buffer[chunk_pos:chunk_pos + self._chunk_size]
                self._dev.write(0x02, chunk, timeout)

                chunk_pos += self._chunk_size
