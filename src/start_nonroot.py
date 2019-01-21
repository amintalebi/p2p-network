from src.Peer import Peer

root_address = ('127.0.0.5', 3536)

peer_address = ("127.0.0.4", 8014)
peer = Peer(peer_address[0],
            peer_address[1],
            is_root=False,
            root_address=root_address)

print(peer_address)

peer.run()


