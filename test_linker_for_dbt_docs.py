from linker_for_dbt_docs import make_link


class TestMakeLink:
    def test_it_takes_a_project_name_and_model_with_dot_and_makes_link(self):
        project_name = 'star_fish'
        model_name = 'dim.problem_barnacles'
        expected = '<a href="#!/model/model.star_fish.dim_problem_barnacles">dim.problem_barnacles</a>'
        assert expected == make_link(project_name, model_name)

    def test_it_takes_a_project_name_and_model_with_underscore_and_makes_link(self):
        project_name = 'star_fish'
        model_name = 'dim_problem_barnacles'
        expected = '<a href="#!/model/model.star_fish.dim_problem_barnacles">dim.problem_barnacles</a>'
        assert expected == make_link(project_name, model_name)
