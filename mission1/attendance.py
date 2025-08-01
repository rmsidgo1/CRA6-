name_to_member_id = {}
member_count = 0

# dat[사용자ID][요일]
attendance_by_day = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
names = [''] * 100
wednesday_attendance_count = [0] * 100
weekend_attendance_count = [0] * 100


def input2(name, weekday):
    global member_count

    if name not in name_to_member_id:
        member_count += 1
        name_to_member_id[name] = member_count
        names[member_count] = name

    member_id = name_to_member_id[name]

    take_attendance(member_id, weekday)


def take_attendance(member_id, weekday):
    add_point = 0
    index = 0

    if weekday == "monday":
        index = 0
        add_point += 1
    elif weekday == "tuesday":
        index = 1
        add_point += 1
    elif weekday == "wednesday":
        index = 2
        add_point += 3
        wednesday_attendance_count[member_id] += 1
    elif weekday == "thursday":
        index = 3
        add_point += 1
    elif weekday == "friday":
        index = 4
        add_point += 1
    elif weekday == "saturday":
        index = 5
        add_point += 2
        weekend_attendance_count[member_id] += 1
    elif weekday == "sunday":
        index = 6
        add_point += 2
        weekend_attendance_count[member_id] += 1

    attendance_by_day[member_id][index] += 1
    points[member_id] += add_point


def show_grade(attendance_file="attendance_weekday_500.txt"):
    try:
        with open(attendance_file, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    input2(parts[0], parts[1])

        for i in range(1, member_count + 1):
            if attendance_by_day[i][3] > 9:
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
            if grade[i] not in (1, 2) and wednesday_attendance_count[i] == 0 and weekend_attendance_count[i] == 0:
                print(names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    show_grade()
