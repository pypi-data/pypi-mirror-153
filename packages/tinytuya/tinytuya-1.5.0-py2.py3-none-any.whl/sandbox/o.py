import tinytuya

#tinytuya.set_debug(True)

"""
        "name": "Lamp",
            "ip": "10.0.1.48",
            "ver": "3.3",
            "id": "55004706bcddc23d1b11",
            "key": "b62bc9feb9e985da",
"""
d = tinytuya.OutletDevice('55004706bcddc23d1b11', '10.0.1.48', 'b62bc9feb9e985da')
d.set_version(3.3)
d.set_socketPersistent(True)


while(True):
    print(" > Send Request for Status < ")
    payload = d.generate_payload(tinytuya.DP_QUERY)
    d.send(payload)

    # See if any data is available
    data = d.receive()
    print('Received Payload: %r' % data)

    print(" > Send DPS Update Request < ")
    payload = d.generate_payload(tinytuya.UPDATEDPS,['18','19','20'])
    d.send(payload)
    
    # See if any data is available
    data = d.receive()
    print('Received Payload: %r' % data)

