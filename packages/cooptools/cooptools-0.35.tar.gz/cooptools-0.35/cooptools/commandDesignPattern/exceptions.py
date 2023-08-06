
class ResolveStateException(Exception):
    def __init__(self, command, inner: Exception):
        super().__init__()
        print(f"Unable to execute command: {command}"
              f"\n{inner}")

class ResolveBatchException(Exception):
    def __init__(self, batch, inner: Exception):
        super().__init__()
        print(f"Unable to execute batch: {batch}"
              f"\n{inner}")