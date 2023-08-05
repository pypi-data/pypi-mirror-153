from bc_time.api.objects.base import Base
from bc_time.api.constants.api import Api as ApiConstants

class ObjectBase(Base):
    def create(self, payload: dict) -> dict:
        return self.api.create( content_type_id=self.content_type_id, payload=payload)

    def create_many(self, payloads: dict) -> dict:
        return self.api.create(
            content_type_id=self.content_type_id,
            payloads=payloads,
            content_uid=ApiConstants.UID_POST_MANY
        )

    def update(self, content_uid, payload: dict) -> dict:
        return self.api.update(
            content_type_id=self.content_type_id,
            content_uid=content_uid,
            payload=payload
        )

    def update_many(self, payloads: dict) -> dict:
        return self.api.update(
            content_type_id=self.content_type_id,
            content_uid=ApiConstants.UID_POST_MANY,
            payload=payloads
        )

    def get_all_using_pagination(self, filters: dict=None, page: int=1, row_count: int=ApiConstants.DEFAULT_ROW_COUNT) -> dict:
        return self.api.get_all_using_pagination(
            content_type_id=self.content_type_id,
            filters=filters,
            page=page,
            row_count=row_count
        )

    def get_one(self, content_uid: int) -> dict:
        return self.api.get_one(content_type_id=self.content_type_id, content_uid=content_uid)

    def get_many(self, content_uids: list) -> dict:
        return self.api.get_many(content_type_id=self.content_type_id, content_uids=content_uids)