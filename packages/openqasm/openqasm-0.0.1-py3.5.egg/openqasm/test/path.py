import os

from enum import Enum

class Path(Enum):
    """Helper with paths commonly used during the tests."""

    qiskit_path = ["qiskit/"]

    # Main SDK path:    qiskit/
    SDK = qiskit_path[0]
    # test.python path: qiskit/test/python/
    TEST = os.path.normpath(os.path.join(SDK, '..', 'test'))
    # Examples path:    examples/
    EXAMPLES = os.path.normpath(os.path.join(SDK, '..', 'examples'))
    # Schemas path:     qiskit/schemas
    SCHEMAS = os.path.normpath(os.path.join(SDK, 'schemas'))
    # Sample QASMs path: qiskit/test/python/qasm
    QASMS = os.path.normpath(os.path.join(TEST, 'examples'))
