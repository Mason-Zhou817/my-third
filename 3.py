#import json
'''
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Student:
    """学生实体类，保存单个学生的基本信息。"""

    student_id: str
    name: str
    age: int
    gender: str
    major: str
    phone: str

    def update(self, name=None, age=None, gender=None, major=None, phone=None):
        if name:
            self.name = name
        if age is not None:
            self.age = age
        if gender:
            self.gender = gender
        if major:
            self.major = major
        if phone:
            self.phone = phone


class StudentManager:
    """学生管理类，负责业务逻辑和数据持久化。"""

    def __init__(self, data_file="students.json"):
        self.data_file = Path(data_file)
        self.students = {}
        self.load()

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("该学号已存在")
        self.students[student.student_id] = student
        self.save()

    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError("未找到该学生")
        del self.students[student_id]
        self.save()

    def update_student(self, student_id, **kwargs):
        student = self.find_student(student_id)
        if student is None:
            raise ValueError("未找到该学生")
        student.update(**kwargs)
        self.save()

    def find_student(self, student_id):
        return self.students.get(student_id)

    def list_students(self):
        return list(self.students.values())

    def save(self):
        data = [asdict(student) for student in self.students.values()]
        self.data_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self):
        if not self.data_file.exists():
            return

        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []

        for item in data:
            student = Student(**item)
            self.students[student.student_id] = student


class ConsoleApp:
    """控制台交互类，负责菜单和用户输入。"""

    def __init__(self):
        self.manager = StudentManager()

    def run(self):
        while True:
            self.show_menu()
            choice = input("请选择操作：").strip()

            try:
                if choice == "1":
                    self.add_student()
                elif choice == "2":
                    self.delete_student()
                elif choice == "3":
                    self.update_student()
                elif choice == "4":
                    self.find_student()
                elif choice == "5":
                    self.show_all_students()
                elif choice == "0":
                    print("已退出学生信息管理系统。")
                    break
                else:
                    print("输入无效，请重新选择。")
            except ValueError as error:
                print(f"操作失败：{error}")

    @staticmethod
    def show_menu():
        print("\n========== 学生信息管理系统 ==========")
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改学生")
        print("4. 查询学生")
        print("5. 显示所有学生")
        print("0. 退出系统")
        print("====================================")

    def add_student(self):
        student = Student(
            student_id=self.read_required("请输入学号："),
            name=self.read_required("请输入姓名："),
            age=self.read_int("请输入年龄："),
            gender=self.read_required("请输入性别："),
            major=self.read_required("请输入专业："),
            phone=self.read_required("请输入电话："),
        )
        self.manager.add_student(student)
        print("添加成功。")

    def delete_student(self):
        student_id = self.read_required("请输入要删除的学生学号：")
        self.manager.delete_student(student_id)
        print("删除成功。")

    def update_student(self):
        student_id = self.read_required("请输入要修改的学生学号：")
        student = self.manager.find_student(student_id)
        if student is None:
            raise ValueError("未找到该学生")

        print("直接回车表示保留原信息。")
        name = input(f"姓名（当前：{student.name}）：").strip()
        age_text = input(f"年龄（当前：{student.age}）：").strip()
        gender = input(f"性别（当前：{student.gender}）：").strip()
        major = input(f"专业（当前：{student.major}）：").strip()
        phone = input(f"电话（当前：{student.phone}）：").strip()

        age = int(age_text) if age_text else None
        self.manager.update_student(
            student_id,
            name=name,
            age=age,
            gender=gender,
            major=major,
            phone=phone,
        )
        print("修改成功。")

    def find_student(self):
        student_id = self.read_required("请输入要查询的学生学号：")
        student = self.manager.find_student(student_id)
        if student is None:
            print("未找到该学生。")
            return
        self.print_student(student)

    def show_all_students(self):
        students = self.manager.list_students()
        if not students:
            print("暂无学生信息。")
            return

        print("\n所有学生信息：")
        for student in students:
            self.print_student(student)

    @staticmethod
    def print_student(student):
        print(
            f"学号：{student.student_id} | "
            f"姓名：{student.name} | "
            f"年龄：{student.age} | "
            f"性别：{student.gender} | "
            f"专业：{student.major} | "
            f"电话：{student.phone}"
        )

    @staticmethod
    def read_required(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("输入不能为空，请重新输入。")

    @staticmethod
    def read_int(prompt):
        while True:
            value = input(prompt).strip()
            try:
                number = int(value)
                if number <= 0:
                    print("请输入正整数。")
                    continue
                return number
            except ValueError:
                print("请输入合法整数。")


if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
'''
import json
from pathlib import Path


