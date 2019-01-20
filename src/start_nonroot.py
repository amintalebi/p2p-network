from src.Peer import Peer
from src.Stream import Stream

root_address = ('127.0.0.1', 3434)

peer_address = ("127.0.0.3", 8000)
peer = Peer(peer_address[0],
            peer_address[1],
            is_root=False,
            root_address=root_address)

peer.run()


