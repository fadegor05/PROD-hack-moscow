import json
from typing import Dict, Any
import aiohttp
from app.core.config import ParserSettings

settings = ParserSettings()


class ReceiptParser:
    def __init__(self, token: str):
        self.token = token
        self.api_url = "https://proverkacheka.com/api/v1/check/get"

    async def parse_receipt(self, qr_raw: str) -> Dict[str, Any]:
        """Parse receipt data from QR code string"""
        data = {"token": self.token, "qrraw": qr_raw}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, data=data) as response:
                receipt_data = await response.json()
                return self._extract_receipt_info(receipt_data)

    def _extract_receipt_info(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant information from receipt data"""
        receipt = receipt_data["data"]["json"]
        return {
            "store": receipt["user"],
            "items": [self._format_item(item) for item in receipt["items"]],
            "total": receipt["totalSum"] / 100,
        }

    def _format_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Format individual item data"""
        return {
            "name": item["name"],
            "price": item["price"] / 100,
            "quantity": item["quantity"],
        }


parser = ReceiptParser(token=settings.proverkacheka_token)
