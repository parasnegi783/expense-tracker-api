from fastapi import FastAPI, HTTPException, Query
from src.models import Expense, ExpenseCreate, TotalResponse, CategoryTotal
from src.storage import ExpenseStorage

app = FastAPI(title="Smart Expense Tracker API")
storage = ExpenseStorage()


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate):
    return storage.add(expense)


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: str | None = Query(default=None)):
    return storage.list(category=category)


@app.get("/expenses/total", response_model=TotalResponse)
def get_totals():
    result = storage.totals()
    return TotalResponse(
        total=result["total"],
        by_category=[CategoryTotal(**c) for c in result["by_category"]],
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    deleted = storage.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Expense deleted"}
