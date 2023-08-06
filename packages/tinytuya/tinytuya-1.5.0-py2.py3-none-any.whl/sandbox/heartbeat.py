import tinytuya
import time

# tinytuya.set_debug(True)

d = tinytuya.OutletDevice('047555462cf432a18791', '10.0.1.45', '9b7eeb55d0c7819e')
d.set_version(3.3)
d.set_socketPersistent(True)

print(" > Send Request for Status < ")
payload = d.generate_payload(tinytuya.DP_QUERY)
d.send(payload)

while(True):
    # See if any data is available
    data = d.receive()
    print('Received Payload: %r' % data)

    # Send keyalive heartbeat
    print(" > Send Heartbeat Ping < ")
    payload = d.generate_payload(tinytuya.HEART_BEAT)
    d.send(payload)


