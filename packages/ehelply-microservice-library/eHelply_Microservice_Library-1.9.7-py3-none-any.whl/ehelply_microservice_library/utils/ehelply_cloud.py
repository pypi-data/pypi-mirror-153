import traceback
import json
import base64
import time
from typing import Union, Optional, List, Any
from enum import Enum

import sentry_sdk
from sentry_sdk.tracing import Span
from fastapi import HTTPException
from pydantic import BaseModel, PrivateAttr

from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.drivers.aws_utils.aws_dynamo import Dynamo, Attribute
from ehelply_bootstrapper.utils.cryptography import Hashing

from ehelply_microservice_library.integrations.m2m import M2M

default_secondary: str = "s"


class AuthException(Exception):
    pass


class CloudParticipantAuthRequest(BaseModel):
    x_access_token: Optional[str] = None
    x_secret_token: Optional[str] = None
    authorization: Optional[str] = None
    ehelply_active_participant: Optional[str] = None
    ehelply_project: Optional[str] = None
    ehelply_data: Optional[str] = None


class CloudParticipantRequest(BaseModel):
    auth: CloudParticipantAuthRequest
    scopes: List[str]
    allow_project_statuses: List[str] = ["enabled"]
    limit: Optional[str] = None
    ignore_project_enabled: bool = False
    ignore_spend_limits: bool = False
    exception_if_unauthorized: bool = True
    exception_if_spend_maxed: bool = True
    exception_if_project_not_enabled: bool = True
    skip_project_check: bool = False


class CloudParticipantAuthResponse(BaseModel):
    authorization: Optional[str] = None
    access_token: Optional[str] = None
    secret_token: Optional[str] = None
    claims: Optional[dict] = None
    data: Optional[dict] = None


class CloudParticipantResponse(BaseModel):
    auth: CloudParticipantAuthResponse
    active_participant: str
    project_uuid: str
    role: str
    scopes: List[str]
    is_privileged: bool = False
    is_m2m: bool = False
    entity_identifier: Optional[str] = None
    limit: Optional[float] = None


class CloudParticipant(BaseModel):
    active_participant: str
    project_uuid: str
    is_privileged: bool = False
    entity_identifier: Optional[str] = None


class DynamoModel(BaseModel):
    __last_update: dict = PrivateAttr()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.__last_update: dict = self.dict()

    def get_pkey_names(self) -> List[str]:
        raise Exception("Requires implementation")

    def get_pkey_values(self) -> List[Any]:
        raise Exception("Requires implementation")

    def to_dynamo_dict(self) -> dict:
        raise Exception("Requires implementation")

    @staticmethod
    def dict_to_model(data: dict) -> 'DynamoModel':
        raise Exception("Requires implementation")

    def get_changed(self) -> List[Attribute]:
        attributes: List[Attribute] = []
        current: dict = self.dict()
        for key, value in current.items():
            if self.__last_update[key] != value:
                attributes.append(Attribute(
                    key=key,
                    value=value
                ))
        self.__last_update = current
        return attributes


class ProjectDB(DynamoModel):
    """
    Used for DB row entry
    """
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    project_status: str
    archived_at: Optional[str] = None

    def get_pkey_names(self) -> List[str]:
        return [
            "primary",
            "secondary"
        ]

    def get_pkey_values(self) -> List[Any]:
        return [
            self.uuid,
            default_secondary
        ]

    def to_dynamo_dict(self) -> dict:
        the_dict: dict = self.dict()
        the_dict["primary"] = self.uuid
        the_dict["secondary"] = default_secondary
        del the_dict["uuid"]
        return the_dict

    @staticmethod
    def dict_to_model(data: dict) -> 'ProjectDB':
        return ProjectDB(**data, uuid=data['primary'])

    def create(self):
        AuthDynamos.projects.create_item(self.get_pkey_values(), self.to_dynamo_dict())

    @staticmethod
    def get(uuid: str) -> 'ProjectDB':
        return ProjectDB.dict_to_model(
            AuthDynamos.projects.get_item([
                uuid,
                default_secondary
            ])
        )

    @staticmethod
    def delete(uuid: str):
        AuthDynamos.projects.delete_item([
            uuid,
            default_secondary
        ])

    def update(self, attributes: Optional[List[Attribute]] = None):
        if attributes is None:
            attributes = self.get_changed()
        AuthDynamos.projects.update_item(self.get_pkey_values(), attributes)

    @staticmethod
    def update_for(uuid: str, attributes: List[Attribute]):
        AuthDynamos.projects.update_item([
            uuid,
            default_secondary
        ], attributes)

    def is_spend_maxed(self) -> bool:
        return self.current_spend >= self.max_spend


