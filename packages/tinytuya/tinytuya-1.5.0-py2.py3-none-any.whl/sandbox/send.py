import tinytuya

#d = tinytuya.OutletDevice('DEVICEID', 'DEVICEIP', 'DEVICEKEY')
d = tinytuya.OutletDevice('63120466600194c51886', '10.0.1.13', '29619e15c19d077d')
d.set_version(3.3)
d.set_socketPersistent(True)

print(" > Send Turn Off Command <")
payload = d.generate_payload(tinytuya.CONTROL, {'1': False})
d.send(payload)

print(" > Begin Monitor Loop <")
while(True):
    # See if any data is available
    data = d.receive()
    print('Received Payload: %r' % data)

    # Send keyalive heartbeat
    print(" > Send Heartbeat Ping < ")
    payload = d.generate_payload(tinytuya.HEART_BEAT)
    d.send(payload)

    
