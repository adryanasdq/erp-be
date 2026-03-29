from sqlmodel import Session as SessionType


def commit_invoice_transaction(processed_data: dict, session: SessionType):
    try:
        session.add(processed_data["invoice"])
        session.add(processed_data["journal_entry"])

        session.commit()
        session.refresh(processed_data["invoice"])
        return processed_data["invoice"]
    except Exception as e:
        session.rollback()
        raise e