class DefaultLimitsDB(DynamoModel):
    """
    Used for DB row entry
    """
    limit_name: str
    value: float

    def get_pkey_names(self) -> List[str]:
        return [
            "primary",
            "secondary"
        ]

    def get_pkey_values(self) -> List[Any]:
        return [
            self.limit_name,
            default_secondary
        ]

    def to_dynamo_dict(self) -> dict:
        the_dict: dict = self.dict()
        the_dict["primary"] = self.limit_name
        the_dict["secondary"] = default_secondary
        del the_dict["limit_name"]
        return the_dict

    @staticmethod
    def dict_to_model(data: dict) -> 'DefaultLimitsDB':
        return DefaultLimitsDB(**data, limit_name=data['primary'])

    def create(self):
        AuthDynamos.default_limits.create_item(self.get_pkey_values(), self.to_dynamo_dict())

    @staticmethod
    def get(default_limit: str) -> 'DefaultLimitsDB':
        return DefaultLimitsDB.dict_to_model(
            AuthDynamos.default_limits.get_item([
                default_limit,
                default_secondary
            ])
        )

    @staticmethod
    def delete(default_limit: str):
        AuthDynamos.default_limits.delete_item([
            default_limit,
            default_secondary
        ])

    def update(self, attributes: Optional[List[Attribute]] = None):
        if attributes is None:
            attributes = self.get_changed()
        AuthDynamos.default_limits.update_item(self.get_pkey_values(), attributes)

    @staticmethod
    def update_for(default_limit: str, attributes: List[Attribute]):
        AuthDynamos.default_limits.update_item([
            default_limit,
            default_secondary
        ], attributes)


class ProjectMemberRoleEnum(str, Enum):
    owner = 'owner'
    member = 'member'
    key = 'key'


class ProjectMembersDB(DynamoModel):
    """
    Used for DB row entry
    """
    project_uuid: str
    member_uuid: str
    role: ProjectMemberRoleEnum
    scopes: List[str]

    def get_pkey_names(self) -> List[str]:
        return [
            "primary",
            "secondary"
        ]

    def get_pkey_values(self) -> List[Any]:
        return [
            self.project_uuid,
            self.member_uuid
        ]

    def to_dynamo_dict(self) -> dict:
        the_dict: dict = self.dict()
        the_dict["primary"] = self.project_uuid
        the_dict["secondary"] = self.member_uuid
        del the_dict["project_uuid"]
        del the_dict["member_uuid"]
        return the_dict

    @staticmethod
    def dict_to_model(data: dict) -> 'ProjectMembersDB':
        return ProjectMembersDB(**data, project_uuid=data['primary'], member_uuid=data['secondary'])

    def create(self):
        AuthDynamos.project_members.create_item(self.get_pkey_values(), self.to_dynamo_dict())

    @staticmethod
    def get(project_uuid: str, member_uuid: str) -> 'ProjectMembersDB':
        return ProjectMembersDB.dict_to_model(
            AuthDynamos.project_members.get_item([
                project_uuid,
                member_uuid
            ])
        )

    @staticmethod
    def delete(project_uuid: str, member_uuid: str):
        AuthDynamos.project_members.delete_item([
            project_uuid,
            member_uuid
        ])

    def update(self, attributes: Optional[List[Attribute]] = None):
        if attributes is None:
            attributes = self.get_changed()
        AuthDynamos.project_members.update_item(self.get_pkey_values(), attributes)

    @staticmethod
    def update_for(project_uuid: str, member_uuid: str, attributes: List[Attribute]):
        AuthDynamos.project_members.update_item([
            project_uuid,
            member_uuid
        ], attributes)


