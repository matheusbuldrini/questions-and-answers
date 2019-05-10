from pybuilder.core import use_plugin, init, task

# These are the plugins we want to use in our project.
# Projects provide tasks which are blocks of logic executed by PyBuilder.

use_plugin("python.core")
# the python unittest plugin allows running python's standard library unittests
use_plugin("python.unittest")
use_plugin("python.coverage")
# this plugin allows installing project dependencies with pip
use_plugin("python.install_dependencies")
# a linter plugin that runs flake8 (pyflakes + pep8) on our project sources
#use_plugin("python.flake8")
# a plugin that measures unit test statement coverage

# The project name
name = "eswqa"
# What PyBuilder should run when no tasks are given.
# Calling "pyb" amounts to calling "pyb publish" here.
# We could run several tasks by assigning a list to `default_task`.
default_task = ["analyze", "task2"]

# This is an initializer, a block of logic that runs before the project is built.
@init
def set_properties(project):
    project.set_property("coverage_break_build", False)
    project.set_property('dir_source_main_python', 'classes')
    project.set_property("dir_source_unittest_python", "unittests")

@task
@depends("analyze")
def task2():
    print("Hello from task2")
