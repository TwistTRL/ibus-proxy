#!/usr/bin/env python
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
        if writer == curWriter:
          continue
        curWriter.write(data)
      if len(self.sinks)>0:
        await asyncio.wait([writer.drain() for writer in self.sinks])  # Flow control, see later
    writer.close()
    self.source = None
    self.print_info()

  async def sink_server(self,reader, writer):
    self.sinks.append(writer)
    self.print_info()
    while True:
      data = await reader.read(1)  # Max number of bytes to read
      if not data:
        break
    self.sinks.remove(writer)
    self.print_info()
    writer.close()

  async def start_servers(self):
    [sourceServer,sinkServer] = [ await asyncio.start_server(self.source_server, self.inHost, self.inPort),
                                                     await asyncio.start_server(self.sink_server, self.outHost, self.outPort)
    ]
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
  ibusProxy = IBUSProxy('0.0.0.0',9001,'0.0.0.0',9000)
  await ibusProxy.start_servers()

asyncio.run(main('0.0.0.0',9001,'0.0.0.0',9000))
