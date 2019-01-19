from src.Peer import Peer
from src.Stream import Stream

peer_address = ("127.0.0.2", 8080)
peer = Peer(peer_address[0],
            peer_address[1],
            is_root=False,
            root_address=Stream.ROOT_ADDRESS)

peer.run()
peer.ui.run()

