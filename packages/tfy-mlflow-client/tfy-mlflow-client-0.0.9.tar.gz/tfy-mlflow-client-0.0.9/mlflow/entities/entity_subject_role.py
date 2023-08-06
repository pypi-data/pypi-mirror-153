from mlflow.entities import EntityType, Role, SubjectType
from mlflow.protos.service_pb2 import SubjectRoles as ProtoEntitySubjectRoles


class EntitySubjectRole:
    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        subject_type: str,
        subject_id: str,
        role: int,
    ):
        self._entity_type = EntityType(entity_type)
        self._entity_id = entity_id
        self._subject_type = SubjectType(subject_type)
        self._subject_id = subject_id
        self._role = Role(role)

    @property
    def entity_type(self) -> EntityType:
        return self._entity_type

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def subject_type(self) -> SubjectType:
        return self._subject_type

    @property
    def subject_id(self) -> str:
        return self._subject_id

    @property
    def role(self) -> Role:
        return self._role

    def to_proto(self):
        param = ProtoEntitySubjectRoles()
        param.entity_type = self.entity_type.value
        param.entity_id = self.entity_id
        param.subject_type = self.subject_type.value
        param.subject_id = self.subject_id
        param.role = self.role.name
        return param
