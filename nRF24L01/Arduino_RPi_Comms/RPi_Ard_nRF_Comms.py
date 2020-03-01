# (ensure libraries located in same directory on RPi)
import RPi.GPIO as GPIO
import time
import spidev
from lib_nrf24 import NRF24

# set GPIO mode in "Broadcom SOC Channel"
GPIO.setmode(GPIO.BCM)

# setup pipe address (in hexcode)
pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

# begin the radio using GPIO08 as CE and GPIO25 as CSN pins
radio.begin(0, 25)

# set payload size as 32 bit, channel address as 76, data rate of 1 mbps and power levels as minimum
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

# open the pipes to start writing the data and print the basic details of nRF24l01
radio.openWritingPipe(pipes[0])
radio.printDetails()

# prepare a message in the string form. This message will be sent to Arduino UNO
sendMessage = list("Hi..Arduino UNO")
while len(sendMessage) < 32:
    sendMessage.append(0)

while True: # while radio is available, continue writing
    start = time.time()
    radio.write(sendMessage)
    print("Sent the message: {}".format(sendMessage))# print a debug statement of message delivery
    radio.startListening()

# if the string is completed and pipe is closed then print a debug message of timed out
while not radio.available(0):
    time.sleep(1/100)
    if time.time() - start > 2:
        print("Timed out.")  # print error message if radio disconnected or not functioning anymore
        break

# stop listening + close comms. Wait 3 secs and restart the communication with another message
radio.stopListening()
time.sleep(3)
