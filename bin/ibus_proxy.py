#!/usr/bin/env python
"""
Usage:
  script.py <inHost> <inPort> <outHost> <outPort> 

"""

from docopt import docopt
import asyncio
from datetime import datetime

class IBUSProxy:
  def __init__(self,inHost,inPort,outHost,outPort):
    self.inHost = inHost
    self.outHost = outHost
    self.inPort = inPort
    self.outPort = outPort
    self.source = None
    self.sinks = []
    
  async def source_server(self,reader,writer):
    if self.source:
      writer.write(b"Duplicated source socket connection is not allowed.\n")
      writer.close()
      return
    self.source = writer
    self.print_info()
    while True:
      data = await reader.read(4096)  # Max number of bytes to read
      if not data:
        break
      for curWriter in self.sinks:
        curWriter.write(data)
      if len(self.sinks)>0:
        try:
          await asyncio.wait([writer.drain() for writer in self.sinks])  # Flow control, see later
        except:
          pass
    writer.close()
    self.source = None
    self.print_info()

  async def sink_server(self,reader, writer):
    self.sinks.append(writer)
    self.print_info()
    try:
      while True:
          data = await reader.read(1)  # Max number of bytes to read
          if not data:
            break
    except:
      pass
    self.sinks.remove(writer)
    self.print_info()
    writer.close()

  async def start_servers(self):
    [task,done] = await asyncio.wait([asyncio.start_server(self.source_server, self.inHost, self.inPort),
                                    asyncio.start_server(self.sink_server, self.outHost, self.outPort)
                                    ])
    [sourceServer,sinkServer] = [t.result() for t in task]
    await asyncio.wait([sourceServer.serve_forever(),
                        sinkServer.serve_forever()
                        ])

  def print_info(self):
    addrPortList = [writer.get_extra_info("socket").getpeername() for writer in self.sinks]
    addrStrings = ["  * {}:{}".format(ip,port) for ip,port in addrPortList]
    print(
      "vvvvvvvvvv{}vvvvvvvvvv\n" \
      "Current source: {}\n" \
      "Current clients: {}\n" \
      "{}\n" \
      "^^^^^^^^^^{}^^^^^^^^^^\n" \
         .format( datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  self.source.get_extra_info("socket").getpeername()[0] if self.source else "None",
                  len(self.sinks),
                  "\n".join(addrStrings),
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                  )
    )

async def main(inHost,inPort,outHost,outPort):
  ibusProxy = IBUSProxy(inHost,inPort,outHost,outPort)
  await ibusProxy.start_servers()

if __name__ == "__main__":
  options = docopt(__doc__)
  asyncio.run(main(options["<inHost>"],options["<inPort>"],
                   options["<outHost>"],options["<outPort>"]
                   )
              )
