import json
import os
from src.models import Expense, ExpenseCreate

DATA_FILE = os.environ.get("EXPENSE_DATA_FILE", "expenses.json")


class ExpenseStorage:
    def __init__(self, file_path: str = DATA_FILE):
        self.file_path = file_path

    def _read(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write(self, data: list[dict]) -> None:
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _next_id(self, data: list[dict]) -> int:
        if not data:
            return 1
        return max(item["id"] for item in data) + 1

    def add(self, expense: ExpenseCreate) -> Expense:
        data = self._read()
        new_id = self._next_id(data)
        record = expense.model_dump()
        record["id"] = new_id
        record["date"] = str(record["date"])
        data.append(record)
        self._write(data)
        return Expense(**record)

    def list(self, category: str | None = None) -> list[Expense]:
        data = self._read()
        if category:
            data = [e for e in data if e["category"].lower() == category.lower()]
        return [Expense(**e) for e in data]

    def delete(self, expense_id: int) -> bool:
        data = self._read()
        filtered = [e for e in data if e["id"] != expense_id]
        if len(filtered) == len(data):
            return False
        self._write(filtered)
        return True

    def totals(self) -> dict:
        data = self._read()
        overall = round(sum(e["amount"] for e in data), 2)
        categories: dict[str, float] = {}
        for e in data:
            cat = e["category"]
            categories[cat] = round(categories.get(cat, 0) + e["amount"], 2)
        by_category = [{"category": k, "total": v} for k, v in sorted(categories.items())]
        return {"total": overall, "by_category": by_category}

    def clear(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
