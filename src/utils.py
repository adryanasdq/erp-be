from cuid2 import Cuid


def generate_cuid() -> str:
    """
    Generate a collision-resistant unique identifier (CUID).
    Returns a string containing lowercase letters and numbers.
    """

    CUID_GENERATOR: Cuid = Cuid(length=10)
    return CUID_GENERATOR.generate()
