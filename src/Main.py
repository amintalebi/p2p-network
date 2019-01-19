from src.Peer import Peer

if __name__ == "__main__":
    root_address = ('127.0.0.1', 3434)
    peer1_address = ("127.0.0.1", 8080)

    server = Peer(root_address[0],
                  root_address[1],
                  is_root=True)

    peer1 = Peer(peer1_address[0],
                 peer1_address[1],
                 is_root=False,
                 root_address=root_address)
    server.run()
    peer1.run()
    peer1.ui.run()
