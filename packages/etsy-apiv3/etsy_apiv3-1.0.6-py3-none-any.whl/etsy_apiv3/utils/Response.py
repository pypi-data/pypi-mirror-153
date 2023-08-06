from pydantic.generics import GenericModel
from typing import Generic, TypeVar, List

ResultsT = TypeVar('ResultsT')

class Response(GenericModel, Generic[ResultsT]):
    count: int
    results: List[ResultsT]