class ProjectLimitsDB(DynamoModel):
    """
    Used for DB row entry
    """
    project_uuid: str
    limit_name: str
    value: float

    def get_pkey_names(self) -> List[str]:
        return [
            "primary",
            "secondary"
        ]

    def get_pkey_values(self) -> List[Any]:
        return [
            self.project_uuid,
            self.limit_name
        ]

    def to_dynamo_dict(self) -> dict:
        the_dict: dict = self.dict()
        the_dict["primary"] = self.project_uuid
        the_dict["secondary"] = self.limit_name
        del the_dict["project_uuid"]
        del the_dict["limit_name"]
        return the_dict

    @staticmethod
    def dict_to_model(data: dict) -> 'ProjectLimitsDB':
        return ProjectLimitsDB(**data, project_uuid=data['primary'], limit_name=data['secondary'])

    def create(self):
        AuthDynamos.project_limits.create_item(self.get_pkey_values(), self.to_dynamo_dict())

    @staticmethod
    def get(project_uuid: str, limit_name: str) -> 'ProjectLimitsDB':
        return ProjectLimitsDB.dict_to_model(
            AuthDynamos.project_limits.get_item([
                project_uuid,
                limit_name
            ])
        )

    @staticmethod
    def delete(project_uuid: str, limit_name: str):
        AuthDynamos.project_limits.delete_item([
            project_uuid,
            limit_name
        ])

    def update(self, attributes: Optional[List[Attribute]] = None):
        if attributes is None:
            attributes = self.get_changed()
        AuthDynamos.project_limits.update_item(self.get_pkey_values(), attributes)

    @staticmethod
    def update_for(project_uuid: str, limit_name: str, attributes: List[Attribute]):
        AuthDynamos.project_limits.update_item([
            project_uuid,
            limit_name
        ], attributes)


class StackAdministratorsDB(DynamoModel):
    """
    Used for DB row entry
    """
    member_uuid: str
    scopes: List[str]

    def get_pkey_names(self) -> List[str]:
        return [
            "primary",
            "secondary"
        ]

    def get_pkey_values(self) -> List[Any]:
        return [
            self.member_uuid,
            default_secondary
        ]

    def to_dynamo_dict(self) -> dict:
        the_dict: dict = self.dict()
        the_dict["primary"] = self.member_uuid
        the_dict["secondary"] = default_secondary
        del the_dict["member_uuid"]
        return the_dict

    @staticmethod
    def dict_to_model(data: dict) -> 'StackAdministratorsDB':
        return StackAdministratorsDB(**data, member_uuid=data['primary'])

    def create(self):
        AuthDynamos.stack_administrators.create_item(self.get_pkey_values(), self.to_dynamo_dict())

    @staticmethod
    def get(member_uuid: str) -> 'StackAdministratorsDB':
        return StackAdministratorsDB.dict_to_model(
            AuthDynamos.stack_administrators.get_item([
                member_uuid,
                default_secondary
            ])
        )

    @staticmethod
    def delete(member_uuid: str):
        AuthDynamos.stack_administrators.delete_item([
            member_uuid,
            default_secondary
        ])

    def update(self, attributes: Optional[List[Attribute]] = None):
        if attributes is None:
            attributes = self.get_changed()
        AuthDynamos.stack_administrators.update_item(self.get_pkey_values(), attributes)

    @staticmethod
    def update_for(member_uuid: str, attributes: List[Attribute]):
        AuthDynamos.stack_administrators.update_item([
            member_uuid,
            default_secondary
        ], attributes)


class KeysDB(DynamoModel):
    """
    Used for DB row entry
    """
    access_token: str
    secret_token: str

    def get_pkey_names(self) -> List[str]:
        return [
            "primary",
            "secondary"
        ]

    def get_pkey_values(self) -> List[Any]:
        return [
            self.access_token,
            default_secondary
        ]

    def to_dynamo_dict(self) -> dict:
        the_dict: dict = self.dict()
        the_dict["primary"] = self.access_token
        the_dict["secondary"] = default_secondary
        del the_dict["access_token"]
        return the_dict

    @staticmethod
    def dict_to_model(data: dict) -> 'KeysDB':
        return KeysDB(**data, access_token=data['primary'])

    def create(self):
        AuthDynamos.keys.create_item(self.get_pkey_values(), self.to_dynamo_dict())

    @staticmethod
    def get(access_token: str) -> 'KeysDB':
        return KeysDB.dict_to_model(
            AuthDynamos.keys.get_item([
                access_token,
                default_secondary
            ])
        )

    @staticmethod
    def delete(access_token: str):
        AuthDynamos.keys.delete_item([
            access_token,
            default_secondary
        ])

    def update(self, attributes: Optional[List[Attribute]] = None):
        if attributes is None:
            attributes = self.get_changed()
        AuthDynamos.keys.update_item(self.get_pkey_values(), attributes)

    @staticmethod
    def update_for(access_token: str, attributes: List[Attribute]):
        AuthDynamos.keys.update_item([
            access_token,
            default_secondary
        ], attributes)


