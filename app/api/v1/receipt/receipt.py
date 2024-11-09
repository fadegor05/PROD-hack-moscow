from fastapi import APIRouter
from app.integrations.parser import parser
from app.schemas.receipt_schema import ReceiptInfo, QRCodeInput

receipt_router = APIRouter(prefix="/receipt", tags=["Receipt"])


@receipt_router.post("", response_model=ReceiptInfo)
async def parse_receipt(qr_data: QRCodeInput) -> ReceiptInfo:
    """Parse receipt data from QR code"""
    return await parser.parse_receipt(qr_data.qr_raw) 