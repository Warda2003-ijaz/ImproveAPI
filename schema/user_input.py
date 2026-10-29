from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated

class LoanApplicant(BaseModel):
    age: Annotated[int, Field(..., gt=17, lt=100, description="Applicant ki age")]
    monthly_income: Annotated[float, Field(..., gt=0, description="Monthly income PKR mein")]
    loan_amount: Annotated[float, Field(..., gt=0, description="Total loan amount")]
    loan_term_months: Annotated[int, Field(..., gt=0, description="Loan kitne mahine ka hai")]
    existing_loans: Annotated[int, Field(..., ge=0, description="Pehle se kitne loans hain")]
    credit_history: Annotated[Literal['good', 'average', 'none'], Field(..., description="Credit history")]
    employment_type: Annotated[Literal['salaried', 'business', 'self_employed'], Field(..., description="Job type")]

    @computed_field
    @property
    def monthly_installment(self) -> float:
        return self.loan_amount / self.loan_term_months

    @computed_field
    @property
    def debt_to_income(self) -> float:
        return self.monthly_installment / self.monthly_income