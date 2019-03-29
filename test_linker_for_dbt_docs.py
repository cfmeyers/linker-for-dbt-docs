import os

from linker_for_dbt_docs import (
    make_link,
    collect_linkable_file_names,
    insert_links_in_line,
    make_link_map,
    get_dbt_project_path,
    tokenize_line,
    build_model_match_pattern,
)


class TestMakeLink:
    def test_it_takes_a_project_name_and_model_with_dot_and_makes_link(self):
        project_name = 'starfish'
        model_name = 'dim.problem_barnacles'
        expected = '<a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>'
        assert expected == make_link(project_name, model_name)

    def test_it_takes_a_project_name_and_model_with_underscore_and_makes_link(self):
        project_name = 'starfish'
        model_name = 'dim_problem_barnacles'
        expected = '<a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>'
        assert expected == make_link(project_name, model_name)


class TestCollectLinkableFileNames:
    def test_it_collects_model_names_from_absolute_path(self):
        absolute_path = os.path.abspath('fixtures/starfish')
        expected = set(['raw_barnacles', 'dim_problem_barnacles'])

        assert expected == collect_linkable_file_names(absolute_path)


class TestInsertLinksInLine:
    def test_it_inserts_link_for_single_underscored_model_name(self):
        model_names = set(['raw_barnacles', 'dim_problem_barnacles'])
        project_name = 'starfish'
        link_map = make_link_map(model_names, project_name)
        line = 'Lots of rows in dim_problem_barnacles.'

        expected = 'Lots of rows in <a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>.'

        assert expected == insert_links_in_line(link_map, line)

    def test_it_inserts_link_for_single_dotted_model_name(self):
        model_names = set(['raw_barnacles', 'dim_problem_barnacles'])
        project_name = 'starfish'
        link_map = make_link_map(model_names, project_name)
        line = 'Lots of rows in dim.problem_barnacles.'

        expected = 'Lots of rows in <a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>.'

        assert expected == insert_links_in_line(link_map, line)

    def test_it_inserts_link_for_two_model_names(self):
        model_names = set(['raw_barnacles', 'dim_problem_barnacles'])
        project_name = 'starfish'
        link_map = make_link_map(model_names, project_name)
        line = 'Lots of rows in dim.problem_barnacles, dim_problem_barnacles.'

        expected = 'Lots of rows in <a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>, <a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>.'

        assert expected == insert_links_in_line(link_map, line)

    def test_it_does_not_insert_link_inside_of_linke(self):
        model_names = set(['raw_barnacles', 'dim_problem_barnacles'])
        project_name = 'starfish'
        link_map = make_link_map(model_names, project_name)
        line = 'Lots of rows in <a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>.'
        assert line == insert_links_in_line(link_map, line)


class TestTokenizeLine:
    def test_it_returns_single_item_for_line_with_no_anchor_tags(self):
        line = 'Lots of rows in dim.problem_barnacles, dim_problem_barnacles.'
        assert [line] == tokenize_line(line)

    def test_it_splits_line_by_anchor_tags(self):
        line = 'Lots of rows in <a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>.'
        expected = [
            'Lots of rows in ',
            '<a href="#!/model/model.starfish.dim_problem_barnacles">dim.problem_barnacles</a>',
            '.',
        ]
        assert expected == tokenize_line(line)


class TestBuildModelMatchPattern:
    def test_it(self):
        model_names = set(['prob_barnacles', 'prob_barnacles_cleaned'])
        expected = r'(prob_barnacles_cleaned|prob_barnacles)'

        assert expected == build_model_match_pattern(model_names)


class TestGetDBTProjectPath:
    def test_it(self):
        absolute_path = os.path.abspath(
            'fixtures/starfish/models/transform/dim_problem_barnacles.md'
        )
        expected = os.path.abspath('fixtures/starfish')

        assert expected == get_dbt_project_path(absolute_path)
