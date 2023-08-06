class PassphraseError(Exception):
    def __str__(self):
        return "Wrong passphrase"


class WalletExists(Exception):
    def __str__(self):
        return "Wallet exists"
