#!/usr/bin/env python
import asyncio

sources = []
sinks = []

async def echo_server(reader, writer):
  if len(clients)==0:
    await input_server(reader, writer)
  else:
    await output_server(reader, writer)

async def input_server(reader, writer):
  peerAddr = writer.get_extra_info("socket").getpeername()[0]
  print("Adding {}".format(peerAddr))
  print("# Current client number: {}".format(len(clients)))
  clients.append(writer)
  while True:
    data = await reader.read(100)  # Max number of bytes to read
    if not data:
      break
    for curWriter in clients:
      if writer == curWriter:
        continue
      curWriter.write("{}\t{}".format(peerAddr,data.decode().replace('\t','\t\t')) \
                              .encode()
                      )
    await asyncio.wait([writer.drain() for writer in clients])  # Flow control, see later
  clients.remove(writer)
  print("Removed {}".format(peerAddr))
  print("# Current client number: {}".format(len(clients)))
  writer.close()

async def output_server(reader, writer):
  peerAddr = writer.get_extra_info("socket").getpeername()[0]
  print("Adding {}".format(peerAddr))
  print("# Current client number: {}".format(len(clients)))
  clients.append(writer)
  while True:
    data = await reader.read(100)  # Max number of bytes to read
    if not data:
      break
  clients.remove(writer)
  print("Removed {}".format(peerAddr))
  print("# Current client number: {}".format(len(clients)))
  writer.close()

async def main(host, portIn):
  server = await asyncio.start_server(input_server, host, portIn)
  server = await asyncio.start_server(output_server, host, portIn)
  await server.serve_forever()

asyncio.run(main('127.0.0.1', 5000))
