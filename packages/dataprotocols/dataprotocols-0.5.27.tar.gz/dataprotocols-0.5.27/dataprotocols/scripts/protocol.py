from dataprotocols.gsof import Gsof
from dataprotocols.eryo import Eryo
from pathlib import Path
import asyncio
import functools
import os
import signal
import click
import json
import time
from networktools.ip import validURL


PROTOCOL = dict(GSOF=Gsof, ERYO=Eryo)


async def run_test(loop, code, host, port, limit=2000, show=True,
                   protocol=Gsof, data_file='./test.json'):
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    protocol_name = protocol.__class__.__name__
    print("Inicializando %s con:" % (protocol_name))
    [print(k, "->", v) for k, v in ginput.items()]
    file_path = Path(data_file)
    limit_counter = limit
    counter = 0
    print("Conexion a->", ginput)
    instance = protocol(**ginput)
    idc = await instance.connect()
    print("IDC->", idc)
    with open(file_path, "a+") as prt_file:
        prt_file.write("[")
        while counter <= limit_counter:
            try:
                print("Heart beat")
                heartbeat = await instance.heart_beat(idc)
                print("Heartbeat", heartbeat)
                if heartbeat:
                    print("MSG recv>")
                    await instance.get_message_header(idc)
                    done, msg = await instance.get_records()
                    if done:
                        if show:
                            print("%s -> %s" % (protocol_name, code))
                            [print(k, "->", v) for k, v in msg.items()]
                        json.dump(msg, prt_file, indent=2)
                        prt_file.write(",\n")
                else:
                    await instance.close(idc)
                    idc = await instance.connect()
            except Exception as ex:
                prt_file.write("]")
                await instance.close(idc)
                print(f"Error {ex}")
                loop.close()
                raise ex
            except KeyboardInterrupt as ke:
                prt_file.write("]")
                await instance.close(idc)
                loop.close()
                print(ke)
                raise ke
            counter += 1
        prt_file.write("]")
    await instance.close(idc)


@click.command()
@click.option("--code", default="CODE", help="Código de estación (obligatoria)")
@click.option("--host", default="AQUI-VA-LA-URL", help="URL de estación (obligatoria)")
@click.option("--port", default=9080, help="Nro de puerto, defecto 9080")
@click.option("--limit", default=2000, help="Nro de mensajes, defecto 2000")
@click.option("--show/--no-show", default=True, show_default=True,
              type=bool, help="Mostrar cada mensaje")
@click.option("--protocol", default="GSOF", help="Protocolo, defecto GSOF, opciones {GSOF, ERYO}")
@click.option("--data_file", default='./test.json', help="Archivo de almacenamiento de datos, defecto ./test.json")
def run_protocol(code, host, port, limit, show, protocol, data_file):
    loop = asyncio.get_event_loop()
    try:
        if validURL(host):
            prt = PROTOCOL.get(protocol.upper(), Gsof)
            loop.run_until_complete(
                run_test(loop, code, host, port, limit, show, prt, data_file))
        else:
            print("Ingresa datos reales para obtener resultados: protocol --help\nRevisa tus parámetros nuevamente")
    except Exception as ex:
        print("Exception %s" % ex)
        loop.call_soon_threadsafe(loop.stop)
        print(ex)
    except KeyboardInterrupt as ke:
        print("Exception %s" % ke)
        loop.call_soon_threadsafe(loop.stop)
        print(ke)
    finally:
        loop.close()


if __name__ == '__main__':
    run_protocol()
