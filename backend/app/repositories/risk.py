import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models.risk import RiskScore
from app.repositories.base import BaseRepository
from app.schemas.risk import RiskEngineResult

logger = logging.getLogger(__name__)


class RiskRepository(BaseRepository[RiskScore]):
    def __init__(self):
        super().__init__(RiskScore)

    async def upsert_score(self, db: AsyncSession, result: RiskEngineResult) -> RiskScore:
        """
        Idempotent upsert of a RiskScore into the database.
        Conflicts on (region_id, timestamp).
        """
        stmt = insert(RiskScore).values(
            region_id=result.region_id,
            timestamp=result.timestamp,
            rainfall_score=result.component_scores.get("rainfall_score"),
            tide_score=result.component_scores.get("tide_score"),
            elevation_score=result.component_scores.get("elevation_score"),
            flood_score=result.component_scores.get("flood_score"),
            final_score=result.final_score,
            risk_level=result.risk_level,
        )

        # On conflict, update the computed values
        stmt = stmt.on_conflict_do_update(
            index_elements=["region_id", "timestamp"],
            set_=dict(
                rainfall_score=stmt.excluded.rainfall_score,
                tide_score=stmt.excluded.tide_score,
                elevation_score=stmt.excluded.elevation_score,
                flood_score=stmt.excluded.flood_score,
                final_score=stmt.excluded.final_score,
                risk_level=stmt.excluded.risk_level,
            )
        )
        
        # Execute and return the updated record
        result_proxy = await db.execute(stmt.returning(RiskScore))
        await db.commit()
        
        score_record = result_proxy.scalar_one()
        return score_record
