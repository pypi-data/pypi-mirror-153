#     Copyright 2021. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import time
from simplejson import dumps

from thingsboard_gateway.connectors.mqtt.mqtt_uplink_converter import MqttUplinkConverter, log


class CustomMqttUplinkConverter(MqttUplinkConverter):
    def __init__(self, config):
        self.__config = config.get('converter')
        self.dict_result = {}

    def convert(self, topic, body, deviceID):
        try:
            # getting all data after last '/' symbol in this case: if topic = 'devices/temperature/sensor1' device name will be 'sensor1'.
            self.dict_result["deviceName"] = deviceID#topic.split("/")[-1]
            self.dict_result["deviceType"] = "AC"  # just hardcode this
            self.dict_result["telemetry"] = []  # template for telemetry array
            # Replacing the 0x (if '0x' in body), needs for converting to bytearray
            #bytes_to_read = body.replace("0x", "")
            # Converting incoming data to bytearray
            #converted_bytes = bytearray.fromhex(bytes_to_read)
            if self.__config.get("extension-config") is not None:
                # Processing every telemetry key in config for extension
                for telemetry_key in self.__config["extension-config"]:
                    value = body
                    # reading every value with value length from config
                    #for _ in range(self.__config["extension-config"][telemetry_key]):
                        # process and remove byte from processing
                        # value = value * 256 + converted_bytes.pop(0)
                    # creating telemetry data for sending into Thingsboard
                    telemetry_to_send = {telemetry_key.replace("Bytes", ""): value}
                    log.info("telemetry: %s", telemetry_to_send)

                    self.dict_result["telemetry"].append(telemetry_to_send)
                    # adding data to telemetry array
            else:
                # if no specific configuration in config file - just send data which received
                self.dict_result["telemetry"] = {"data": int(body, 0)}
            return self.dict_result

        except Exception as e:
            log.exception('Error in converter, for config: \n%s\n and message: \n%s\n', dumps(
                self.__config), body)
            log.exception(e)
