class LibraryError(Exception):
    pass

class BookYetAlreadyError(LibraryError):
    pass

class BookNotFoundError(LibraryError):
    pass

class BookNotAvailableError(LibraryError):
    pass

class ReaderAlreadyExistsError(LibraryError):
    pass