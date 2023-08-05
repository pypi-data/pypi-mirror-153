from bc_time.api.objects.base import Base
from bc_time.api.constants.api import Api as ApiConstants

class GroupBase(Base):
    membership_content_type_id = None

    def add_visitor_to_group(self, group_uid: int, visitor_uid: int, add_only: bool=True) -> dict:
        payload = {'link_uid' : visitor_uid}
        if add_only:
            payload['add_only'] = 'add_only'
        return self.api.update(self.membership_content_type_id, group_uid, payload)

    def remove_visitor_from_group(self, group_uid: int, visitor_uid: int, remove_only: bool=True) -> dict:
        payload = {'link_uid' : visitor_uid}
        if remove_only:
            payload['remove_only'] = 'remove_only'
        return self.api.update(self.membership_content_type_id, group_uid, payload)

    def get_all_members_using_pagination(self, group_uid: int, page: int=1, row_count: int=ApiConstants.DEFAULT_ROW_COUNT) -> dict:
        return self.api.get_all_using_pagination(self.membership_content_type_id, content_uid=group_uid, page=page, row_count=row_count)