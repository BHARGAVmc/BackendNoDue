def assign_requirements_to_student(student):
    from .models import Subject, FacultyRequirementTemplate, StudentRequirementStatus

    subjects = Subject.objects.filter(
        branch=student.branch,
        year=student.year,
        sem=student.sem,
        section=student.section
    )

    for subject in subjects:
        templates = FacultyRequirementTemplate.objects.filter(subject_code=subject.subject_code)
        for template in templates:
            exists = StudentRequirementStatus.objects.filter(
                student_roll_no=student.roll_no,
                subject_code=subject.subject_code,
                faculty_email=template.faculty_email,
                requirement=template.requirement
            ).exists()
            if not exists:
                StudentRequirementStatus.objects.create(
                    student_roll_no=student.roll_no,
                    subject_code=subject.subject_code,
                    faculty_email=template.faculty_email,
                    requirement=template.requirement,
                    softcopy_required=template.softcopy_required,
                    status=False,
                    file=None
                )
