############### Imports ###############
from time import sleep, sleep_ms

import uasyncio as asyncio
from machine import SPI, Pin
from sx127x import SX127x

#######################################


########### LoRaSenderApp Class ########
class LoraSenderApp:
    """
    Application to send messages using an SX127x LoRa module when a button is pressed.
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
        "btn_pin": 36,
    }

    ###############################

    ###### Class constructor ######
    def __init__(self):
        """
        Initialize the LoRaSenderApp:
        1. Set up the push button for user input.
        2. Configure the SPI interface and LoRa module.
        3. Create asynchronous tasks for button monitoring and message sending.
        """
        self.push_button = Pin(LoraSenderApp.APP_PARAMETERS["btn_pin"], Pin.IN)

        self.device_spi = SPI(
            baudrate=10000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(LoraSenderApp.DEVICE_CONFIG["sck"], Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(LoraSenderApp.DEVICE_CONFIG["mosi"], Pin.OUT, Pin.PULL_UP),
            miso=Pin(LoraSenderApp.DEVICE_CONFIG["miso"], Pin.IN, Pin.PULL_UP),
        )

        self.lora = SX127x(
            self.device_spi,
            pins=LoraSenderApp.DEVICE_CONFIG,
            parameters=LoraSenderApp.LORA_PARAMETERS,
        )

        self.lock_button_push = asyncio.Lock()
        self.lock_button_push.acquire()

        asyncio.create_task(self.TriggeredSend())
        asyncio.create_task(self.CheckButton())

    ##################################

    #### Checks button is pressed ####
    async def CheckButton(self):
        """
        Monitor the push button state:
        1. Continuously check if the button is pressed.
        2. If pressed, release the lock to signal the send task.
        """
        while True:
            if self.push_button.value():
                print("Push")
                self.lock_button_push.release()
                await asyncio.sleep_ms(250)
            await asyncio.sleep_ms(10)

    ###################################

    ###### Send message on button press ######
    async def TriggeredSend(self):
        """
        Send a message when triggered by a button press:
        1. Wait for the lock to be released by the button press.
        2. Send a predefined payload via LoRa.
        """
        while True:
            await self.lock_button_push.acquire()

            payload = "Button pressed"
            print("Sending packet: \n{}\n".format(payload))
            self.lora.println(payload)
    
    ##########################################

    ########## Start the event loop ##########
    def Loop(self):
        """
        Start the event loop to run all asynchronous tasks.
        """
        evtloop = asyncio.get_event_loop()
        evtloop.run_forever()
    
    ##########################################

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
    2. Initialize and start the LoRaSenderApp.
    """
    set_global_exception()
    app = LoraSenderApp()
    await app.Loop()


#######################################

########### Application Entry #########
if __name__ == "__main__":
    asyncio.run(main())

#######################################
