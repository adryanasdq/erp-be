from cuid2 import Cuid
from sqlalchemy import Sequence, text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


def generate_cuid() -> str:
    """
    Generate a collision-resistant unique identifier (CUID).
    Returns a string containing lowercase letters and numbers.
    """

    CUID_GENERATOR: Cuid = Cuid(length=10)
    return CUID_GENERATOR.generate()


async def generate_custom_id(prefix: str, session: AsyncSession) -> str:
    """
    Generate a custom ID with a given prefix and table name.
    Returns a string in the format: {prefix}{next_sequence_value}
    Example: EMP0001, DEP0002, etc.
    """

    seq_name = f"{prefix.lower()}_id_seq"
    await session.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {seq_name} START 1"))
    seq = Sequence(seq_name)
    next_val = await session.execute(seq)
    join_date = datetime.now().strftime('%y%m')

    return f"{prefix.upper()}{join_date}{str(next_val).zfill(4)}"