from cuid2 import Cuid
from sqlalchemy import Sequence
from sqlalchemy.orm import Session as SessionType


def generate_cuid() -> str:
    """
    Generate a collision-resistant unique identifier (CUID).
    Returns a string containing lowercase letters and numbers.
    """

    CUID_GENERATOR: Cuid = Cuid(length=10)
    return CUID_GENERATOR.generate()


def generate_custom_id(prefix: str, table_name: str, session: SessionType) -> str:
    """
    Generate a custom ID with a given prefix and table name.
    Returns a string in the format: {prefix}{next_sequence_value}
    Example: EMP0001, DEP0002, etc.
    """

    seq_name = f"{prefix.lower()}_{table_name.lower()[:2]}_id_seq"
    session.execute(f"CREATE SEQUENCE IF NOT EXISTS {seq_name} START 1")
    seq = Sequence(seq_name)
    next_val = session.execute(seq)

    return f"{prefix.lower()}{str(next_val.scalar()).zfill(4)}"