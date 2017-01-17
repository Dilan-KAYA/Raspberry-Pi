# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import datetime

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

        
while True:
    if humidity <= 20:
        GPIO.setmode(GPIO.BCM)#Rasp uzerindeki BCM numaralandirmalari gecerli yapildi
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)#23 nolu pin ile +3.3v cikis verildi
        
        GPIO.output(23,True)#23 nolu pini aktif hale getirildi.
        
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4) # Sicaklik ve nem degerleri

    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)#23 nolu pini +3.3v cikis verdik
        GPIO.output(23,False)#23 nolu pini 0v'a dusurduk.
        
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

    time.sleep(0.5)

   
    # LCD i�in kullan�lacak GPIO pinleri planland�
    LCD_RS = 26
    LCD_E  = 19
    LCD_D4 = 13
    LCD_D5 = 6
    LCD_D6 = 5
    LCD_D7 = 11
     
    # LCD cihazinin
    LCD_WIDTH = 16    # LCD'nin her sat�r� i�in max karakter say�s�
    LCD_CHR = True    # LCD'nin ���klar� a��ld�
    LCD_CMD = False   # LCD komut modu kapat�ld�
     
    LCD_LINE_1 = 0x80 # 1. sat�r i�in LCD RAM adresi
    LCD_LINE_2 = 0xC0 # 2. sat�r i�in LCD RAM adresi
     
    # Zamanlama sabitleri
    E_PULSE = 0.0005 # Darbe zaman�
    E_DELAY = 0.0005 # Gecikme zaman�
     
    def main():
      # Main program block
      GPIO.setwarnings(False)
      GPIO.setmode(GPIO.BCM)       # BCM numaralar� kullan�ld�
      GPIO.setup(LCD_E, GPIO.OUT)  # E
      GPIO.setup(LCD_RS, GPIO.OUT) # RS
      GPIO.setup(LCD_D4, GPIO.OUT) # DB4
      GPIO.setup(LCD_D5, GPIO.OUT) # DB5
      GPIO.setup(LCD_D6, GPIO.OUT) # DB6
      GPIO.setup(LCD_D7, GPIO.OUT) # DB7
     
      # Ekran� ba�latacak metodunu �al��t�r
      lcd_init()
     
      

      # Send some test
      lcd_string("Sicaklik: %d C" % temperature,LCD_LINE_1)
      lcd_string("Nem: %d %%" % humidity,LCD_LINE_2)
     
      time.sleep(3) # 3 second delay

        
     
    def lcd_init():
      # Ekran ba�lat�ld�
      lcd_byte(0x33,LCD_CMD) # 110011 Ba�lat�ld�
      lcd_byte(0x32,LCD_CMD) # 110010 Ba�lat�ld�
      lcd_byte(0x06,LCD_CMD) # 000110 S�rg�n�n hareket y�n�
      lcd_byte(0x0C,LCD_CMD) # 001100 Ekran a��k, S�rg� kapat�ld�, Yan�p S�n�yor
      lcd_byte(0x28,LCD_CMD) # 101000 Veri uzunlu�u, sat�r say�s�, yaz� tipi boyutu
      lcd_byte(0x01,LCD_CMD) # 000001 Ekran temizleme
      time.sleep(E_DELAY)
     
    def lcd_byte(bits, mode):
      # Data pinlerine bit g�nderme
      # bits = data
      # mode = True karakter i�in
      #        False komut i�in
     
      GPIO.output(LCD_RS, mode) # RS
     
      # Y�ksek bitler
      GPIO.output(LCD_D4, False)
      GPIO.output(LCD_D5, False)
      GPIO.output(LCD_D6, False)
      GPIO.output(LCD_D7, False)
      if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
      if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
      if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
      if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
     
      # 'Enable' pinini de�i�tirme metodunu �al��t�r
      lcd_toggle_enable()
     
      # D���k bitler
      GPIO.output(LCD_D4, False)
      GPIO.output(LCD_D5, False)
      GPIO.output(LCD_D6, False)
      GPIO.output(LCD_D7, False)
      if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
      if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
      if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
      if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
     
      # 'Enable' pinini de�i�tirme metodunu �al��t�r
      lcd_toggle_enable()
     
    def lcd_toggle_enable():
      # Ge�i�i etkinle�tirme
      time.sleep(E_DELAY)
      GPIO.output(LCD_E, True)
      time.sleep(E_PULSE)
      GPIO.output(LCD_E, False)
      time.sleep(E_DELAY)
     
    def lcd_string(message,line):
        # G�r�nt�lenecek mesaj� g�nder
         
        message = message.ljust(LCD_WIDTH," ")
         
        lcd_byte(line, LCD_CMD)
         
        for i in range(LCD_WIDTH):
            lcd_byte(ord(message[i]),LCD_CHR)
         
    if __name__ == '__main__':
         
        try:
            main()
        except KeyboardInterrupt: #Klavye kesilmesi d���nda
          pass
        finally: 
            lcd_byte(0x01, LCD_CMD)
            lcd_string("",LCD_LINE_1)
            GPIO.cleanup()

