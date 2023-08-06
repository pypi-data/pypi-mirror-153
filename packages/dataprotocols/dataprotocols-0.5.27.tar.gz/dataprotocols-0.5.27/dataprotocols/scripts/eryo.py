from dataprotocols.eryo import Eryo
import asyncio
import functools
import os
import signal
import json
import time
import click
from networktools.ip import validURL


async def run_test(loop, code, host, port, limit=2000, show=True):
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    print("Inicializando ERYO con:")
    [print(k, "->", v) for k, v in ginput.items()]
    eryo = Eryo(**ginput)
    idc = await eryo.connect()
    eryo_test = "eryo_test.json"
    limit_counter = limit
    counter = 0
    with open(eryo_test, "a+") as eryo_file:
        eryo_file.write("[")
        while counter <= limit_counter:
            try:
                heartbeat = await eryo.heart_beat(idc)
                if heartbeat:
                    await eryo.get_message_header(idc)
                    done, msg = await eryo.get_records()
                    if done:
                        if show:
                            print("Eryo %s" % code)
                            [print(k, "->", v) for k, v in msg.items()]
                        json.dump(msg, eryo_file, indent=2)
                        eryo_file.write(",\n")
                else:
                    await eryo.close(idc)
                    idc = await eryo.connect()
            except Exception as ex:
                eryo_file.write("]")
                print("Error %s" % ex)
                await eryo.close(idc)
                loop.close()
                raise ex
            except KeyboardInterrupt as ke:
                eryo_file.write("]")
                await eryo.close(idc)
                loop.close()
                print(ke)
            counter += 1
        eryo_file.write("]")
    await eryo.close(idc)


@click.command()
@click.option("--code", default="CODE", help="Código de estación")
@click.option("--host", default="AQUI-VA-URL", help="URL de estación")
@click.option("--port", default=8890, help="Nro de puerto")
@click.option("--limit", default=2000, help="Nro de mensajes")
@click.option("--show/--no-show", default=True, show_default=True,
              type=bool, help="Mostrar cada mensaje")
def run_eryo(code, host, port, limit, show):
    loop = asyncio.get_event_loop()
    try:
        if validURL(host):
            loop.run_until_complete(
                run_test(loop, code, host, port, limit, show))
        else:
            print(
                "Igresa datos reales para obtener resultados: eryo --help \n Revisa tus parámetros nuevamente")
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
    run_eryo()
