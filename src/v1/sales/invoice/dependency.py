from sqlmodel import Session as SessionType, select
from src.core.models.sales.invoice import Invoice as DbInvoice
from src.core.schemas.sales.invoice import InvoiceSchema
from src.v1.accounting.journal.dependency import validate_journal_entry
from src.v1.accounting.account.dependency import get_account_by_code
from src.core.schemas.accounting.journal import JournalEntrySchema, JournalLineSchema
from .exception import DuplicateInvoiceNumber, InvoiceNotFound


def get_invoice_by_id(id: str, session: SessionType):
    db_invoice = session.get(DbInvoice, id)
    if not db_invoice:
        raise InvoiceNotFound()
    return db_invoice


def get_all_invoices(session: SessionType, customer_id: str = None, status: str = None):
    """
    Fetch all invoices with optional filtering.
    Logically: Used to see total outstanding AR (account receivables).
    """
    statement = select(DbInvoice)
    if customer_id:
        statement = statement.where(DbInvoice.customer_id == customer_id)
    if status:
        statement = statement.where(DbInvoice.status == status)

    return session.exec(statement).all()


def validate_invoice_processing(data: InvoiceSchema, session: SessionType):
    # 1. Check for duplicate invoice number
    existing = session.exec(
        select(DbInvoice).where(DbInvoice.invoice_number == data.invoice_number)
    ).first()
    if existing:
        raise DuplicateInvoiceNumber()

    # 2. Create Invoice DB Object
    db_invoice = DbInvoice(**data.model_dump())

    # 3. Prepare Revenue Journal Entry
    # Dr Accounts Receivable (1200) | Cr Sales Revenue (4010)
    ar_account = get_account_by_code("1200", session)
    rev_account = get_account_by_code("4010", session)

    journal_data = JournalEntrySchema(
        reference_type="INVOICE",
        reference_id=db_invoice.id,
        description=f"Revenue for Invoice {data.invoice_number}",
        lines=[
            JournalLineSchema(account_id=ar_account.id, debit=data.total_amount),
            JournalLineSchema(account_id=rev_account.id, credit=data.total_amount),
        ],
    )

    db_journal = validate_journal_entry(journal_data, session)

    return {"invoice": db_invoice, "journal_entry": db_journal}
