"""
Repository for TideData persistence.
"""
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models.tide import TideData
from app.repositories.base import BaseRepository
from app.schemas.tide import TideDataCreate


class TideRepository(BaseRepository[TideData]):
    def __init__(self):
        super().__init__(TideData)

    async def bulk_upsert(
        self, db: AsyncSession, records: List[TideDataCreate]
    ) -> int:
        """
        Upsert a list of tide records.
        If a record for the same region and timestamp exists, update it.
        """
        if not records:
            return 0
            
        values = [record.model_dump() for record in records]
        
        stmt = insert(self.model).values(values)
        
        # On conflict (region_id, timestamp), update the measurements
        update_dict = {
            c.name: c
            for c in stmt.excluded
            if c.name not in ["id", "region_id", "timestamp"]
        }
        
        stmt = stmt.on_conflict_do_update(
            index_elements=["region_id", "timestamp"],
            set_=update_dict
        )
        
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

tide_repo = TideRepository()
