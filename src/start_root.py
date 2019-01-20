from src.Peer import Peer
from src.Stream import Stream

if __name__ == "__main__":
    root_address = ('127.0.0.1', 3434)

    server = Peer(root_address[0],
                  root_address[1],
                  is_root=True)

    server.run()
