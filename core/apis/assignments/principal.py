from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)


@principal_assignments_resources.route("", methods=["GET"], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_and_graded_assignments(p):
    """Returns list of assignments"""
    submitted_and_graded_assignments = Assignment.get_submitted_and_graded_assignments()
    submitted_and_graded_assignments_dump = AssignmentSchema().dump(
        submitted_and_graded_assignments, many=True
    )
    return APIResponse.respond(data=submitted_and_graded_assignments_dump)


@principal_assignments_resources.route("/grade", methods=["POST"], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or regrade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.principal_mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p,
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)