class NoDatadomeValuesInHtmlException(Exception):
    pass

class MalformedDatadomeValuesObjectException(Exception):
    pass

class UnknownChallengeTypeException(Exception):
    pass

class UnparasbleJsonDatadomeBodyException(Exception):
    pass

class UnparasbleHtmlDatadomeBodyException(Exception):
    pass

class PermanentlyBlockedException(Exception):
    pass