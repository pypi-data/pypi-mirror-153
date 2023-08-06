import re
import os
import socket
import asyncio
from asyncio import shield
import math
import errno
from struct import unpack
from functools import reduce
import sys
import time
import datetime


from basic_logtools.filelog import LogFile

from networktools.time import timestamp, now
from networktools.library import my_random_string
'''
###############################################################################
CLASE ERYO  __authors__ = " David Pineda"
###############################################################################
Conexion TCP/IP con un determinado receptor.
'''
from .eryo_settings import (ERYO_FIELD_NAMES, ERYO_REC, ERYO_TABLE_NAMES,
                            BUFF_MAX_SIZE, TABLES_SIZES, ERYO_LIST, SYNC_MARKER_VALUE, BLOCKS_FLAGS,
                            ETN_reverse, TABLES_BY_FLAG, CONS, MSG_ID, signal_check)

from networktools.colorprint import rprint, gprint, bprint

from dataprotocols import BaseProtocol

"""
Check verification

int eryo_trailer_decode(char *buf, int start, eryo_trailer_t *ptr)
{
  int index=start;
  DECODE_BITS(16, buf, index, ptr->checksum);
  assert(index - start==sizeof(eryo_trailer_t));
  return index;
}

inidice = partida
decodificar 2 bytes (16 bits) a variable checksu,
compara,  la diferencia (index-start) con tamaño de eryo_trailer_y


"""


def convert_data(key, table_name, data):
    size_table = ERYO_REC[table_name]
    field_names = ERYO_FIELD_NAMES[key]
    bytes_table = TABLES_SIZES[table_name]
    try:
        unpacked = unpack(size_table, data)
    except Exception as e:
        print("No unpack on converta data", e)
        raise e
    table_dict = dict(zip(field_names, unpacked))
    return table_dict


def checksum(data):
    check_data = list(data)
    suma = sum(check_data[:-2])
    return suma