class AuthDynamos:
    default_limits: Dynamo
    projects: Dynamo
    project_members: Dynamo
    project_limits: Dynamo
    stack_administrators: Dynamo
    keys: Dynamo
    loaded: bool = False

    @staticmethod
    def make():
        if not AuthDynamos.loaded:
            table_name: str = State.config.app.auth.dynamo_table

            AuthDynamos.default_limits = Dynamo(
                table_name=table_name,
                p_keys=["primary", "secondary"],
                sub_table="default_limits"
            )
            AuthDynamos.projects = Dynamo(
                table_name=table_name,
                p_keys=["primary", "secondary"],
                sub_table="projects"
            )
            AuthDynamos.project_members = Dynamo(
                table_name=table_name,
                p_keys=["primary", "secondary"],
                sub_table="project_members"
            )
            AuthDynamos.project_limits = Dynamo(
                table_name=table_name,
                p_keys=["primary", "secondary"],
                sub_table="project_limits"
            )
            AuthDynamos.stack_administrators = Dynamo(
                table_name=table_name,
                p_keys=["primary", "secondary"],
                sub_table="stack_administrators"
            )
            AuthDynamos.keys = Dynamo(
                table_name=table_name,
                p_keys=["primary", "secondary"],
                sub_table="keys"
            )
            AuthDynamos.loaded = True


async def ehelply_cloud_access(
        auth: CloudParticipantAuthRequest,
        scopes: List[str],
        allow_project_statuses: Optional[List[str]] = None,
        limit: Optional[str] = None,
        ignore_project_enabled=False,
        ignore_spend_limits=False,
        exception_if_unauthorized=True,
        exception_if_spend_maxed=True,
        exception_if_project_not_enabled=True,
        skip_project_check=False,
) -> Union[bool, CloudParticipantResponse]:
    """

    Args:
        limit:
        allow_project_statuses:
        auth:
        node:
        service_target:
        ignore_project_enabled:
        ignore_spend_limits:
        exception_if_unauthorized:
        exception_if_spend_maxed:
        exception_if_project_not_enabled:
        skip_project_check:

    Returns:

    """
    cloud_participant_request: CloudParticipantRequest = CloudParticipantRequest(
        auth=auth,
        scopes=scopes,
        allow_project_statuses=allow_project_statuses if allow_project_statuses is not None else ["enabled"],
        limit=limit,
        ignore_project_enabled=ignore_project_enabled,
        ignore_spend_limits=ignore_spend_limits,
        exception_if_unauthorized=exception_if_unauthorized,
        exception_if_spend_maxed=exception_if_spend_maxed,
        exception_if_project_not_enabled=exception_if_project_not_enabled,
        skip_project_check=skip_project_check
    )

    start_time = time.time()
    AuthDynamos.make()
    response: Union[bool, CloudParticipantResponse] = __cloud_participant(cloud_participant_request)
    State.logger.debug("CloudParticipant Auth: --- %s seconds ---" % (time.time() - start_time))
    State.logger.debugg(str(response.dict()))
    return response


