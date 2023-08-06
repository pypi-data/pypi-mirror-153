# Right now there is no proto object defined for this
# If we need to define proto, then add _MLflowObject as
# parent class
class UserInfo:
    def __init__(self, user_id: str, email: str):
        self._user_id = user_id
        self._email = email

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def email(self) -> str:
        return self._email
