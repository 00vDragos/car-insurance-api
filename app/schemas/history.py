from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel


class HistoryItem(BaseModel):
    type: Literal["POLICY", "CLAIM"]

    # POLICY fields
    policyId: Optional[int] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    provider: Optional[str] = None

    # CLAIM fields
    claimId: Optional[int] = None
    claimDate: Optional[date] = None
    amount: Optional[float] = None
    description: Optional[str] = None

class PolicyHistoryItem(BaseModel):
    type: Literal["POLICY"]
    policyId: int
    startDate: date
    endDate: date
    provider: Optional[str]

class ClaimHistoryItem(BaseModel):
    type: Literal["CLAIM"]
    claimId: int
    claimDate: date
    amount: float
    description: str

# Listă combinată cu evenimente (claim + policy)
CarHistoryResponse = list[PolicyHistoryItem | ClaimHistoryItem]
