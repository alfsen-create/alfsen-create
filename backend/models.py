from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

@dataclass
class Subcontractor:
    name: str
    trade: str
    contact: str
    cost_rate: float
    permissions: str = "view_only"
    jobs: List[tuple] = field(default_factory=list)
    hours_logged: float = 0.0

    def assign_to_job(self, job_id: str, hours: float = 0.0) -> None:
        self.jobs.append((job_id, hours))
        self.hours_logged += hours

    def total_cost(self) -> float:
        return self.cost_rate * self.hours_logged

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "trade": self.trade,
            "contact": self.contact,
            "rate": self.cost_rate,
            "permissions": self.permissions,
            "hours_logged": self.hours_logged,
            "jobs": [
                {"job_id": job_id, "hours": hours} for job_id, hours in self.jobs
            ],
            "total_cost": self.total_cost(),
        }


@dataclass
class MarketingRep:
    name: str
    channel: str
    generated_leads: List[Dict] = field(default_factory=list)
    campaigns: List[Dict] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)

    def submit_lead(self, client_name: str, job_type: str) -> Dict:
        lead = {"client": client_name, "type": job_type, "timestamp": datetime.now()}
        self.generated_leads.append(lead)
        return lead

    def log_campaign(self, name: str, budget: int, reach: int, revenue: int = 0) -> str:
        roi = ((revenue - budget) / budget * 100) if budget > 0 else 0
        if roi < 0:
            self.alerts.append(
                f"\u26A0\uFE0F Campaign '{name}' flagged for negative ROI: {roi:.2f}%"
            )
        self.campaigns.append(
            {
                "name": name,
                "budget": budget,
                "reach": reach,
                "revenue": revenue,
                "roi": roi,
                "date": datetime.now().strftime("%Y-%m"),
            }
        )
        return f"Campaign '{name}' logged."

    def report(self) -> str:
        roi_list = [c["roi"] for c in self.campaigns]
        avg_roi = sum(roi_list) / len(roi_list) if roi_list else 0
        return (
            f"{self.name} - Channel: {self.channel}\n"
            f"Leads Generated: {len(self.generated_leads)} | "
            f"Campaigns: {len(self.campaigns)} | Avg ROI: {avg_roi:.2f}%"
        )

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "channel": self.channel,
            "leads": self.generated_leads,
            "campaigns": self.campaigns,
            "alerts": self.alerts,
        }


@dataclass
class SalesRep:
    name: str
    region: str
    leads: List[Dict] = field(default_factory=list)
    deals: List[Dict] = field(default_factory=list)

    def log_lead(self, client_name: str, job_type: str) -> str:
        self.leads.append({"client": client_name, "type": job_type, "timestamp": datetime.now()})
        return f"Lead logged for {client_name} ({job_type})."

    def close_deal(self, client_name: str, amount: int, job_id: str | None = None) -> str:
        self.deals.append(
            {
                "client": client_name,
                "amount": amount,
                "job_id": job_id,
                "date": datetime.now().strftime("%Y-%m"),
            }
        )
        return f"Deal closed for {client_name} worth ${amount}."

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "region": self.region,
            "leads": self.leads,
            "deals": self.deals,
            "total_revenue": sum(d["amount"] for d in self.deals),
        }
