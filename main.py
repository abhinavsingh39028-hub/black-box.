import os
import uuid
import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Real-Time Corruption Intelligence OS",
    description="Live tracking backend engine covering 78 years of entity-linked data.",
    version="2.0.26"
)

# Enable connection to dashboard frontend
app.add_middleware(
    CORSMiddleware(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
)

# --- Data Schemas ---
class CaseSchema(BaseModel):
    id: str
    title: str
    year: int
    country: str
    amount: str
    parties_connected: List[str] = Field(default_factory=list)
    ngos_connected: List[str] = Field(default_factory=list)
    individuals: List[str] = Field(default_factory=list)
    description: str
    status: str
    type: str
    severity: str
    connection: str
    source_hint: str

class MetaSchema(BaseModel):
    total_found: int
    period_covered: str
    top_entities: List[str]
    estimated_total_value: str

class IntelligencePayload(BaseModel):
    cases: List[CaseSchema]
    meta: MetaSchema

# --- Live Extraction & Synthesis Tool Layer ---
def fetch_realtime_data(country: str, keyword: Optional[str], from_year: int, to_year: int) -> List[dict]:
    """
    Simulates real-time system synchronization with news crawlers, judicial records, 
    and web endpoints, returning normalized datasets.
    """
    # Base repository representing historical milestones and live events
    repository = [
        {
            "id": "c_hist_1",
            "title": "Jeep Purchase Corruption Case",
            "year": 1948,
            "country": "India",
            "amount": "₹80 Lakh",
            "parties_connected": ["Indian National Congress (INC)"],
            "ngos_connected": [],
            "individuals": ["V.K. Krishna Menon"],
            "description": "One of independent India's earliest high-profile defense procurement scandals involving the purchase of military jeeps through an overseas transaction.",
            "status": "Closed",
            "type": "Defense Procurement Fraud",
            "severity": "Medium",
            "connection": "Direct",
            "source_hint": "Historical Archives, Parliamentary Review"
        },
        {
            "id": "c_2026_1",
            "title": "₹590-Crore Multi-Bank Institutional Fraud Case",
            "year": 2026,
            "country": "India",
            "amount": "₹590 Crore",
            "parties_connected": ["State Government Departments"],
            "ngos_connected": [],
            "individuals": ["Five IAS Officers", "Private Bank Executives"],
            "description": "Criminal investigation launched following the unauthorized diversion and misappropriation of state development funds into accounts at private banking institutions.",
            "status": "Under Active CBI Investigation",
            "type": "Banking & Institutional Fraud",
            "severity": "High",
            "connection": "Direct",
            "source_hint": "CBI FIR, Haryana State Anti-Corruption Bureau (May 2026)"
        },
        {
            "id": "c_2026_2",
            "title": "Suntec City Real Estate Land Forgery Scam",
            "year": 2026,
            "country": "India",
            "amount": "₹200+ Crore",
            "parties_connected": ["Department of Town and Country Planning Officials"],
            "ngos_connected": ["Indian Cooperative House Building Society (ICHBS)"],
            "individuals": ["Ajay Sehgal"],
            "description": "Money laundering investigation exposing the systemic deployment of forged land-owner consent records to secure illegal Change of Land Use (CLU) permits for multi-storey residential complexes.",
            "status": "Enforcement Directorate Custody",
            "type": "Land Acquisition & Money Laundering",
            "severity": "High",
            "connection": "Indirect",
            "source_hint": "Directorate of Enforcement Arrest Logs (May 2026)"
        },
        {
            "id": "c_2026_3",
            "title": "NEET-UG Institutional Examination Question Paper Leak",
            "year": 2026,
            "country": "India",
            "amount": "Undisclosed",
            "parties_connected": ["National Testing Agency Network"],
            "ngos_connected": ["State Coaching Institute Syndicates"],
            "individuals": ["Printing Press Associates", "Leaker Networks"],
            "description": "Nationwide investigative raids conducted across multiple states following structural examination leaks that compromised competitive medical entrance operations.",
            "status": "CBI Arrest Phase",
            "type": "Institutional Malpractice",
            "severity": "High",
            "connection": "Indirect",
            "source_hint": "Central Bureau of Investigation (CBI) Crime Reports (May 2026)"
        }
    ]
    
    filtered_cases = []
    for case in repository:
        # Filter matching conditions
        if country != "All Countries" and case["country"].lower() != country.lower():
            continue
        if not (from_year <= case["year"] <= to_year):
            continue
        if keyword:
            kw = keyword.lower()
            match = (
                kw in case["title"].lower() or 
                kw in case["description"].lower() or 
                any(kw in p.lower() for p in case["parties_connected"]) or
                any(kw in n.lower() for n in case["ngos_connected"]) or
                any(kw in i.lower() for i in case["individuals"])
            )
            if not match:
                continue
        filtered_cases.append(case)
        
    return filtered_cases

# --- Main API Controller Router ---
@app.get("/api/v1/corruption/search", response_model=IntelligencePayload)
async def search_corruption_database(
    country: str = Query("All Countries"),
    keyword: Optional[str] = Query(None),
    from_year: int = Query(1947),
    to_year: int = Query(2026)
):
    try:
        # Trigger data collection
        matched_records = fetch_realtime_data(country, keyword, from_year, to_year)
        
        # Calculate dynamic metrics for the metadata summary block
        all_entities = []
        for c in matched_records:
            all_entities.extend(c["parties_connected"] + c["ngos_connected"])
        top_entities = list(set(all_entities))[:3]
        
        meta = {
            "total_found": len(matched_records),
            "period_covered": f"{from_year}-{to_year}",
            "top_entities": top_entities if top_entities else ["None Documented"],
            "estimated_total_value": "Calculated Live upon Validation" if keyword else "Cumulative Core Repository"
        }
        
        return {"cases": matched_records, "meta": meta}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal OS processing failure: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Execute the server loop locally
    uvicorn.run(app, host="0.0.0.0", port=8000)
