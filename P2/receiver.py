############### Imports ###############
from time import sleep, sleep_ms

import uasyncio as asyncio
from machine import SPI, Pin
from sx127x import SX127x

#######################################


########### LoRaReceiverApp Class ######
class LoraReceiverApp:
    """
    Application to receive messages using an SX127x LoRa module.
    """

    ###### Protocol Configuration ######
    DEVICE_CONFIG = {
        "miso": 19,
        "mosi": 27,
        "ss": 18,
        "sck": 5,
        "dio_0": 23,
        "reset": 9,
    }

    LORA_PARAMETERS = {
        "frequency": 433e6,
        "tx_power_level": 2,
        "signal_bandwidth": 125e3,
        "spreading_factor": 8,
        "coding_rate": 5,
        "preamble_length": 8,
        "implicit_header": False,
        "sync_word": 0x12,
        "enable_CRC": False,
        "invert_IQ": False,
    }

    APP_PARAMETERS = {
        "led_pin": 32,
    }

    ###################################

    ###### Class constructor ######
    def __init__(self):
        """
        Initialize the LoRaReceiverApp:
        1. Set up an LED for indicating message reception.
        2. Configure the SPI interface and LoRa module.
        3. Create asynchronous tasks for handling LoRa messages and LED signaling.
        """
        self.led = Pin(LoraReceiverApp.APP_PARAMETERS["led_pin"], Pin.OUT)

        self.device_spi = SPI(
            baudrate=10000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(LoraReceiverApp.DEVICE_CONFIG["sck"], Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(LoraReceiverApp.DEVICE_CONFIG["mosi"], Pin.OUT, Pin.PULL_UP),
            miso=Pin(LoraReceiverApp.DEVICE_CONFIG["miso"], Pin.IN, Pin.PULL_UP),
        )

        self.lora = SX127x(
            self.device_spi,
            pins=LoraReceiverApp.DEVICE_CONFIG,
            parameters=LoraReceiverApp.LORA_PARAMETERS,
        )

        self.evt_msg_rx = asyncio.Event()

        asyncio.create_task(self.TriggeredLed())
        asyncio.create_task(self.CheckLoRaRx())
    
    ###################################

    ###### Check for LoRa messages ######
    async def CheckLoRaRx(self):
        """
        Asynchronously check for received LoRa messages:
        1. Continuously poll the LoRa module for new messages.
        2. When a message is received, print it and trigger the event for LED signaling.
        """
        while True:
            if self.lora.received_packet():
                print("Payload: {}".format(self.lora.read_payload()))
                self.evt_msg_rx.set()
            await asyncio.sleep_ms(10)

    ###################################

    ###### Trigger LED signaling ######
    async def TriggeredLed(self):
        """
        Asynchronously handle LED signaling when a message is received:
        1. Wait for the event indicating a received message.
        2. Turn the LED on for 250ms, then turn it off.
        3. Clear the event to wait for the next message.
        """
        while True:
            await self.evt_msg_rx.wait()
            print("Event triggered")
            self.led.value(1)
            await asyncio.sleep_ms(250)
            self.led.value(0)
            self.evt_msg_rx.clear()
    
    ###################################

    ###### Start the event loop ######
    def Loop(self):
        """
        Start the event loop to run all asynchronous tasks.
        """
        evtloop = asyncio.get_event_loop()
        evtloop.run_forever()

    ###################################

#######################################


####### Global Exception Handler #######
def set_global_exception():
    """
    Set a global exception handler to handle and print exceptions
    raised during asynchronous tasks.
    """

    def handle_exception(loop, context):
        import sys

        sys.print_exception(context["exception"])
        sys.exit()

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)


#######################################


############ Main Function ############
async def main():
    """
    Main entry point of the application:
    1. Set up global exception handling.
    2. Initialize and start the LoRaReceiverApp.
    """
    set_global_exception()
    app = LoraReceiverApp()
    await app.Loop()


#######################################

########### Application Entry #########
if __name__ == "__main__":
    asyncio.run(main())

#######################################
