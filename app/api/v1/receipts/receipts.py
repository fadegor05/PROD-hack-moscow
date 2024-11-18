from fastapi import APIRouter

from app.integrations.parser import parser
from app.schemas.receipt_schema import IReceiptRead, IQRCodePost

receipts_router = APIRouter(prefix="/receipts", tags=["Receipt"])


@receipts_router.post(
    "",
    summary="Обработать QR-код чека",
    description="Принимает данные QR-кода чека и возвращает структурированную информацию о покупке",
)
async def post_receipts(qr_data: IQRCodePost) -> IReceiptRead:
    return await parser.parse_receipt(qr_data.qr_raw)
