import datetime
from typing import List, Optional

from pydantic import BaseModel

from phiterm.release.release_enums import ReleaseType
from phiterm.release.release_schemas import ReleaseSchema
from phiterm.utils.dttm import current_datetime_utc
from phiterm.utils.log import logger


class WsReleases(BaseModel):
    # This data will grow and should be stored using a sqlite db on the users machine
    releases: List[ReleaseSchema] = []
    last_update_ts: datetime.datetime = current_datetime_utc()

    def add_release(self, rls: ReleaseSchema):
        self.releases.append(rls)
        self.last_update_ts = current_datetime_utc()

    def get_latest_release(self) -> Optional[ReleaseSchema]:
        if len(self.releases) > 0:
            return self.releases[-1]
        return None

    def get_releases_by_type(
        self, rel_type: ReleaseType, active_only: bool = True
    ) -> Optional[List[ReleaseSchema]]:
        """Returns active releases of type rel_type"""
        rls = [rel for rel in self.releases if rel.release_type == rel_type.value]
        if rls:
            if active_only:
                return [r for r in rls if r.is_active]
            return rls
        return None

    def set_active_releases_as_complete(self, rel_type: ReleaseType) -> None:
        """Sets active releases of rel_type as complete"""

        logger.debug(f"Marking existing {rel_type.value} releases as complete")

        active_releases: Optional[List[ReleaseSchema]] = self.get_releases_by_type(
            rel_type
        )
        if active_releases is None or len(active_releases) == 0:
            logger.debug(f"No active {rel_type.value} releases found")
            return

        for rls in active_releases:
            rls.is_active = False
            rls.end_ts = current_datetime_utc()
            # rls.last_update_ts = current_datetime_utc()
            logger.debug(
                f"Release {rls.id_release} ({rls.release_type}) marked as complete"
            )


#
# def secho_releases(ws_releases: WsReleases, last_n_releases: int = 3) -> None:
#
#     pprint_subheading("\nPast Releases")
#     releases_by_type: Dict[
#         str, List[ReleaseSchema]
#     ] = ws_releases.releases_by_type
#     for rel_type, rel_list in releases_by_type.items():
#         pprint_subheading(f"\n{rel_type}:")
#         for i in range(min(len(rel_list), last_n_releases)):
#             rel_list[i].secho_status()
