from src.Peer import Peer


if __name__ == "__main__":
    root_address = ('127.0.0.5', 3534)

    server = Peer(root_address[0],
                  root_address[1],
                  is_root=True)
    print(root_address)
    server.run()


