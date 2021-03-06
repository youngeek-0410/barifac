import datetime
from logging import getLogger

import requests
from app.crud import (
    DepartmentCRUD,
    EvaluationCRUD,
    SchoolCRUD,
    SubjectCRUD,
    TeacherCRUD,
    TermCRUD,
)
from app.db.database import get_db_session
from app.schemas import (
    CreateDepartmentSchema,
    CreateEvaluationSchema,
    CreateSchoolSchema,
    CreateSubjectSchema,
    CreateTeacherSchema,
    CreateTermSchema,
)
from bs4 import BeautifulSoup  # 取得したデータの解析
from tqdm import tqdm

SYLLABUS_URL = "https://syllabus.kosen-k.go.jp/Pages/PublicSchools"
SYLLABUS_TOP_URL = "https://syllabus.kosen-k.go.jp"

logger = getLogger(__name__)
db_session = get_db_session()


def add_school_to_db(
    is_add_department=False, is_add_subject=False, processing_school_name=None
) -> None:
    is_before_processing_school = False if processing_school_name is None else True
    res = requests.get(SYLLABUS_URL)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text, "html.parser")
    school_soup_list = soup.find(string="学校一覧").parent.parent.parent
    school_a_list = school_soup_list.find_all("a")
    for school_a in tqdm(school_a_list, position=0, desc="school"):
        if school_a.parent["style"] == "display:none":
            continue
        school_name = school_a.text
        if processing_school_name and school_name == processing_school_name:
            is_before_processing_school = False
        if is_before_processing_school:
            continue
        school_url = SYLLABUS_TOP_URL + school_a.get("href")
        school = SchoolCRUD(db_session).get_by_name(school_name)
        if not school:
            school_schema = CreateSchoolSchema(
                name=school_name,
                syllabus_url=school_url,
            )
            school = SchoolCRUD(db_session).create(school_schema.dict())
            tqdm.write(f"Created school: {school.name}")
        else:
            tqdm.write(f"Skipped school: {school.name}")
        db_session.commit()

        if is_add_department:
            add_department_to_db(school, school_url, is_add_subject)


def add_department_to_db(school, school_url, is_add_subject) -> None:
    res = requests.get(school_url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text, "html.parser")
    department_soup_list = soup.find_all(string="本年度の開講科目一覧")
    for department_soup in tqdm(department_soup_list, position=1, desc="department"):
        department_name = department_soup.parent.parent.parent.find("h4").text
        if "専攻" in department_name:
            continue
        department_url = SYLLABUS_TOP_URL + department_soup.parent.attrs["href"]
        department = DepartmentCRUD(db_session).get_by_school_and_name(
            school, department_name
        )
        if not department:
            department_schema = CreateDepartmentSchema(
                name=department_name,
                school_uuid=school.uuid,
                syllabus_url=department_url,
            )
            department = DepartmentCRUD(db_session).create(department_schema.dict())
            tqdm.write(
                f"Created department: {department.school.name}-{department_name}"
            )
        else:
            tqdm.write(
                f"Skipped department: {department.school.name}-{department_name}"
            )
        db_session.commit()

        if is_add_subject:
            add_subject_to_db(department, department_url)


