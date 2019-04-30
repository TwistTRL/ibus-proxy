#!/usr/bin/env python
import asyncio

sources = []
sinks = []

async def source_server(reader, writer):
  peerAddr = writer.get_extra_info("socket").getpeername()[0]
  print("Adding {}".format(peerAddr))
  print("# Current source number: {}".format(len(sources)))
  sources.append(writer)
  while True:
    data = await reader.read(100)  # Max number of bytes to read
    if not data:
      break
    for curWriter in sinks:
      if writer == curWriter:
        continue
      curWriter.write("{}\t{}".format(peerAddr,data.decode().replace('\t','\t\t')) \
                              .encode()
                      )
    await asyncio.wait([writer.drain() for writer in sources])  # Flow control, see later
  sources.remove(writer)
  print("Removed {}".format(peerAddr))
  print("# Current client number: {}".format(len(sources)))
  writer.close()

async def sink_server(reader, writer):
  peerAddr = writer.get_extra_info("socket").getpeername()[0]
  print("Adding {}".format(peerAddr))
  print("# Current client number: {}".format(len(sinks)))
  sinks.append(writer)
  while True:
    data = await reader.read(100)  # Max number of bytes to read
    if not data:
      break
  sinks.remove(writer)
  print("Removed {}".format(peerAddr))
  print("# Current client number: {}".format(len(sinks)))
  writer.close()

async def main(host, portIn, portOut):
  server1 = await asyncio.start_server(source_server, host, portIn)
  server2 = await asyncio.start_server(sink_server, host, portOut)
  await asyncio.wait([server1.serve_forever(),server2.serve_forever()])

asyncio.run(main('0.0.0.0',9001,9000))
