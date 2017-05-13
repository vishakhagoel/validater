from . import validate_approvals
import pytest

APPROVER_1 = 'approver_1'
APPROVER_2 = 'approver_2'
DEPENDENCIES = 'DEPENDENCIES'

def test_reading_file_with_single_entity(tmpdir):
    test_file = tmpdir.join('test_file')
    test_file.write(APPROVER_1)
    assert validate_approvals.read_file(test_file) == [APPROVER_1]


def test_reading_file_with_multiple_entities(tmpdir):
    test_file = tmpdir.join('test_file')
    test_file.write(APPROVER_1 + '\n' + APPROVER_2)
    assert validate_approvals.read_file(test_file) == [APPROVER_1, APPROVER_2]


def test_building_dependency_map(tmpdir):
    root = tmpdir.mkdir('root')
    backend_folder = root.mkdir('backend')
    backend_deps = backend_folder.join(DEPENDENCIES)
    backend_deps.write('this/is/a/test')

    frontend_folder = root.mkdir('frontend')
    frontend_deps = frontend_folder.join(DEPENDENCIES)
    frontend_deps.write('/this/is/another/test')
    map = validate_approvals.build_dependency_map(root.realpath())
    assert map['this/is/a/test'] == [backend_folder.realpath()]
    assert map['/this/is/another/test'] == [frontend_folder.realpath()]