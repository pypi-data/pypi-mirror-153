from enum import Enum
from typing import Callable, List, Dict, Optional, Any, Text
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from skill_sdk.utils.util import CamelModel


class SessionRequestDto(CamelModel):
    new_session: bool
    id: str
    attributes: Dict[str, str]


class SkillContextAttributeValueDto(CamelModel):
    id: int
    value: str
    nested_in: List[int]
    overlaps_with: List[int]
    extras: Dict[str, str]


class SkillContextDto(CamelModel):
    intent: str
    skill_id: str
    attributes: Optional[Dict[str, List[str]]]
    attributesV2: Optional[Dict[str, List[SkillContextAttributeValueDto]]]
    tokens: Dict[str, str]
    locale: str
    configuration: Dict[str, List[str]]
    user_profile_config: str
    client_type_name: str


class SkillFitnessInitiateJudgement(CamelModel):
    context: SkillContextDto
    session: SessionRequestDto
    spi_version: str


class SkillFitContentMap(CamelModel):
    skillFitConfidence: float


class SkillAssessmentResultType(Text, Enum):
    NOT_IMPLEMENTED = "501"
    CONNECTION_FAILED = "502"
    TIMEOUT = "408"
    OK = "200"


class SkillFitAssessmentObject(CamelModel):
    result_type: SkillAssessmentResultType
    content_version: str
    content_map: Dict[str, str]


class SkillFitAssessmentSingleton(object):
    _instance = None
    _skill_fit_assess_func: Callable

    def __init__(self):
        if SkillFitAssessmentSingleton._instance is None:
            raise RuntimeError('Call SkillFitAssessmentSingleton.instance() instead')
        else:
            SkillFitAssessmentSingleton._instance = self

    def set_response_implementation(self, func_name):
        self._skill_fit_assess_func = func_name

    def get_response_implementation(self, r: SkillFitnessInitiateJudgement):
        response_object = self._skill_fit_assess_func(r)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=dict(resultType=response_object.result_type,
                                         contentMap=jsonable_encoder(response_object.content_map),
                                         contentVersion=response_object.content_version))

    def return_default_response_implementation(self, r: SkillFitnessInitiateJudgement):
        return SkillFitAssessmentObject(result_type=SkillAssessmentResultType.NOT_IMPLEMENTED, content_version=1.0,
                                        content_map=dict(SkillFitContentMap(skillFitConfidence=0.0)))

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._skill_fit_assess_func = cls.return_default_response_implementation

        return cls._instance