def __cloud_participant(cloud_participant_request: CloudParticipantRequest) -> Union[bool, CloudParticipantResponse]:
    with sentry_sdk.start_span(
            op="cp_authentication",
            description="Cloud Participant Authentication"
    ) as sentry_span:
        m2m: M2M = State.integrations.get("m2m")
        ehelply_data_dict, ehelply_entity_identifier, ehelply_active_participant, ehelply_project_uuid, my_auth, is_m2m_key = __cp_authentication(
            cloud_participant_request, m2m, sentry_span
        )

    with sentry_sdk.start_span(
            op="cp_authorization",
            description="Cloud Participant Authorization"
    ) as sentry_span:
        if is_m2m_key:
            response: CloudParticipantResponse = CloudParticipantResponse(
                auth=my_auth,
                is_privileged=True,
                is_m2m_key=True,
                active_participant=ehelply_active_participant,
                project_uuid=ehelply_project_uuid,
                entity_identifier=ehelply_entity_identifier,
                role="stack_administrator",
                scopes=[],
                limit=None
            )
            sentry_span.set_tag('is_speedy_m2m', True)
            sentry_span.set_data('CloudParticipantResponse', __remove_sensitive_data(response, safe_participant=True))
            return response

        try:
            with sentry_span.start_child(op="cp_authorization", description="Retrieving Project Details"):
                project: ProjectDB = ProjectDB.get(ehelply_project_uuid)
        except:
            raise HTTPException(
                status_code=401,
                detail="Invalid project - Denied by eHelply - CloudParticipant Auth"
            )

        role: str
        scopes: List[str]
        is_privileged: bool = False
        limit: Optional[float] = None

        try:
            with sentry_span.start_child(op="cp_authorization", description="Retrieving Project Member"):
                project_member: ProjectMembersDB = ProjectMembersDB.get(ehelply_project_uuid,
                                                                        ehelply_active_participant)

                for scope in cloud_participant_request.scopes:
                    if scope not in project_member.scopes:
                        raise HTTPException(
                            status_code=401,
                            detail="Unauthorized - Denied by eHelply - CloudParticipant Auth"
                        )

                role = project_member.role
                scopes = project_member.scopes

        except:
            try:
                with sentry_span.start_child(op="cp_authorization", description="Retrieving Stack Administrator"):
                    stack_administrator: StackAdministratorsDB = StackAdministratorsDB.get(ehelply_active_participant)

                    for scope in cloud_participant_request.scopes:
                        if scope not in stack_administrator.scopes:
                            raise HTTPException(
                                status_code=401,
                                detail="Unauthorized - Denied by eHelply - CloudParticipant Auth"
                            )

                    role = "stack_administrator"
                    scopes = stack_administrator.scopes
                    is_privileged = True
            except:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid participant/key - Denied by eHelply - CloudParticipant Auth"
                )

        if cloud_participant_request.limit:
            try:
                with sentry_span.start_child(op="cp_authorization", description="Retrieving Project Limit"):
                    project_limits: ProjectLimitsDB = ProjectLimitsDB.get(ehelply_project_uuid,
                                                                          cloud_participant_request.limit)

                    limit = project_limits.value
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Invalid limit - Error by eHelply - CloudParticipant Auth"
                )

        spend_maxed: bool = False
        project_not_enabled: bool = False

        try:
            if not cloud_participant_request.ignore_project_enabled \
                    and project.project_status not in cloud_participant_request.allow_project_statuses:
                project_not_enabled = True
                raise AuthException("Project is not enabled")

            if not cloud_participant_request.ignore_spend_limits and project.is_spend_maxed():
                spend_maxed = True
                raise AuthException("Spend is maxed")

            response: CloudParticipantResponse = CloudParticipantResponse(
                auth=my_auth,
                is_privileged=is_privileged,
                active_participant=ehelply_active_participant,
                project_uuid=ehelply_project_uuid,
                entity_identifier=ehelply_entity_identifier,
                role=role,
                scopes=scopes,
                limit=limit
            )
            sentry_span.set_tag('is_speedy_m2m', False)
            sentry_span.set_data('CloudParticipantResponse', __remove_sensitive_data(response))
            return response
        except (AuthException, HTTPException):
            pass
        except Exception as e:
            traceback.print_exc()
            State.logger.warning(message="Project checks caused an unexpected error.")
            raise HTTPException(
                status_code=500,
                detail="Ruh Roh, something has gone terribly wrong - Error by eHelply - CloudParticipant Auth"
            )

        if spend_maxed and cloud_participant_request.exception_if_spend_maxed:
            raise HTTPException(
                status_code=400,
                detail="Project spend is maxed - Denied by eHelply - CloudParticipant Auth. Increase max spend to complete this request."
            )
        elif spend_maxed:
            return False

        if project_not_enabled and cloud_participant_request.exception_if_project_not_enabled:
            raise HTTPException(
                status_code=400,
                detail="Project is not enabled - Denied by eHelply - CloudParticipant Auth. The project may be awaiting approval or disabled."
            )
        elif project_not_enabled:
            return False

        if cloud_participant_request.exception_if_unauthorized:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized - Denied by eHelply - CloudParticipant Auth"
            )
        else:
            return False


