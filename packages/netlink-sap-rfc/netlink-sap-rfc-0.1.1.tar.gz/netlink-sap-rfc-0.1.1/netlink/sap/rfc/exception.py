class RfcError(Exception):
    pass


class LogonError(RfcError):
    pass


class CommunicationError(RfcError):
    pass
