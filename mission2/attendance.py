from typing import List, Dict
from abc import abstractmethod, ABC

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WEEKDAY_INDEX = {d: i for i, d in enumerate(DAYS)}
DAY_POINTS = {"monday": 1, "tuesday": 1, "wednesday": 3, "thursday": 1, "friday": 1, "saturday": 2, "sunday": 2}


class Member:
    def __init__(self, name: str):
        self.name = name
        self.attendance = [0] * 7
        self.points = 0
        self.grade = 0

    def attend(self, day: str):
        idx = WEEKDAY_INDEX[day]
        self.attendance[idx] += 1
        self.points += DAY_POINTS.get(day, 0)

    @property
    def wed_count(self):
        return self.attendance[WEEKDAY_INDEX["wednesday"]]

    @property
    def weekend_count(self):
        return self.attendance[WEEKDAY_INDEX["saturday"]] + self.attendance[WEEKDAY_INDEX["sunday"]]


class Policy(ABC):
    """
    test coverage 100% 달성을 위해 "pragma: no cover" 주석 추가
    참고 링크: https://coverage.readthedocs.io/en/coverage-5.2.1/excluding.html
             https://github.com/pytest-dev/pytest-cov/issues/428
    """
    registry = []

    @abstractmethod
    def apply(self, member: Member):  # pragma: no cover
        pass

    def __init_subclass__(cls):
        super().__init_subclass__()
        Policy.registry.append(cls)


class BonusWednesdayPolicy(Policy):
    def apply(self, member: Member):
        if member.wed_count > 9:
            member.points += 10


class BonusWeekendPolicy(Policy):
    def apply(self, member: Member):
        if member.weekend_count > 9:
            member.points += 10


class Grader:
    def compute(self, point: int) -> int:
        if point >= 50:
            return 1
        if point >= 30:
            return 2
        return 0

    def label(self, grade: int) -> str:
        return {1: "GOLD", 2: "SILVER"}.get(grade, "NORMAL")


class AttendanceSystem:
    def __init__(self):
        self.members: Dict[str, Member] = {}
        self.policies = Policy.registry
        self.grader = Grader()

    def ensure_member(self, name: str) -> Member:
        if name not in self.members:
            self.members[name] = Member(name)
        return self.members[name]

    def check_bad_member(self, member):
        return (member.grade == 0 and
                member.wed_count == 0 and
                member.weekend_count == 0)

    def load_attendance(self, lines, limit=500):
        for i, line in enumerate(lines):
            if i >= limit:
                break
            parsed = self.parse_line(line)
            if not parsed:
                continue
            name, weekday = parsed
            member = self.ensure_member(name)
            member.attend(weekday)

    def parse_line(self, line: str):
        parts = line.strip().split()
        if len(parts) != 2:
            return None
        name, weekday = parts[0], parts[1].lower()
        if weekday not in WEEKDAY_INDEX:
            return None
        return name, weekday

    def apply_policies(self):
        for member in self.members.values():
            for policy in self.policies:
                policy().apply(member)

    def finalize_grades(self):
        for member in self.members.values():
            member.grade = self.grader.compute(member.points)

    def print_report(self):
        for member in self.members.values():
            label = self.grader.label(member.grade)
            print(f"NAME : {member.name}, POINT : {member.points}, GRADE : {label}")

        print("\nRemoved player")
        print("==============")
        for member in self.members.values():
            if self.check_bad_member(member):
                print(member.name)

    def show_result(self, attendance_file):
        try:
            with open(attendance_file, 'r', encoding='utf-8') as lines:
                self.load_attendance(lines, limit=500)
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            return

        self.apply_policies()
        self.finalize_grades()
        self.print_report()
