from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class display:
    def __init__( self, config:object ):
        self.i2c = busio.I2C(SCL,SDA)
        self.display = adafruit_ssd1306.SSD1306_I2C( config['DISPLAY']['WIDTH'], config['DISPLAY']['HEIGHT'], Self.i2c)
        self.padding = config['DISPLAY']['PADDING']
        self.top = self.padding
        self.bottom = self.display.height - self.padding
        self.x = 0
        self.txt_height = 8
        self.font = ImageFont.load_default()
    
    def clear_display(self):
        self.display.fill(0)
        self.display.show()

    def print_lines( self,lines:list ):
        image = Image.new("1", (self.display.width, self.display.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
        y = 0
        for line in lines:
            draw.text((self.x, self.top + y), line, font=self.font, fill= 255)
            y+=self.txt_height
        
        self.display.image(image)
        self.display.show()
