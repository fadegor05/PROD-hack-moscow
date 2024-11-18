from app.crud.base_crud import BaseCRUD
from app.models.invite_model import Invite
from app.schemas.invite_schema import IInviteCreate, IInviteUpdate


class InviteCRUD(BaseCRUD[Invite, IInviteCreate, IInviteUpdate]):
    pass


invite = InviteCRUD(Invite)
