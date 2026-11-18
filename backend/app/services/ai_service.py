"""
AI Service — Generates grounded climate risk advisories, contributor breakdowns, and recommendations.
Integrates with local Qwen 3 when online, and falls back gracefully to a deterministic,
grounded template reasoning engine when the local LLM is offline.
"""
from typing import Any, Dict, List, Optional
import httpx
import logging

from app.services.region_service import region_service
from app.services.analytics_service import analytics_service

logger = logging.getLogger(__name__)

# Standard local Ollama / Qwen endpoint
LOCAL_LLM_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"  # or qwen:latest


class AIService:
    def __init__(self):
        self.region_service = region_service
        self.analytics_service = analytics_service

    async def _probe_local_llm(self) -> bool:
        """Check if local LLM server is accessible quickly without blocking tests/UI."""
        try:
            async with httpx.AsyncClient(timeout=0.25) as client:
                res = await client.get("http://localhost:11434/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    def generate_deterministic_insights(self, region_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate grounded, deterministic, template-based explanation from structured risk data.
        Explicitly labeled as fallback to ensure full academic and technical integrity.
        """
        name = region_data["name"]
        district = region_data["district"]
        state = region_data.get("state", "India")
        elevation = region_data.get("elevation_m", 5.0)
        flood_severity = region_data.get("flood_severity", "none")
        rain = region_data.get("latest_rainfall_mm", 0.0)
        tide = region_data.get("latest_tide_m", 1.0)
        
        risk = region_data.get("latest_risk")
        if isinstance(risk, dict):
            ccri_score = risk.get("final_score") or 0.0
            risk_level = risk.get("risk_level") or "Low"
            comp_scores = risk.get("component_scores") or {}
            eff_weights = risk.get("effective_weights") or {}
        elif risk is not None:
            ccri_score = risk.final_score if risk.final_score is not None else 0.0
            risk_level = risk.risk_level or "Low"
            comp_scores = risk.component_scores or {}
            eff_weights = risk.effective_weights or {}
        else:
            ccri_score = 0.0
            risk_level = "Low"
            comp_scores = {}
            eff_weights = {}

        # Contributor breakdown
        contributors = []
        if rain >= 100.0:
            contributors.append(f"Precipitation: Severe rainfall ({rain} mm) heavily saturates coastal drainage systems.")
        elif rain >= 50.0:
            contributors.append(f"Precipitation: Moderate rainfall ({rain} mm) presents localized runoff pressure.")
        else:
            contributors.append(f"Precipitation: Low rainfall ({rain} mm) currently does not exacerbate pluvial risk.")

        if tide >= 2.5:
            contributors.append(f"Tidal Surge: High spring tide ({tide:.2f} m) poses critical barrier against coastal stormwater discharge.")
        elif tide >= 1.5:
            contributors.append(f"Tidal Surge: Moderate tidal level ({tide:.2f} m) presents standard coastal hydrodynamic resistance.")
        else:
            contributors.append(f"Tidal Surge: Low tide ({tide:.2f} m) facilitates unhindered gravity runoff into the sea.")

        if elevation <= 3.0:
            contributors.append(f"Topography: Critically low elevation ({elevation} m) renders the estuary highly susceptible to inundation.")
        elif elevation <= 7.0:
            contributors.append(f"Topography: Low-to-moderate elevation ({elevation} m) provides limited natural coastal buffer.")
        else:
            contributors.append(f"Topography: Elevated coastal ridge ({elevation} m) provides substantial barrier against marine ingress.")

        contributors.append(f"Historical Hazard: Documented {flood_severity.upper()} flood severity profile increases base vulnerability factor.")

        # Recommendations
        recommendations = []
        if risk_level in ("Critical", "High"):
            recommendations.append("Issue high-alert advisories to municipal drainage and flood management teams.")
            recommendations.append("Pre-position mobile high-capacity dewatering pumps in low-lying sub-districts.")
            recommendations.append("Inspect tidal control sluice gates and reinforce estuarine earthen embankments.")
            recommendations.append("Restrict non-essential marine and waterfront activities during astronomical high tides.")
        elif risk_level == "Moderate":
            recommendations.append("Maintain routine surveillance of coastal storm drains and tidal inlets.")
            recommendations.append("Monitor regional weather radar for sudden convective cloudburst developments.")
            recommendations.append("Audit emergency response stockpiles and communication repeaters.")
        else:
            recommendations.append("Standard operating baseline — continue routine automated telemetry collection.")
            recommendations.append("Schedule preventive desilting of coastal drainage culverts during low tide windows.")

        situation_text = (
            f"{name} ({district}, {state}) is currently evaluated at **{risk_level.upper()} Risk** "
            f"with a Composite Climate Risk Index (CCRI) of **{ccri_score:.1f}/100** under the Phase 5 deterministic methodology. "
            f"The primary risk drivers are the combination of {elevation}m topographic elevation, "
            f"{tide:.2f}m tidal levels, and a {flood_severity} historical flood profile."
        )

        return {
            "region_id": region_data["id"],
            "region_name": name,
            "overall_situation": situation_text,
            "ccri_score": ccri_score,
            "risk_level": risk_level,
            "main_contributors": contributors,
            "recommended_actions": recommendations,
            "data_limitations": [
                "Tide observations are sourced from a development simulation mock, NOT genuine INCOIS real-time telemetry.",
                "Weather measurements reflect Open-Meteo observational baseline seeds.",
                "Methodology is configured for hackathon demonstration and has not received official meteorological agency validation."
            ],
            "model_status": "Fallback Deterministic Reasoning Engine (Local Qwen 3 offline)",
            "is_llm_generated": False,
        }

    async def get_insights(self, region_id: int) -> Dict[str, Any]:
        """Generate structured AI insights for a region."""
        region = self.region_service.get_region(region_id)
        if not region:
            return {
                "error": "Region not found",
                "status": "error"
            }

        # Check local LLM
        has_llm = await self._probe_local_llm()
        deterministic_result = self.generate_deterministic_insights(region.model_dump())

        if not has_llm:
            return deterministic_result

        # If LLM is available, query Qwen
        try:
            prompt = (
                f"You are the Climate Intelligence AI for the Coastal Climate Risk Dashboard. "
                f"Region: {region.name}, CCRI Score: {deterministic_result['ccri_score']}/100 ({deterministic_result['risk_level']}). "
                f"Rainfall: {region.latest_rainfall_mm}mm, Tide: {region.latest_tide_m}m, Elevation: {region.elevation_m}m. "
                f"Provide a brief executive briefing explaining why this region has this risk level and 3 practical recommendations."
            )
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    LOCAL_LLM_URL,
                    json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
                )
                if resp.status_code == 200:
                    llm_text = resp.json().get("response", "")
                    deterministic_result["llm_executive_briefing"] = llm_text
                    deterministic_result["model_status"] = f"Local LLM ({MODEL_NAME})"
                    deterministic_result["is_llm_generated"] = True
        except Exception as e:
            logger.warning("Local LLM invocation failed, using deterministic fallback: %s", e)

        return deterministic_result

    async def answer_question(self, region_id: int, question: str) -> Dict[str, Any]:
        """Answer user questions regarding coastal risk for a selected region."""
        region = self.region_service.get_region(region_id)
        if not region:
            return {"answer": "Region not found.", "status": "error"}

        q_lower = question.lower()
        insights = await self.get_insights(region_id)

        # Grounded intelligent responses
        if "why" in q_lower or "cause" in q_lower or "contributor" in q_lower:
            answer = (
                f"**Why {region.name} is at {insights['risk_level']} Risk ({insights['ccri_score']:.1f} CCRI):**\n\n"
                + "\n".join(f"• {c}" for c in insights["main_contributors"])
                + f"\n\n*Topographic Note:* Mean elevation is {region.elevation_m} meters above sea level."
            )
        elif "action" in q_lower or "recommend" in q_lower or "what should" in q_lower:
            answer = (
                f"**Recommended Precautionary Actions for {region.name}:**\n\n"
                + "\n".join(f"1. {a}" for a in insights["recommended_actions"])
            )
        elif "tide" in q_lower or "ocean" in q_lower:
            answer = (
                f"The current tidal level in {region.name} is **{region.latest_tide_m:.2f} meters** (Mock Provider). "
                f"In coastal backwaters, tidal levels above 1.5m restrict gravity-based stormwater runoff."
            )
        elif "rain" in q_lower or "weather" in q_lower:
            answer = (
                f"The 24-hour precipitation in {region.name} is **{region.latest_rainfall_mm:.1f} mm** (Open-Meteo baseline). "
                f"This contributes directly to the pluvial flood component score."
            )
        elif "elevation" in q_lower or "terrain" in q_lower:
            answer = (
                f"{region.name} has a mean coastal elevation of **{region.elevation_m} meters**. "
                f"Lower elevations exponentially increase storm surge and tidal inundation exposure."
            )
        else:
            answer = (
                f"**Summary for {region.name}:**\n"
                f"{insights['overall_situation']}\n\n"
                f"**Key Actions:**\n" + "\n".join(f"• {a}" for a in insights["recommended_actions"][:2])
            )

        return {
            "region_id": region_id,
            "region_name": region.name,
            "question": question,
            "answer": answer,
            "model_source": insights["model_status"],
            "disclaimer": "AI answers are strictly grounded in structured backend CCRI metrics and do not replace official disaster management orders."
        }


ai_service = AIService()
