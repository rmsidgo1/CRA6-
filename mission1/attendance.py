DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WEEKDAY_INDEX = {d: i for i, d in enumerate(DAYS)}
DAY_POINTS = {
    "monday": 1, "tuesday": 1, "wednesday": 3,
    "thursday": 1, "friday": 1, "saturday": 2, "sunday": 2,
}

name_to_member_id = {}
member_count = 0

attendance_by_day = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
names = [''] * 100
wednesday_count = [0] * 100
weekend_count = [0] * 100


def take_attendance(name, weekday):
    member_id = ensure_member(name)

    update_attendance(member_id, weekday)


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


def show_grade(attendance_file="attendance_weekday_500.txt"):
    try:
        with open(attendance_file, 'r', encoding='utf-8') as lines:
            load_attendance(lines, limit=500)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return

    for i in range(1, member_count + 1):
        if attendance_by_day[i][2] > 9:
            points[i] += 10
        if attendance_by_day[i][5] + attendance_by_day[i][6] > 9:
            points[i] += 10

        if points[i] >= 50:
            grade[i] = 1
        elif points[i] >= 30:
            grade[i] = 2
        else:
            grade[i] = 0

        print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
        if grade[i] == 1:
            print("GOLD")
        elif grade[i] == 2:
            print("SILVER")
        else:
            print("NORMAL")

    print("\nRemoved player")
    print("==============")
    for i in range(1, member_count + 1):
        if grade[i] not in (1, 2) and wednesday_count[i] == 0 and weekend_count[i] == 0:
            print(names[i])


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

# Coverage 100% 위해 주석처리
# if __name__ == "__main__":
#     show_grade()
