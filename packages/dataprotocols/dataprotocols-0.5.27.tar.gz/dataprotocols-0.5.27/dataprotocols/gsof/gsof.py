from struct import unpack, error as struct_error

import socket
from asyncio import shield
import asyncio

from networktools.time import timestamp

from networktools.colorprint import rprint, bprint

from dataprotocols import BaseProtocol

'''
###############################################################################
CLASE GSOF  __authors__ = "Henry T. Berglund ----> David Pineda"
###############################################################################
Conexion TCP/IP con un determinado receptor.
Updated to python3.5 by David Pineda @pineiden dpineda@csn.uchile.cl

'''

try:
    from .gsof_settings import gsof_field_names, gsof_rec, gsof_table_names
except Exception:
    from gsof_settings import gsof_field_names, gsof_rec, gsof_table_names


def checksum256(data_check):
    """Calculate checksum"""
    # ord: string -> unicode int
    # map(a,b): opera a en b
    # list entrega lista o arrays
    # formula: 	(Status + type + length + data bytes) modulo 256
    data_bytes = data_check.get("DATA_BYTES")
    checksum = data_check.get("CHECKSUM")
    chk256 = sum(data_bytes) % 256
    return checksum == chk256


class Gsof(BaseProtocol):
    """ Class to connect to tcp port and parse GSOF messages """
    tipo = "GSOF"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_0 = None
        self.msg_bytes = None
        self.rec_dict = {}
        self.batt_status = 0
        self.tables = gsof_table_names
        # manage asyncronous clients

    def __repr__(self):
        return f"Gsof({self.station},{self.address})"

    def __str__(self):
        return f"Gsof({self.station},{self.address})"

    async def get_message_header(self, idc):
        # receive data from source
        # max amount of data
        # N ammount of bites
        if idc in self.clients:
            self.data_check = {}
            reader = self.clients[idc]['reader']
            writer = self.clients[idc]['writer']
            self.timestamp = timestamp()
            BytesData = 7
            bufsize = BytesData
            msg_field_names = ('STX', 'STATUS', 'TYPE', 'LENGTH',
                               'T_NUM', 'PAGE_INDEX', 'MAX_PAGE_INDEX')

            try:
                if writer.transport.is_closing():
                    self.logger.error(f"La conexión se cerró {writer}")
                    self.status = False
                    raise Exception(
                        f"Conexión perdida para idc {idc} station {self.station}")
                data = None

                try:
                    data = await shield(self.readbytes(reader, bufsize))
                    self.msg_dict = dict(zip(
                        msg_field_names,
                        unpack('>' + str(bufsize) + 'B', data)))
                    campos_unpack = unpack('>%dB' % bufsize, data)
                    self.msg_dict = dict(zip(msg_field_names, campos_unpack))
                    status = self.msg_dict['STATUS']
                    bin_status = bin(status)
                    batt_status = bin_status[3]
                    self.msg_dict["LOW_BATTERY"] = bool(int(batt_status))
                    self.msg_bytes = await shield(self.readbytes(reader, self.msg_dict['LENGTH']-3))
                    self.msg_0 = self.msg_bytes
                    n = 2
                    check_etx = await shield(self.readbytes(reader, n))
                    (checksum, etx) = unpack('>2B', check_etx)
                    self.data_check["CHECKSUM"] = checksum
                    self.data_check["DATA_BYTES"] = list(self.msg_bytes+data[1:])
                    self.checksum = checksum256(self.data_check)
                    self.msg_dict["CHECKED"] = self.checksum
                except asyncio.CancelledError as ce:
                    self.logger.exception("Get message CancelledError, %s" % ce)
                    raise ce                
                except asyncio.TimeoutError as te:
                    self.logger.exception(f"Get message TimeoutError, {te}")
                    raise te
                except asyncio.IncompleteReadError as ir:
                    self.logger.exception(
                        f"""Station {self.station}, Tiempo fuera al no poder
                        leer en readbytes {bufsize} bytes, {ir}""")
                    raise ir
                except socket.timeout as timeout:
                    self.logger.exception(
                        f"La conexión se cerró, socket timeout {timeout}, STATION {self.station}")
                    self.on_blocking()
                    self.logger.exception("Esperando mucho tiempo")
                    self.status = False
                    raise timeout
                except Exception as ex:
                    print("Escepcion as ex: %s" % ex)
                    self.logger.exception(
                        f"La conexión se cerró, error en comunicación {ex}")
                    await self.close(idc)
                    self.on_blocking()
                    info = f"Error {ex} en estación {self.station}. Encabezado con data {data}"
                    self.logger.info(info)
                    self.logger.error(ex)
                    self.status = False
                    raise ex
                return True

            except asyncio.IncompleteReadError as e:
                self.logger.exception(f"Error de mensaje incompleto {e}")
                self.logger.error(
                    f"Error de mensaje esperado en n bytes {e.expected}")
                self.logger.error(f"Error de mensaje recibido {e.partial}")
                raise e

            except socket.timeout:
                await self.close()
                self.sock = self.create_socket(None)
                self.on_blocking()
                raise socket.timeout

            except socket.error as ex:
                await self.close()
                self.logger.error(ex)
                self.sock = self.create_socket(None)
                self.on_blocking()
                raise ex
        else:
            raise Exception(f"No idc {idc} at clients")

    async def get_records(self, idc='', ids=''):
        msg = {}
        while self.msg_bytes:
            # READ THE FIRST TWO BYTES FROM RECORD HEADER
            try:
                record_type, record_length = unpack('>2B', self.msg_bytes[0:2])
            except struct_error as unpack_error:
                self.status = False
                self.logger.exception(f"Error en hacer unpack {unpack_error} (error)")
                raise unpack_error
            except Exception as ex:
                self.status = False
                qex = f"Error {ex} en estación {self.station}, tabla Header"
                self.logger.debug(qex)
                raise ex
            self.msg_bytes = self.msg_bytes[2:]
            try:
                msg_table = self.select_record(record_type, record_length)
                msg.update(msg_table)
            except Exception as ex:
                self.status = False
                self.logger.error(ex)
                self.logger.error("Desconectando debido a error en mensaje")
                self.logger.error(
                    f"Reconectando debido a error en mensaje, luego de desconexión, {ex}")
                self.on_blocking()
                self.logger.error(f"Levantando error a ...Clliente {idc} Station ID: {ids}")
                raise ex
            except asyncio.IncompleteReadError as ir:
                print(
                    f"Error por lectura incomplete al leer {n} bytes en {self.station}")
                self.logger.exception(
                    f"""Station {self.station}, lectura incomplete al leer
                    en readbytes, error: {ir}""")
                raise ir
            except asyncio.TimeoutError as te:
                print(f"Error Timeout al leer {n} bytes en {self.station}")
                self.logger.exception(
                    f"Station {self.station}, Tiempo fuera al leer en readbytes, {te}")
                raise te
            except asyncio.IncompleteReadError as ir:
                print(f"Incomplete read, station {self.station}")
                self.logger.exception(
                    f"Station {self.station}, Tiempo fuera al no poder leer en readbytes {n} bytes, {ir}")
                raise ir

        msg["HEADER"] = self.msg_dict
        done = self.checksum
        return done, msg

    def select_record(self, record_type, record_length):
        field_names = gsof_field_names
        rec_input = gsof_rec
        msg = []
        table_name = self.tables.get(record_type)
        timestamp = self.timestamp
        try:
            rec_field_names = field_names.get(record_type)
            if record_type not in [13, 14, 33, 48] and record_type in field_names.keys():
                # print("Base recibida")
                try:
                    rec_values = unpack(
                        rec_input[record_type], self.msg_bytes[:record_length])
                    msg = dict(list(zip(rec_field_names, rec_values)))
                    msg['TIMESTAMP'] = timestamp
                    self.rec_dict.update({table_name: msg})
                    self.msg_bytes = self.msg_bytes[record_length:]
                except struct_error as unpack_error:
                    self.status = False
                    self.logger.exception(f"Error en hacer unpack {unpack_error} (error)")
                    raise unpack_error
                except Exception as ex:
                    self.status = False
                    self.logger.exception(f"Error al hacer unpack {ex}")
                    raise ex

            elif record_type in [13, 14, 33, 48] and record_type in field_names.keys():
                L = len(self.msg_bytes)-1
                bNUM = self.msg_bytes[0:1]
                try:
                    code = rec_input[record_type][0]
                    NUM_OF_SVS = unpack(code, bNUM)  # char-> pass to int
                except struct_error as unpack_error:
                    self.status = False
                    self.logger.exception(f"Error en hacer unpack {unpack_error} (error)")
                    raise unpack_error
                except Exception as ex:
                    self.status = False
                    qex = "Error %s en estación %s, tabla %s" % (
                        ex, self.station, record_type)
                    self.logger.exception(qex)
                    raise ex
                u = int(L/NUM_OF_SVS[0])
                # Acortar el NSVS quitando primer byte
                self.msg_bytes = self.msg_bytes[1:]
                # for field in range(len(rec_field_names)):
                #    self.rec_dict[rec_field_names[field]] = []
                for sat in range(NUM_OF_SVS[0]):
                    try:
                        code = rec_input[record_type][1]
                        rec_values = unpack(
                            code, self.msg_bytes[0:u])  # why [0:10]
                        msg_k = dict(list(zip(rec_field_names, rec_values)))
                        msg_k['TIMESTAMP'] = timestamp
                        msg.append(msg_k)
                    except struct_error as unpack_error:
                        self.status = False
                        self.logger.exception(f"Error en hacer unpack {unpack_error} (error)")
                        raise unpack_error
                    except Exception as ex:
                        self.status = False
                        self.logger.debug(ex)
                        raise ex
                    self.msg_bytes = self.msg_bytes[u:]
                    tname = table_name+"_"+str(sat)
                    self.rec_dict.update({table_name: msg})
            else:
                """Unknown record type? Skip it for now!"""
                # print record_type
                msg = self.msg_bytes[record_length + 2:]
                self.msg_bytes = self.msg_bytes[record_length + 2:]
        except Exception as ex:
            self.status = False
            raise ex
        return {table_name: msg}


