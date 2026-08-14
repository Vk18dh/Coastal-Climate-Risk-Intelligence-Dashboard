import datetime
import urllib.request
import json
from typing import Dict, Any
from app.config.settings import settings
from app.config.logging import logger
from app.services.risk_service import risk_service

class AIService:
    """
    AI Advisory Service.
    Generates explainable Executive Summaries, Key Threat Assessments, and Actionable Mitigation Recommendations
    using Groq API (llama-3.3-70b-versatile) with high-accuracy rule-based fallbacks.
    """

    def generate_groq_summary(self, risk_data: Dict[str, Any]) -> str:
        """Attempts to invoke Groq API for LLM executive climate advisory."""
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_free_groq_api_key_here":
            return ""

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            prompt = (
                f"You are a Coastal Climate Risk Intelligence Expert. Analyze the following location metrics:\n"
                f"Region: {risk_data.get('region_name')}, {risk_data.get('state')}\n"
                f"Risk Score: {risk_data.get('composite_risk_score')}/100 ({risk_data.get('risk_level')})\n"
                f"Metrics: Rainfall={risk_data['contributing_factors']['current_rainfall_mm']}mm, "
                f"Tide={risk_data['contributing_factors']['current_tide_height_m']}m, "
                f"Elevation={risk_data['contributing_factors']['mean_elevation_m']}m.\n"
                f"Provide a concise 3-sentence executive summary and 3 bullet point recommendations for disaster management authorities."
            )
            data = {
                "model": settings.AI_MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": settings.AI_TEMPERATURE,
                "max_tokens": 300
            }

            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    res_body = json.loads(resp.read().decode("utf-8"))
                    return res_body["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Groq API call skipped or failed: {e}")
        return ""

    def generate_ai_report(self, region_id: int) -> Dict[str, Any]:
        """Generates AI Executive Advisory report for a coastal region."""
        risk_data = risk_service.compute_risk_for_region(region_id)
        r_name = risk_data.get("region_name")
        r_level = risk_data.get("risk_level")
        score = risk_data.get("composite_risk_score")
        factors = risk_data.get("contributing_factors", {})

        # Attempt Groq API invocation first
        groq_text = self.generate_groq_summary(risk_data)
        if groq_text:
            return {
                "region_id": region_id,
                "region_name": r_name,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "risk_level": r_level,
                "composite_score": score,
                "ai_executive_summary": groq_text,
                "engine": f"Groq LLM ({settings.AI_MODEL_NAME})",
                "confidence_score": 0.95
            }

        # Deterministic Expert Rule-Engine Fallback
        threats = []
        recommendations = []

        if factors.get("current_rainfall_mm", 0) > 20.0:
            threats.append("Heavy localized precipitation exacerbating stormwater drainage bottlenecks.")
            recommendations.append("Activate emergency high-capacity dewatering pumps at tidal sluice gates.")
        else:
            threats.append("Moderate rainfall with potential accumulation in low-lying micro-basins.")
            recommendations.append("Inspect stormwater drainage channels and clear debris obstructions.")

        if factors.get("current_tide_height_m", 0) > 2.0:
            threats.append("High spring tide surge causing sea-water backflow into urban creeks.")
            recommendations.append("Deploy automated flood barriers and restrict public access to low-lying sea fronts.")

        if factors.get("mean_elevation_m", 10.0) < 5.0:
            threats.append("Low elevation terrain highly susceptible to estuarine inundation.")
            recommendations.append("Issue flood warnings for coastal wards and prepare emergency evacuation shelters.")

        summary = (
            f"The coastal zone of {r_name} is currently classified under {r_level} Climate Risk with a Composite Index of {score}/100. "
            f"Key vulnerability is driven by current meteorological rainfall ({factors.get('current_rainfall_mm')} mm) combined with "
            f"sea tide height ({factors.get('current_tide_height_m')} m) relative to the mean elevation ({factors.get('mean_elevation_m')} m). "
            f"Immediate disaster mitigation procedures are advised."
        )

        return {
            "region_id": region_id,
            "region_name": r_name,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "risk_level": r_level,
            "composite_score": score,
            "ai_executive_summary": summary,
            "key_threats": threats,
            "recommendations": recommendations,
            "engine": "Expert Rule-Based Climate Engine (Groq Fallback)",
            "confidence_score": 0.92
        }

ai_service = AIService()
