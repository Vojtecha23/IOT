from time import sleep_ms, sleep_us
from lcd_api import LcdApi

class I2cLcd(LcdApi):
    # PCF8574 backpack: P0=RS P1=RW P2=EN P3=BL P4..P7=data
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.addr = i2c_addr
        self.backlight = 0x08
        sleep_ms(30)
        for nibble in (0x30, 0x30, 0x30, 0x20):
            self._write4(nibble, 0)
            sleep_ms(5)
        super().__init__(num_lines, num_columns)
        for cmd in (0x28, 0x08, 0x01, 0x06, 0x0C):
            self.hal_write_command(cmd)
            sleep_ms(2)

    def _raw(self, bits):
        self.i2c.writeto(self.addr, bytes([bits | self.backlight]))

    def _write4(self, nibble, mode):
        data = (nibble & 0xF0) | mode
        self._raw(data)
        self._raw(data | 0x04)
        sleep_us(1)
        self._raw(data & ~0x04)
        sleep_us(50)

    def hal_write_command(self, cmd):
        self._write4(cmd & 0xF0, 0)
        self._write4((cmd << 4) & 0xF0, 0)
        if cmd in (0x01, 0x02):
            sleep_ms(2)

    def hal_write_data(self, data):
        self._write4(data & 0xF0, 1)
        self._write4((data << 4) & 0xF0, 1)
