class PassphraseError(Exception):
    def __str__(self):
        return "Wrong passphrase"