class Eryo(BaseProtocol):
    """ Class to connect to tcp port and parse ERYO messages """
    tipo = "ERYO"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_0 = None
        self.msg_bytes = None
        self.rec_dict = {}
        self.batt_status = 0
        self.tables = ERYO_TABLE_NAMES

    async def get_records(self):
        """
        Obtener bytes y traducir a un msg ERYO

        """
        idc = self.select_idc
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        sync_marker_first = SYNC_MARKER_VALUE.get('first')
        sync_marker_second = SYNC_MARKER_VALUE.get('second')
        t0 = time.time()
        try:
            if writer.transport.is_closing():
                self.logger.error(f"La conexión se cerró {writer}")
                self.status = False
                raise Exception("Conexión perdida")
            try:
                done = False
                counter = 1
                data = b''
                byte_a, byte_b = (0, 0)
                suma_bytes = 0
                msg = {}
                position = 0
                while not done:
                    byte_a = await shield(self.readbytes(reader, 1))
                    while byte_a != sync_marker_first:
                        byte_a = await shield(self.readbytes(reader, 1))
                    byte_b = await shield(self.readbytes(reader, 1))
                    if byte_b == sync_marker_second:
                        # read next 3 bytes
                        resto_header = await shield(self.readbytes(reader, 3))
                        suma_bytes += 5
                        header = byte_a+byte_b+resto_header
                        data += header
                        data_dict = convert_data(1, "ERYO_HEADER", header)
                        data_dict['MESSAGE_ID'] = MSG_ID.get(
                            data_dict.get("MESSAGE_ID"))
                        msg["ERYO_HEADER"] = data_dict
                        # POSITION_BLOCK
                        byte_count = data_dict.get("BYTE_COUNT")
                        all_bytes = await shield(self.readbytes(reader, byte_count-5))
                        data += all_bytes
                        key_2 = "POSITION_BLOCK"
                        PB_bytes = TABLES_SIZES.get(key_2)
                        suma_bytes += PB_bytes
                        PB_data = all_bytes[position:position+PB_bytes]
                        position += PB_bytes
                        PB_dict = convert_data(2, key_2, PB_data)
                        SITE_ID = PB_dict["SITE_ID"].decode("utf8")
                        PB_dict["SITE_ID"] = re.sub("\x00+$", "", SITE_ID)
                        SOLUTION_ID = PB_dict["SOLUTION_ID"].decode("utf8")
                        PB_dict["SOLUTION_ID"] = re.sub(
                            "\x00+$", "", SOLUTION_ID)
                        msg["POSITION_BLOCK"] = PB_dict
                        FLAGS = PB_dict.get('FLAGS')
                        bloques = list(filter(
                            lambda e: e[1] > 0,
                            [(block, FLAGS & value) for block, value in
                             BLOCKS_FLAGS.items()]))
                        for block_name, value in bloques:
                            if block_name == 'SAT_INFO':
                                HDR = "SAT_HDR"
                                INFO = "SAT_INFO_BLOCK"
                                nbytes = TABLES_SIZES.get(HDR)
                                suma_bytes += nbytes
                                data_block = all_bytes[position:position+nbytes]
                                position += nbytes
                                n = ETN_reverse.get(HDR)
                                data_dict = convert_data(n, HDR, data_block)
                                msg["SAT_INFO"] = {HDR: data_dict}
                                msg["SAT_INFO"]["DATA"] = []
                                NRO_SATS = data_dict.get('SAT_BLOCK_COUNT')
                                key = TABLES_BY_FLAG.get("SAT_INFO")[1]
                                for i in range(NRO_SATS):
                                    nbytes = TABLES_SIZES.get(INFO)
                                    suma_bytes += nbytes
                                    data_block = all_bytes[position:position+nbytes]
                                    position += nbytes
                                    n = ETN_reverse.get(INFO)
                                    data_dict = convert_data(
                                        n, INFO, data_block)
                                    key = "CONSTELLATION"
                                    data_dict[key] = CONS.get(
                                        data_dict.get(key))
                                    key = "SIGNAL_FLAGS"
                                    data_dict["SIGNALS"] = signal_check(
                                        data_dict.get(key))
                                    msg["SAT_INFO"]["DATA"].append(data_dict)
                            else:
                                for key in TABLES_BY_FLAG.get(block_name):
                                    nbytes = TABLES_SIZES.get(key)
                                    suma_bytes += nbytes
                                    data_block = all_bytes[position:position+nbytes]
                                    position += nbytes
                                    n = ETN_reverse.get(key)
                                    data_dict = convert_data(
                                        n, key, data_block)
                                    msg[key] = data_dict
                        # CHECKSUM
                        key = "ERYO_TRAILER"
                        nbytes = TABLES_SIZES.get(key)
                        suma_bytes += nbytes
                        checksum_bytes = all_bytes[position:position+nbytes]
                        n = ETN_reverse.get(key)
                        # checksum_bytes = await reader.readexactly(nbytes)
                        data_dict = convert_data(n, key, checksum_bytes)
                        msg[key] = data_dict
                        checksum_msg = data_dict.get("CHECKSUM")
                        chsum = checksum(data)
                        done = checksum_msg == chsum
                return done, msg
            except asyncio.TimeoutError as te:
                print(f"Timeout error on Eryo {self.station}, error {te}")
                self.logger.exception(
                    f"Get message records TimeoutError, {te}")
                return False, {}
            except asyncio.IncompleteReadError as ir:
                print(
                    f"Incomplete read on get records header, ERYO, station {self.station}")
                self.logger.exception(
                    f"Station {self.station}, Tiempo fuera al no poder leer en readbytes {n} bytes, {ir}")
                if self.raise_incompleteread:
                    raise ir
                return False, {}
            except socket.timeout as timeout:
                self.logger.warning(
                    f"La conexión se cerró, socket timeout {timeout}")
                self.on_blocking()
                self.logger.exception()
                self.status = False
                await asyncio.sleep(.1)
                return False, {}
            except Exception as ex:
                self.logger.error(
                    f"La conexión se cerró, error en comunicación {ex}")
                self.close(idc)
                self.on_blocking()
                info = f"Error {ex} en estación {self.station}. Encabezado con data {data}"
                self.logger.info(info)
                self.logger.error(ex)
                self.status = False
                await asyncio.sleep(.1)
                return False, {}
        except socket.timeout as timeout:
            self.logger.warning(
                f"La conexión se cerró, socket timeout {timeout}")
            self.on_blocking()
            self.logger.exception()
            self.status = False
            await asyncio.sleep(.1)
            return False, {}
        except Exception as ex:
            self.logger.error(
                f"La conexión se cerró, error en comunicación {ex}")
            self.close(idc)
            self.on_blocking()
            info = f"Error {ex} en estación {self.station}. Encabezado con data {data}"
            self.logger.info(info)
            self.logger.error(ex)
            self.status = False
            await asyncio.sleep(.1)
            return False, {}

    async def get_message_header(self, idc):
        self.select_idc = idc
