DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WEEKDAY_INDEX = {d: i for i, d in enumerate(DAYS)}
DAY_POINTS = {
    "monday": 1, "tuesday": 1, "wednesday": 3,
    "thursday": 1, "friday": 1, "saturday": 2, "sunday": 2,
}
MEMBER_COUNT_LIMIT = 100

name_to_member_id = {}
member_count = 0

attendance_by_day = [[0] * MEMBER_COUNT_LIMIT for _ in range(MEMBER_COUNT_LIMIT)]
points = [0] * MEMBER_COUNT_LIMIT
grade = [0] * MEMBER_COUNT_LIMIT
names = [''] * MEMBER_COUNT_LIMIT
wednesday_count = [0] * MEMBER_COUNT_LIMIT
weekend_count = [0] * MEMBER_COUNT_LIMIT


def ensure_member(member_name):
    global member_count

    if member_name in name_to_member_id:
        return name_to_member_id[member_name]

    member_count += 1
    member_id = member_count
    name_to_member_id[member_name] = member_id
    names[member_id] = member_name
    attendance_by_day[member_id] = [0] * 7
    points[member_id] = 0
    grade[member_id] = 0
    wednesday_count[member_id] = 0
    weekend_count[member_id] = 0
    return member_id


def update_attendance(member_id, weekday):
    idx = WEEKDAY_INDEX[weekday]
    attendance_by_day[member_id][idx] += 1
    points[member_id] += DAY_POINTS[weekday]
    if weekday == "wednesday":
        wednesday_count[member_id] += 1
    if weekday in ("saturday", "sunday"):
        weekend_count[member_id] += 1


def parse_line(line: str):
    parts = line.strip().split()
    if len(parts) != 2:
        return None
    name, weekday = parts[0], parts[1].lower()
    if weekday not in WEEKDAY_INDEX:
        return None
    return name, weekday


def apply_bonuses() -> None:
    for member_id in range(1, member_count + 1):
        if attendance_by_day[member_id][2] > 9:  # thursday count
            points[member_id] += 10
        if (attendance_by_day[member_id][5] + attendance_by_day[member_id][6]) > 9:  # weekend total
            points[member_id] += 10


def load_attendance(lines, limit=500):
    for i, line in enumerate(lines):
        if i >= limit:
            break
        parsed = parse_line(line)
        if not parsed:
            continue
        name, weekday = parsed
        member_id = ensure_member(name)
        update_attendance(member_id, weekday)


def compute_grade(point):
    if point >= 50:
        return 1
    if point >= 30:
        return 2
    return 0


def grade_label(g):
    return {1: "GOLD", 2: "SILVER"}.get(g, "NORMAL")


def finalize_grades() -> None:
    for member_id in range(1, member_count + 1):
        grade[member_id] = compute_grade(points[member_id])


def print_report() -> None:
    for member_id in range(1, member_count + 1):
        print(f"NAME : {names[member_id]}, POINT : {points[member_id]}, GRADE : {grade_label(grade[member_id])}")
    print("\nRemoved player")
    print("==============")
    for member_id in range(1, member_count + 1):
        if grade[member_id] == 0 and wednesday_count[member_id] == 0 and weekend_count[member_id] == 0:
            print(names[member_id])


def show_result(attendance_file):
    try:
        with open(attendance_file, 'r', encoding='utf-8') as lines:
            load_attendance(lines, limit=500)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return

    apply_bonuses()
    finalize_grades()
    print_report()
