import json
import google.generativeai as genai
from app.core.config import GeminiSettings
from typing import Dict, Any, TypedDict

settings = GeminiSettings()


class Category(TypedDict):
    category: str


class Gemini:
    def __init__(self, api_key: str | None):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model_name="gemini-1.5-flash")
        else:
            self.client = None

    def get_category(self, receipt: Dict[str, Any]) -> Category:
        if not self.client:
            return {"category": "Прочее"}

        prompt = f"""
        Ты - парсер чеков. Тебе дан чек в формате JSON. Тебе нужно проанализировать чек и вернуть его категорию.
        
        Доступные категории:
        - Продукты
        - Кофейня
        - Рестораны
        - Одежда
        - Электроника
        - Развлечения
        - Транспорт
        - Здоровье
        - Дом
        - Прочее
        
        Верни ответ строго в формате JSON:
        {{"category": "название_категории"}}
        
        Вот чек: {receipt}
        """
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=Category,
                ),
            )
            return json.loads(response.text)
        except:
            return {"category": "Прочее"}


gemini_client = Gemini(api_key=settings.gemini_api_key)
