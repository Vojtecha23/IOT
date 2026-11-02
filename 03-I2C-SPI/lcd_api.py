from time import sleep_ms

class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_ENTRY_INC = 0x02
    LCD_ON_CTRL = 0x08
    LCD_ON_DISPLAY = 0x04
    LCD_ON_CURSOR = 0x02
    LCD_ON_BLINK = 0x01
    LCD_DDRAM = 0x80

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.display_on = True

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        sleep_ms(2)
        self.cursor_x = self.cursor_y = 0

    def move_to(self, x, y):
        if not (0 <= x < self.num_columns and 0 <= y < self.num_lines):
            raise ValueError('LCD position')
        self.cursor_x, self.cursor_y = x, y
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.hal_write_command(self.LCD_DDRAM | (x + offsets[y]))

    def putchar(self, char):
        self.hal_write_data(ord(char))
        self.cursor_x += 1

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.move_to(0, (self.cursor_y + 1) % self.num_lines)
            else:
                self.putchar(char)

    def hal_write_command(self, cmd):
        raise NotImplementedError

    def hal_write_data(self, data):
        raise NotImplementedError
