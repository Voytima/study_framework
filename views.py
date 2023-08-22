from divo_framework.templator import render
from components.models import Engine, MapperRegistry
from components.decorators import AppRoute
from components.cbv import ListView, CreateView
from components.unit_of_work import UnitOfWork

app = Engine()
"""
Decorators execute during ***IMPORT*** stage.
It means, when we create global variable "routes = {}",
even without calling the controllers
using decorators like "@AppRoute(routes=routes, url='/')"
will fill out dictionary "routes" with needed routes.
"""
routes = {}
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


# Class-controller "Main page"
@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=app.categories)


# Class-controller "About project" page
@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


# Class-controller "Schedule" page
@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html')


# Class-controller "Page 404"
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page Not Found'


# Class-controller "Courses list" page
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, request):
        try:
            category = app.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# Class-controller "Create course" page
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = 1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = app.decode_value(name)

            category = None
            if self.category_id != -1:
                category = app.find_category_by_id(int(self.category_id))
                course = app.create_course('record', name, category)
                app.courses.append(course)
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = app.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# Class-controller "Create category" page
@AppRoute(routes=routes, url='/create-category/')
class CategoriesCreateView(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):

        name = data.get('name')
        name = app.decode_value(name)

        new_category = app.create_category()
        app.categories.append(new_category)

        schema = {'name': name}
        new_category.mark_new(schema)
        UnitOfWork.get_current().commit()


# Class-controller - "List of categories" page
@AppRoute(routes=routes, url='/category-list/')
class CategoryList(ListView):
    template_name = 'category_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data.get('name')
        name = app.decode_value(name)
        new_obj = app.create_user('student')

        app.students.append(new_obj)
        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = app.courses
        context['students'] = app.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = app.decode_value(course_name)
        course = app.get_course(course_name)
        student_name = data['student_name']
        student_name = app.decode_value(student_name)
        student = app.get_student(student_name)
        course.add_student(student)
