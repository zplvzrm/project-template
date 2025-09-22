"""Exception"""


class ProjectError(Exception):
    """Etl error"""


class PluginNotFoundError(ProjectError):
    """PluginNotFoundError"""

    def __init__(self, namespace: str, name: str):
        super().__init__()
        self._namespace = namespace
        self._name = name

    def __repr__(self):
        return f'Can not found "{self._name}" plugin in {self._namespace}'

    def __str__(self):
        return self.__repr__()


class InputError(ProjectError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(ProjectError):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
        