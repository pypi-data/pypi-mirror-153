#!/usr/bin/env python3

import logging
import os
import random as rd

from brping import PingDevice, PingMessage, definitions


class EmulatedPingDevice(PingDevice):


    def __init__(self):

        super().__init__()

        self.logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0]) 

        self._device_type = 0 # 0: Unknown; 1: Ping Echosounder; 2: Ping360
        self._device_revision = 0

        self._device_id = 1

        self._firmware_version_major = 1
        self._firmware_version_minor = 0
        self._firmware_version_patch = 0 

        self._protocol_version_major = 1
        self._protocol_version_minor = 0
        self._protocol_version_patch = 0 

        self._reserved = 0


    def handle_ping_message(self, incoming_message):
        if incoming_message:
            if incoming_message.message_id == definitions.COMMON_GENERAL_REQUEST:
                if incoming_message.requested_id == definitions.COMMON_PROTOCOL_VERSION:
                    self.answer_commmon_protocol_request(incoming_message)
                elif incoming_message.requested_id == definitions.COMMON_DEVICE_INFORMATION:
                    self.answer_common_device_information_request(incoming_message)
                elif incoming_message.requested_id == definitions.COMMON_SET_DEVICE_ID:
                    self.answer_common_device_id(incoming_message)
                else:
                    self.unknown_request(incoming_message)


    def answer_commmon_protocol_request(self, request: PingMessage) -> None:

        answer = PingMessage(definitions.COMMON_PROTOCOL_VERSION)
        answer.protocol_version_major = self._protocol_version_major
        answer.protocol_version_minor = self._protocol_version_minor
        answer.protocol_version_patch = self._protocol_version_patch
        self.reserved = self._reserved
        self.send(request, answer)


    def answer_common_device_information_request(self, request: PingMessage) -> None:

        answer = PingMessage(definitions.COMMON_DEVICE_INFORMATION)

        answer.device_type = self._device_type
        answer.device_revision = self._device_revision
        answer.firmware_version_major = self._firmware_version_major
        answer.firmware_version_minor = self._firmware_version_minor
        answer.firmware_version_patch = self._firmware_version_patch
        self.reserved = self._reserved
        self.send(request, answer)


    def answer_common_device_id(self, request: PingMessage) -> None:

        temp = self._device_id
        self._device_id = request.device_id
        self.logger.info(f"Emulated device id has been changed from {temp} to {self._device_id}")

        answer = PingMessage(definitions.COMMON_ACK)
        self.send(request, answer)


    def unknown_request(self, request: PingMessage) -> None:

        answer = PingMessage(definitions.COMMON_NACK)
        self.send(request, answer)
        

    def send(self, request: PingMessage, answer: PingMessage):
        answer.dst_device_id = request.src_device_id
        answer.src_device_id = self._device_id

        answer.pack_msg_data()
        self.write(answer.msg_data)
