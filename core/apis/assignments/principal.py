from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_assignments(p):
    """
    Lists all submitted and graded assignments.
    Only accessible to authenticated principals.
    """
    all_submitted_and_graded_assignments = Assignment.get_all_submitted_and_graded_assignments()
    all_submitted_and_graded_assignments_dump = AssignmentSchema().dump(
        all_submitted_and_graded_assignments, many=True
    )
    
    print(all_submitted_and_graded_assignments_dump)
    
    return APIResponse.respond(data=all_submitted_and_graded_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_all_teachers(p):
    """
    Lists all teachers in the system.
    Only accessible to authenticated principals.
    """
    all_teachers = Teacher.get_all_teachers()
    all_teachers_dump = TeacherSchema().dump(all_teachers, many=True)
    
    return APIResponse.respond(data=all_teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignments(p, incoming_payload):
    """
    Grades or regrades an assignment.
    Only accessible to authenticated principals, with input validation.
    """
    grade_or_regrade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    graded_or_regraded_assignment = Assignment.mark_grade(
        _id=grade_or_regrade_assignment_payload.id,
        grade=grade_or_regrade_assignment_payload.grade,
        auth_principal=p,
    )
    
    db.session.commit()
    
    graded_or_regraded_assignment_dump = AssignmentSchema().dump(graded_or_regraded_assignment)
    
    return APIResponse.respond(data=graded_or_regraded_assignment_dump)
