import tinytuya

tinytuya.set_debug(True)

d = tinytuya.OutletDevice('eba1a5ca763ca479da7jyp', 'Auto', '02bc2d7593be459b')
d.set_version(3.3)
d.set_dpsUsed({"1": None})
payload=d.generate_payload(tinytuya.CONTROL_NEW, data=None)
data = d._send_receive(payload)
print('Response: %r' % data)

print(" > Fetch Status < ")
data = d.status()
print(data)


