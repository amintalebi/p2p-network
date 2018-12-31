from src.Peer import Peer

if __name__ == "__main__":
    server = Peer("127.0.0.1", 3434, is_root=True)
    server.run()

    client = Peer("127.0.0.1", 8080, is_root=False,
                  root_address=("127.0.0.1", 3434))
