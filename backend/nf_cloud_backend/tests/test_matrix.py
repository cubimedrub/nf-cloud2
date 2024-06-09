from enum import Enum
from typing import Callable

from httpx import Response
from backend.nf_cloud_backend.tests import DbTestCase
from .constants import *


class WorkflowCase(Enum):
    PRIVATE = 1
    PUBLIC = 2
    READ_SHARED = 3
    WRITE_SHARED = 4
    OWNED = 5
    ADMIN = 6


class MatrixTest(DbTestCase):
    def workflow_params(self) -> dict[WorkflowCase, tuple[dict, int]]:
        return {
            WorkflowCase.PRIVATE:
                (self.headers_default(), WORKFLOW_2_PRIVATE),
            WorkflowCase.PUBLIC:
                (self.headers_default(), WORKFLOW_5_PUBLIC),
            WorkflowCase.READ_SHARED:
                (self.headers_default(), WORKFLOW_3_READ_SHARED),
            WorkflowCase.WRITE_SHARED:
                (self.headers_default(), WORKFLOW_4_WRITE_SHARED),
            WorkflowCase.OWNED:
                (self.headers_default(), WORKFLOW_1_OWNED),
            WorkflowCase.ADMIN:
                (self.headers_admin(), WORKFLOW_1_OWNED), 
        }
    

    def check_permissions(self, call: Callable[[dict, int], Response], responses: dict[WorkflowCase, int]):
        for case, (headers, id) in self.workflow_params().items():
            call(headers, responses)

    def test_list(self):
        self.check_permissions(
            call=lambda headers, id: self.client.get("/workflow", headers=headers),
            responses={
                WorkflowCase.PRIVATE: 200,
                WorkflowCase.PUBLIC: 200,
                WorkflowCase.READ_SHARED: 200,
                WorkflowCase.WRITE_SHARED: 200,
                WorkflowCase.OWNED: 200,
                WorkflowCase.ADMIN: 200,
            },
        )
    

    def test_matrix(self):
        self.client.post("/workflow/new", headers=self.headers_default(), json={
            "name": "newname",
        })


class MatrixRow:
    call: Callable[[dict, int], Response]
    responses: dict[WorkflowCase, int]

    def __init__(self, call: Callable[[dict, int], Response], responses: dict[WorkflowCase, int]):
        self.call = call
        self.responses = responses