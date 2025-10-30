from cuid2 import Cuid
from sqlmodel import Sequence, text, Session as SessionType
from datetime import datetime


def generate_cuid() -> str:
    """
    Generate a collision-resistant unique identifier (CUID).
    Returns a string containing lowercase letters and numbers.
    """

    CUID_GENERATOR: Cuid = Cuid(length=10)
    return CUID_GENERATOR.generate()


def generate_custom_id(prefix: str, session: SessionType) -> str:
    """
    Generate a custom ID with a given prefix and table name.
    Returns a string in the format: {prefix}{join_date}{next_sequence_value}
    Example: EMP25010001, DEP24020002, etc.
    """

    seq_name = f"{prefix.lower()}_id_seq"
    session.exec(text(f"CREATE SEQUENCE IF NOT EXISTS {seq_name} START 1"))
    seq = Sequence(seq_name)
    next_val = session.exec(seq)
    join_date = datetime.now().strftime('%y%m')

    return f"{prefix.upper()}{join_date}{str(next_val).zfill(4)}"


    # TODO: Monthly reset sequence, use "main" schema.

    # prefix = table_name[:2].upper()
    # join_date = datetime.now().strftime('%y%m')

    # seq_name = f"{schema_name}.{table_name.lower()}_id_seq"
    # await session.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {seq_name} START 1"))
    
    # seq = Sequence(seq_name)
    # next_val = await session.execute(seq)

    # # The sequence should be restarted every month
    # query = text(f"""
    #     SELECT id FROM {schema_name}.{table_name}
    #     ORDER BY id DESC LIMIT 1
    # """)

    # result = await session.execute(query)
    # last_id = str(result.scalar())

    # if last_id[4:7] != join_date and last_id:
    #     await session.execute(text(f"ALTER SEQUENCE {seq_name} RESTART WITH 1"))
    #     next_val = await session.execute(seq)

    # return f"{prefix}{join_date}{str(next_val).zfill(4)}"