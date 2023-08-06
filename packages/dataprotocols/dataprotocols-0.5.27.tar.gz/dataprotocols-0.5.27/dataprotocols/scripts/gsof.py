from dataprotocols.gsof import Gsof
import asyncio
import functools
import os
import signal
import click
import json
import time
from networktools.ip import validURL
from networktools.time import gps_time, now
from rich import print
from pyinstrument import Profiler

async def run_test(loop, code, host, port, limit=2000, show=True):
    #with Profiler(async_mode='enabled') as p:
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    print("Inicializando GSOF con:")
    [print(k, "->", v) for k, v in ginput.items()]
    gsof_test = "gsof_test.json"
    limit_counter = limit
    counter = 0
    print("Conexion a->", ginput)
    gsof = Gsof(**ginput)
    print("GSOF object", gsof)
    idc = await gsof.connect()
    print("IDC->", idc)
    with open(gsof_test, "a+") as gsof_file:
        gsof_file.write("[")
        while counter <= limit_counter:
            try:
                heartbeat = await gsof.heart_beat(idc)
                if heartbeat:
                    await gsof.get_message_header(idc)
                    done, msg = await gsof.get_records()
                    if done:
                        if "TIME" in msg:
                            ts_gsof, source = gps_time(msg)
                            ts = now()
                            delta = ts.timestamp() - ts_gsof.timestamp()
                            ts_gsof, source = gps_time(msg)
                            delta = (ts - ts_gsof).total_seconds()
                            msg["DELTA_TIME"] = delta
                            print(f"Delta => {delta}")
                        if show:
                            print("Gsof %s" % code)
                            print(msg)
                        json.dump(msg, gsof_file, indent=2)
                        gsof_file.write(",\n")
                else:
                    await gsof.close(idc)
                    idc = await gsof.connect()
            except Exception as ex:
                gsof_file.write("]")
                await gsof.close(idc)
                print(f"Error {ex}")
                loop.close()
                raise ex
            except KeyboardInterrupt as ke:
                gsof_file.write("]")
                await gsof.close(idc)
                loop.close()
                print(ke)
                raise ke
            counter += 1
        gsof_file.write("]")
    # print("Profiling async")
    # p.print()
    # p.open_in_browser(timeline=True)
    await gsof.close(idc)


@click.command()
@click.option("--code", default="CODE", help="Código de estación")
@click.option("--host", default="AQUI-VA-LA-URL", help="URL de estación")
@click.option("--port", default=9080, help="Nro de puerto")
@click.option("--limit", default=2000, help="Nro de mensajes")
@click.option("--show/--no-show", default=True, show_default=True,
              type=bool, help="Mostrar cada mensaje")
def run_gsof(code, host, port, limit, show):
    loop = asyncio.get_event_loop()
    try:
        if validURL(host):
            loop.run_until_complete(
                run_test(loop, code, host, port, limit, show))
        else:
            print(
                "Ingresa datos reales para obtener resultados: gsof --help \n Revisa tus parámetros nuevamente")
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
    run_gsof()
