# pygame-networking-example
This is a example of a networked client/server based multiplayer example made in Python 3.10.6, using PyGame 2.1.2 for graphics and input.

All of these modules use localhost for networking, the server and client(s) need to be run on the same machine.

The client module waits whenever it calls "Client.recvfrom()", so the module will stop unless server was running when client started