def __cp_authentication(cloud_participant_request: CloudParticipantRequest, m2m: M2M, sentry_span: Span):
    ehelply_active_participant: Optional[str] = None

    with sentry_span.start_child(op="cp_authentication", description="Parsing eHelply Data Header"):
        ehelply_data_dict, ehelply_entity_identifier = __parse_ehelply_data(cloud_participant_request)

    my_auth = CloudParticipantAuthResponse(
        data=ehelply_data_dict
    )

    if cloud_participant_request.auth.authorization:
        with sentry_span.start_child(op="cp_authentication", description="Authorization Token Authentication"):
            ehelply_active_participant = __authentication_by_authorization_token(
                cloud_participant_request,
                m2m,
                my_auth
            )

    is_m2m_key: bool = False

    if cloud_participant_request.auth.x_secret_token and cloud_participant_request.auth.x_access_token:
        with sentry_span.start_child(op="cp_authentication", description="Key (Access/Secret) Authentication"):
            ehelply_active_participant, is_m2m_key = __authentication_by_key(
                cloud_participant_request,
                my_auth,
                m2m
            )

    ehelply_project_uuid = cloud_participant_request.auth.ehelply_project

    if not ehelply_active_participant:
        raise HTTPException(
            status_code=401,
            detail="Missing participant - Denied by eHelply - CloudParticipant Auth"
        )

    if not ehelply_project_uuid:
        raise HTTPException(
            status_code=401,
            detail="Missing project - Denied by eHelply - CloudParticipant Auth"
        )

    return ehelply_data_dict, ehelply_entity_identifier, ehelply_active_participant, ehelply_project_uuid, my_auth, is_m2m_key


def __authentication_by_key(
        cloud_participant_request: CloudParticipantRequest,
        my_auth: CloudParticipantAuthResponse,
        m2m: M2M
) -> str:
    my_auth.access_token = cloud_participant_request.auth.x_access_token
    my_auth.secret_token = cloud_participant_request.auth.x_secret_token

    try:
        is_m2m_key: bool = False
        is_valid_key: bool = m2m.speedy_m2m_auth(
            cloud_participant_request.auth.x_access_token,
            cloud_participant_request.auth.x_secret_token
        )
        if not is_valid_key:
            is_valid_key = __verify_key(
                access=cloud_participant_request.auth.x_access_token,
                secret=cloud_participant_request.auth.x_secret_token
            )
        else:
            is_m2m_key = True
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid key - Denied by eHelply - CloudParticipant Auth"
        )

    if not is_valid_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid key - Denied by eHelply - CloudParticipant Auth"
        )

    ehelply_active_participant = my_auth.access_token

    return ehelply_active_participant, is_m2m_key


def __authentication_by_authorization_token(
        cloud_participant_request: CloudParticipantRequest,
        m2m: M2M,
        my_auth: CloudParticipantAuthResponse
) -> str:
    ehelply_active_participant: Optional[str] = None
    try:
        claims = m2m.verify_token(token=cloud_participant_request.auth.authorization)
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token - Denied by eHelply - CloudParticipant Auth"
        )
    my_auth.authorization = cloud_participant_request.auth.authorization
    if cloud_participant_request.auth.ehelply_active_participant:
        if cloud_participant_request.auth.ehelply_active_participant in claims["custom:participants"].split(","):
            ehelply_active_participant = cloud_participant_request.auth.ehelply_active_participant
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid participant - Denied by eHelply - CloudParticipant Auth"
            )
    my_auth.claims = claims
    return ehelply_active_participant


def __parse_ehelply_data(
        cloud_participant_request: CloudParticipantRequest
) -> (dict, str):
    ehelply_data_dict: Optional[dict] = None
    ehelply_entity_identifier: Optional[str] = None

    if cloud_participant_request.auth.ehelply_data:
        try:
            ehelply_data_b64_bytes = cloud_participant_request.auth.ehelply_data.encode("utf-8")
            ehelply_data_bytes = base64.b64decode(ehelply_data_b64_bytes)
            ehelply_data_dict = json.loads(ehelply_data_bytes.decode("utf-8"))

            if "entity_identifier" in ehelply_data_dict:
                ehelply_entity_identifier = ehelply_data_dict["entity_identifier"]

        except:
            raise HTTPException(
                status_code=400,
                detail="Invalid data - Denied by eHelply - CloudParticipant Auth"
            )
    return ehelply_data_dict, ehelply_entity_identifier


def __verify_key(access: str, secret: str) -> bool:
    actual_secret: str = KeysDB.get(access).secret_token

    hasher: Hashing = Hashing()

    if not hasher.check(secret, actual_secret):
        return False

    return True


def __remove_sensitive_data(cloud_participant_response: CloudParticipantResponse, safe_participant: bool = False) -> dict:
    response: dict = cloud_participant_response.dict()
    if response['auth']['secret_token']:
        response['auth']['secret_token'] = "***"

    if response['role'] == 'key' or safe_participant and len(response['active_participant']) > 8:
        response['active_participant'] = f"...{response['active_participant'][-8:]}"

    if response['auth']['access_token'] and len(response['auth']['access_token']) > 8:
        response['auth']['access_token'] = f"...{response['auth']['access_token'][-8:]}"

    return response