class JsonConfigTool:
    """JSON 配置文件处理工具：读取、修改、保存配置。"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = {}

    def load(self):
        """读取 JSON 配置文件。"""
        if not self.file_path.exists():
            self.data = {}
            return self.data

        try:
            content = self.file_path.read_text(encoding="utf-8")
            self.data = json.loads(content) if content.strip() else {}
            return self.data
        except json.JSONDecodeError as error:
            raise ValueError(f"JSON 格式错误：{error}") from error

    def save(self):
        """保存 JSON 配置文件。"""
        self.file_path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_value(self, key_path, default=None):
        """按点号路径读取值，例如 database.host。"""
        current = self.data
        for key in key_path.split("."):
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current

    def set_value(self, key_path, value):
        """按点号路径修改值，不存在的中间层会自动创建。"""
        keys = key_path.split(".")
        current = self.data

        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

    def delete_value(self, key_path):
        """按点号路径删除配置项。"""
        keys = key_path.split(".")
        current = self.data

        for key in keys[:-1]:
            if not isinstance(current, dict) or key not in current:
                return False
            current = current[key]

        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]
            return True
        return False

    def show(self):
        """格式化显示当前配置。"""
        print(json.dumps(self.data, ensure_ascii=False, indent=2))


class ConsoleApp:
    """命令行交互界面。"""

    def __init__(self):
        file_path = input("请输入 JSON 配置文件路径（默认 config.json）：").strip()
        self.tool = JsonConfigTool(file_path or "config.json")
        self.tool.load()

    def run(self):
        while True:
            self.show_menu()
            choice = input("请选择操作：").strip()

            try:
                if choice == "1":
                    self.tool.show()
                elif choice == "2":
                    self.query_config()
                elif choice == "3":
                    self.modify_config()
                elif choice == "4":
                    self.delete_config()
                elif choice == "5":
                    self.tool.save()
                    print("保存成功。")
                elif choice == "0":
                    print("已退出 JSON 数据处理工具。")
                    break
                else:
                    print("输入无效，请重新选择。")
            except ValueError as error:
                print(f"操作失败：{error}")

    @staticmethod
    def show_menu():
        print("\n========== JSON 数据处理工具 ==========")
        print("1. 显示全部配置")
        print("2. 查询配置项")
        print("3. 修改配置项")
        print("4. 删除配置项")
        print("5. 保存配置文件")
        print("0. 退出")
        print("=====================================")

    def query_config(self):
        key_path = self.read_required("请输入配置路径，例如 database.host：")
        value = self.tool.get_value(key_path, "未找到该配置项")
        print(f"{key_path} = {value}")

    def modify_config(self):
        key_path = self.read_required("请输入配置路径，例如 database.host：")
        raw_value = input("请输入新值（支持数字、布尔值、数组、对象、字符串）：").strip()
        value = self.parse_value(raw_value)
        self.tool.set_value(key_path, value)
        print("修改成功。")

    def delete_config(self):
        key_path = self.read_required("请输入要删除的配置路径：")
        if self.tool.delete_value(key_path):
            print("删除成功。")
        else:
            print("未找到该配置项。")

    @staticmethod
    def parse_value(raw_value):
        """尽量按 JSON 类型解析输入，解析失败时作为普通字符串保存。"""
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError:
            return raw_value

    @staticmethod
    def read_required(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("输入不能为空，请重新输入。")


if __name__ == "__main__":
    app = ConsoleApp()
    app.run()

'''
from datetime import datetime
from pathlib import Path
import traceback
class SimpleLogger:
    """简单日志记录器：记录程序运行状态和错误信息。"""

    LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}

    def __init__(self, log_file="app.log", console_output=True):
        self.log_file = Path(log_file)
        self.console_output = console_output
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def debug(self, message):
        self._write("DEBUG", message)

    def info(self, message):
        self._write("INFO", message)

    def warning(self, message):
        self._write("WARNING", message)

    def error(self, message):
        self._write("ERROR", message)

    def exception(self, message, error):
        """记录异常信息和完整错误堆栈。"""
        detail = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        self._write("ERROR", f"{message}\n{detail}")

    def _write(self, level, message):
        if level not in self.LEVELS:
            raise ValueError(f"不支持的日志级别：{level}")

        log_text = self._format(level, message)
        self.log_file.write_text(
            self._read_existing_content() + log_text + "\n",
            encoding="utf-8",
        )

        if self.console_output:
            print(log_text)

    def _format(self, level, message):
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_text}] [{level}] {message}"

    def _read_existing_content(self):
        if not self.log_file.exists():
            return ""
        return self.log_file.read_text(encoding="utf-8")


def divide(a, b, logger):
    logger.info(f"准备计算：{a} / {b}")
    try:
        result = a / b
        logger.info(f"计算成功，结果为：{result}")
        return result
    except ZeroDivisionError as error:
        logger.exception("计算失败：除数不能为 0", error)
        return None


if __name__ == "__main__":
    logger = SimpleLogger("program.log")

    logger.info("程序启动")
    logger.debug("正在初始化数据")
    logger.warning("当前使用的是示例配置")

    divide(10, 2, logger)
    divide(10, 0, logger)

    logger.info("程序结束")
'''