import exceptions
from bson import ObjectId

from blinker import signal
from .Status import Status
post_event = signal('post-event')


class Post:
    def __init__(self, id, user_id, status, direction, depart_time, max_member, content, users):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.direction = direction
        self.depart_time = depart_time
        self.max_member = max_member
        self.content = content
        self.users = users

    @staticmethod
    def create(user_id, direction, depart_time, max_member, content):
        post = Post(id=str(ObjectId()),
                    user_id=user_id,
                    status=Status.RECRUITING,
                    direction=direction,
                    depart_time=depart_time,
                    max_member=max_member,
                    content=content,
                    users=[user_id])

        return post

    def _check_permission(self, user_id):
        if self.user_id != user_id:
            raise exceptions.AccessDenied

    def _check_modifiable(self):
        if self.status not in ['recruiting', 'closed']:
            raise exceptions.CantModify

    def modify_content(self, user_id, patch_dict: dict):
        #self._check_permission(user_id)
        #self._check_modifiable()

        for key, value in patch_dict.items():
            self.__setattr__(key, value)

    def set_status(self, user_id, status):
        self._check_permission(user_id)
        self._validate_change_status(status)

        self.status = status

        if status == 'ordered':
            post_event.send('ordered', users=self.users, post_id=self.id)

        elif status == 'delivered':
            post_event.send('delivered', users=self.users, place=self.place, post_id=self.id)

    def update_fee(self, user_id, fee):
        self._check_permission(user_id)
        self.fee = fee

    def _validate_change_status(self, status):
        if status not in ['recruiting', 'closed', 'ordered', 'delivered']:
            raise exceptions.NotValidStatus

        if self.status == 'recruiting':
            if status != 'closed':
                raise exceptions.NotValidStatus

        elif self.status == 'closed':
            if status not in ['recruiting', 'ordered']:
                raise exceptions.NotValidStatus

        elif self.status == 'ordered':
            if status != 'delivered':
                raise exceptions.NotValidStatus

        elif self.status == 'delivered':
            raise exceptions.NotValidStatus

    def join(self, user_id, nickname, order_json):
        if self.status != 'recruiting':
            raise exceptions.NotRecruiting

        if len(self.users) >= self.max_member:
            raise exceptions.MaxMember

        if user_id in self.users:
            raise exceptions.AlreadyJoinedUser

        self.users.append(user_id)
        post_event.send('joined',
                        owner_user_id=self.user_id,
                        current_member=len(self.users),
                        store_id=self.store_id,
                        post_id=self._id,
                        user_id=user_id,
                        nickname=nickname,
                        order_json=order_json)

    def quit(self, user_id):
        if self.status != 'recruiting':
            raise exceptions.NotRecruiting

        if user_id == self.user_id:
            raise exceptions.OwnerQuit

        if user_id not in self.users:
            raise exceptions.NotJoinedUser

        self.users.remove(user_id)
        post_event.send('quited', post_id=self._id, user_id=user_id)

    def can_delete(self, user_id):
        self._check_permission(user_id)
        self._check_modifiable()
