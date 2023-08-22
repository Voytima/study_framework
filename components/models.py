import quopri
import sqlite3
from components.unit_of_work import DomainObject
from components.universal_mapper import BaseMapper


# Abstract user class
class User:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'if' in kwargs:
            self.id = kwargs.get('id')

        self.courses = []


# Class tutor
class Teacher(User):
    pass


# Class student
class Student(User, DomainObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Class-factory of users
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # Factory method
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# Class course
class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)


# Class course interactive
class InteractiveCourse(Course):
    pass


# Class course recorded
class RecordCourse(Course):
    pass


# Class-factory of courses
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Class category
class Category(DomainObject):

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')

        self.courses = []

    def course_count(self):
        result = len(self.courses)
        return result


# Class-main project interface
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category():
        return Category()

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'No category with id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name):
        for stud in self.students:
            if stud.name == name:
                return stud

    @staticmethod
    def decode_value(val):
        val_bytes = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        value_decode_str = quopri.decodestring(val_bytes)
        return value_decode_str.decode('UTF-8')


#########################
class StudentMapper(BaseMapper):
    tablename = 'student'
    model = Student


class CategoryMapper(BaseMapper):
    tablename = 'categories'
    model = Category


connection = sqlite3.connect('project.sqlite')


# Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
