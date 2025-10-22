class NoDatadomeValuesInHtmlException(Exception):
    pass

class MalformedDatadomeValuesObjectException(Exception):
    pass

class UnknownChallengeTypeException(Exception):
    pass

class UnparsableJsonDatadomeBodyException(Exception):
    pass

class UnparsableHtmlDatadomeBodyException(Exception):
    pass

class PermanentlyBlockedException(Exception):
    pass