def add_subject_to_db(department, department_url) -> None:
    current_year = datetime.date.today().year

    res = requests.get(department_url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text, "html.parser")
    subject_tr_soup_list = soup.find_all("tr")
    for subject_tr_soup in tqdm(subject_tr_soup_list, position=2, desc="subject"):
        if not subject_tr_soup.has_attr("data-course-value"):
            continue
        subject_td_soup_list = subject_tr_soup.find_all("td")
        for i, grade in enumerate([1, 2, 3, 4, 5]):
            for j, semester in enumerate(["前期", "後期"]):
                if len(subject_td_soup_list) == 16:  # 専攻科判定
                    continue
                if subject_td_soup_list[6 + i * 4 + j * 2].text == "":
                    continue
                general_special = subject_td_soup_list[0].text
                required_optional = subject_td_soup_list[1].text
                subject_url = SYLLABUS_TOP_URL + subject_tr_soup.find("a").get("href")
                subject_name = subject_tr_soup.find("a").text
                # subject_id = subject_td_soup_list[3].text
                # subject_credit_type = subject_td_soup_list[4].text
                subject_credits = subject_td_soup_list[5].text
                subject_grade = grade
                subject_semester = semester
                subject_teachers = list(
                    subject_td_soup_list[26]
                    .text.replace("\r\n", "")
                    .replace(" ", "")
                    .split(",")
                )
                term = TermCRUD(db_session).get_by_year_and_semester(
                    current_year, subject_semester
                )
                if not term:
                    term_schema = CreateTermSchema(
                        academic_year=current_year,
                        semester=subject_semester,
                    )
                    term = TermCRUD(db_session).create(term_schema.dict())
                    tqdm.write(f"Created term: {term.academic_year}-{term.semester}")
                    db_session.flush()
                for teacher_name in subject_teachers:
                    teacher = TeacherCRUD(db_session).get_by_name_and_school(
                        teacher_name, department.school
                    )
                    if not teacher:
                        teacher_schema = CreateTeacherSchema(
                            name=teacher_name,
                            school_uuid=department.school.uuid,
                        )
                        teacher = TeacherCRUD(db_session).create(teacher_schema.dict())
                        tqdm.write(f"Created teacher: {teacher.name}")
                        db_session.flush()
                    subject = SubjectCRUD(db_session).get_by_name_term_school_teacher(
                        subject_name, term, department.school, teacher
                    )
                    if subject:
                        tqdm.write(
                            f"Skipped subject: {subject.name}({subject.school.name} "
                            f"{subject.term.academic_year}-{subject.term.semester}) [{subject.teacher.name}]"
                        )
                        continue
                    else:
                        subject_schema = CreateSubjectSchema(
                            name=subject_name,
                            term_uuid=term.uuid,
                            school_uuid=department.school.uuid,
                            teacher_uuid=teacher.uuid,
                            credits=subject_credits,
                            target_grade=subject_grade,
                            department_uuid=None
                            if general_special == "一般"
                            else department.uuid,
                            category=general_special,
                            type=required_optional,
                            syllabus_url=subject_url,
                        )
                        subject = SubjectCRUD(db_session).create(subject_schema.dict())
                        tqdm.write(
                            f"Created subject: {subject.name}({subject.school.name} "
                            f"{subject.term.academic_year}-{subject.term.semester}) [{subject.teacher.name}]"
                        )
                        db_session.flush()
                        add_evaluation_to_db(subject, subject_url)


def add_evaluation_to_db(subject, subject_url) -> None:
    res = requests.get(subject_url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text, "html.parser")
    evaluation_table_soup = soup.find(
        "table", id="MainContent_SubjectSyllabus_wariaiTable"
    )
    evaluation_tr_soup_list = evaluation_table_soup.find_all("tr")
    for name_td, rate_td in zip(evaluation_tr_soup_list[0], evaluation_tr_soup_list[1]):
        evaluation_name = name_td.text.replace("\r\n", "").replace(" ", "")
        evaluation_rate = rate_td.text.replace("\r\n", "").replace(" ", "")
        if evaluation_name == "" or not evaluation_rate.isdigit():
            continue
        evaluation_rate = int(evaluation_rate)
        if evaluation_rate <= 0 or evaluation_rate >= 100:
            continue
        evaluation = EvaluationCRUD(db_session).get_by_name_and_subject(
            evaluation_name, subject
        )
        if not evaluation:
            evaluation_schema = CreateEvaluationSchema(
                name=evaluation_name,
                rate=evaluation_rate,
                type=evaluation_name,  # TODO: fix
                subject_uuid=subject.uuid,
            )
            evaluation = EvaluationCRUD(db_session).create(evaluation_schema.dict())
            tqdm.write(
                f"Created evaluation: {evaluation.name}-{evaluation.rate}({evaluation.subject.name})"
            )
            db_session.flush()
        else:
            tqdm.write(
                f"Skipped evaluation: {evaluation.name}-{evaluation.rate}({evaluation.subject.name})"
            )
    db_session.commit()


def add_all_data(school_name=None) -> None:
    add_school_to_db(
        is_add_department=True,
        is_add_subject=True,
        processing_school_name=school_name,
    )


def add_schools() -> None:
    add_school_to_db(is_add_department=False, is_add_subject=False)


def add_schools_and_departments() -> None:
    add_school_to_db(is_add_department=True, is_add_subject=False)


def add_subjects_with_school_and_department(school_name, department_name) -> None:
    school = SchoolCRUD(db_session).get_by_name(school_name)
    assert school is not None
    department = DepartmentCRUD(db_session).get_by_school_and_name(
        school, department_name
    )
    assert department is not None
    add_subject_to_db(
        department,
        department.syllabus_url,
    )
