#!/usr/bin/env python3

import logging
import os
import random as rd

from brping import PingMessage, definitions
from ping_emulator.emulated_ping_device import EmulatedPingDevice

# socat -d -d pty,raw,echo=0 pty,raw,echo=0


class EmulatedPing360(EmulatedPingDevice):

    def __init__(self):

        super().__init__()
        self._device_id = 2

        self.logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0]) 
      
        self._mode = 0
        self._gain_setting = 0
        self._angle = 0
        self._transmit_duration = 0
        self._sample_period = 0
        self._transmit_frequency = 0
        self._number_of_samples = 200
        self._transmit = 0

    def worker(self) -> None:
        self.logger.info("Now running")
        while 1:
            incoming_message: PingMessage = self.read()
            if incoming_message:
                if incoming_message.message_id == definitions.COMMON_GENERAL_REQUEST:
                    if incoming_message.requested_id == definitions.PING360_DEVICE_ID:
                        self.answer_ping360_device_id(incoming_message)
                    elif incoming_message.requested_id == definitions.PING360_DEVICE_DATA:
                        self.answer_device_information_request(incoming_message)
                    else:
                        self.handle_ping_message(incoming_message)
                elif incoming_message.message_id == definitions.PING360_MOTOR_OFF:
                    self.answer_motor_off(incoming_message)
                elif incoming_message.message_id == definitions.PING360_RESET:
                    pass
                elif incoming_message.message_id == definitions.PING360_TRANSDUCER:
                    self.answer_transducer(incoming_message)
                else:
                    self.unknown_request(incoming_message)


    def configure(self) -> None:
        self.connect_serial(self.serial_port)


    def answer_ping360_device_id(self, request: PingMessage) -> None:

        self._reserved = request.reserved
        self.answer_common_device_id(request)


    def answer_device_information_request(self, request: PingMessage) -> None:

        answer = PingMessage(definitions.PING360_DEVICE_DATA)

        answer.mode = self._mode
        answer.gain_setting = self._gain_setting
        answer.angle = self._angle
        answer.transmit_duration = self._transmit_duration
        answer.sample_period = self._sample_period
        answer.transmit_frequency = self._transmit_frequency
        answer.number_of_samples = self._number_of_samples
        answer.data_length = self._number_of_samples
        answer.data = self.get_data()
        self.send(request, answer)

    
    def answer_motor_off(self, request: PingMessage):
        
        answer = PingMessage(definitions.COMMON_ACK)
        self.send(request, answer)


    def answer_transducer(self, request: PingMessage):

        self._mode = request.mode
        self._gain_setting = request.gain_setting
        self._angle = request.angle
        self._transmit_duration = request.transmit_duration
        self._sample_period = request.sample_period
        self._transmit_frequency = request.transmit_frequency
        self._number_of_samples = request.number_of_samples
        self._data_length = request.number_of_samples

        answer = PingMessage(definitions.PING360_DEVICE_DATA)
        answer.mode = self._mode
        answer.gain_setting = self._gain_setting
        answer.angle = self._angle
        answer.transmit_duration = self._transmit_duration
        answer.sample_period = self._sample_period
        answer.transmit_frequency = self._transmit_frequency
        answer.number_of_samples = self._number_of_samples
        answer.data_length = self._number_of_samples
        answer.data = self.get_data()
        self.send(request, answer)


    def get_data(self) -> bytearray:
        return bytearray([rd.randint(0, 254) for i in range(self._number_of_samples)])


def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    EmulatedPing360()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Ping360 sonar emulator")
    parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
    parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9092 (Not yet supported)")
    args = parser.parse_args()
    if (args.device is None and args.baudrate is None) and args.udp is None:
        parser.print_help()
        exit(1)

    p = EmulatedPing360()
    if (args.device is not None and args.baudrate is not None):
        p.connect_serial(args.device, args.baudrate)
        p.worker()
    elif args.udp is not None:
        (host, port) = args.udp.split(':')
        p.connect_udp(host, int(port))
        p.worker()

    exit(0)
