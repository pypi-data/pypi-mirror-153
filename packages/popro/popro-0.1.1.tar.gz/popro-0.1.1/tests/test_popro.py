#!/usr/bin/env python

"""Tests for `popro` package."""

import csv
import os
import shutil
from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from popro import cli, engines, popro

# from popro import cli, engines, popro

def create_data_folder():

    delete_data_folder()
    folder_path = os.path.join('tests', 'data')
    Path(folder_path).mkdir(exist_ok=True)


def delete_data_folder():

    folder_path = os.path.join('tests', 'data')
    shutil.rmtree(folder_path, ignore_errors=True)

def write_csv(file_path, list_data):
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for line in list_data:
            writer.writerow(line)
class Test_popro_class:
    def test_input_file_not_found(self):
        create_data_folder()

        data_census = [['age', 'population', 'place', 'year'],
                       [0, 100,  'ny', 2010],
                       [1, 110,  'ny', 2010],
                       [2, 105,  'ny', 2010],
                       [3, 102,  'ny', 2010]]
        path_census = os.path.join('tests', 'data', 'census.csv')
        write_csv(path_census, data_census)

        data_births = [['births', 'place', 'year'],
                       [102,'ny',2011],
                       [116,'ny',2012],
                       [94,'ny',2013],
                       [123,'ny',2014],
                       [156,'ny',2015]]
        path_births = os.path.join('tests', 'data', 'births.csv')
        write_csv(path_births, data_births)

        data_population = [['population', 'place', 'year'],
                           [2031, 'ny', 2010],
                           [2100, 'ny', 2011],
                           [2050, 'ny', 2012],
                           [2040, 'ny', 2013],
                           [2090, 'ny', 2014],
                           [1950, 'ny', 2015]]
        path_population = os.path.join('tests', 'data', 'population.csv')
        write_csv(path_population, data_population)

        with pytest.raises(FileNotFoundError):
            input_file_name = ['censusx.csv', 'births.csv', 'population.csv']
            input_files = [os.path.join('tests', 'data', file)
                           for file in input_file_name]
            dict_input = {'path_census': input_files[0],
                          'path_births': input_files[1],
                          'path_population': input_files[2],
                          'year_census': 2010}
            popro.Popro(dict_input)

        with pytest.raises(FileNotFoundError):
            input_file_name = ['census.csv', 'birthsx.csv', 'population.csv']
            input_files = [os.path.join('tests', 'data', file)
                           for file in input_file_name]
            dict_input = {'path_census': input_files[0],
                          'path_births': input_files[1],
                          'path_population': input_files[2],
                          'year_census': 2010}
            popro.Popro(dict_input)


        with pytest.raises(FileNotFoundError):
            input_file_name = ['census.csv', 'births.csv', 'populationx.csv']
            input_files = [os.path.join('tests', 'data', file)
                           for file in input_file_name]
            dict_input = {'path_census': input_files[0],
                          'path_births': input_files[1],
                          'path_population': input_files[2],
                          'year_census': 2010}
            popro.Popro(dict_input)
        delete_data_folder()

    def test_input_file_empty(self):

        create_data_folder()
        files = ['census.csv', 'births.csv', 'population.csv']
        for file in files:
            open(os.path.join('tests', 'data', file), 'w').close()

        input_file_name = ['census.csv', 'births.csv', 'population.csv']
        input_files = [os.path.join('tests', 'data', file)
                        for file in input_file_name]
        dict_input = {'path_census': input_files[0],
                      'path_births': input_files[1],
                      'path_population': input_files[2],
                      'year_census': 2010}
        with pytest.raises(pd.errors.EmptyDataError):
            popro.Popro(dict_input)

        delete_data_folder()

    def test_input_file_wrong_extension(self):

        # wrong input census file
        create_data_folder()
        files = ['census.xlsx', 'births.csv', 'population.csv']
        for file in files:
            open(os.path.join('tests', 'data', file), 'w').close()
        input_file_name = ['census.xlsx', 'births.csv', 'population.csv']
        input_files = [os.path.join('tests', 'data', file)
                       for file in input_file_name]
        with pytest.raises(TypeError):
            popro.Popro(path_census=input_files[0],
                        path_births=input_files[1],
                        path_population=input_files[2],
                        year_census=2010)
        delete_data_folder()

        # wrong input births file
        create_data_folder()
        files = ['census.csv', 'births.xlsx', 'population.csv']
        for file in files:
            open(os.path.join('tests', 'data', file), 'w').close()
        input_file_name = ['census.csv', 'births.xlsx', 'population.csv']
        input_files = [os.path.join('tests', 'data', file)
                       for file in input_file_name]
        with pytest.raises(TypeError):
            popro.Popro(path_census=input_files[0],
                        path_births=input_files[1],
                        path_population=input_files[2],
                        year_census=2010)
        delete_data_folder()

        # wrong input population file
        create_data_folder()
        files = ['census.csv', 'births.csv', 'population.xlsx']
        for file in files:
            open(os.path.join('tests', 'data', file), 'w').close()
        input_file_name = ['census.csv', 'births.csv', 'population.xlsx']
        input_files = [os.path.join('tests', 'data', file)
                       for file in input_file_name]
        with pytest.raises(TypeError):
            popro.Popro(path_census=input_files[0],
                        path_births=input_files[1],
                        path_population=input_files[2],
                        year_census=2010)
        delete_data_folder()

class Test_get_project_engine:
    def test_via_births_2019_8(self):

        project_engine = engines.tceduca.get_projection_engine(
            year=2019, age=8, year_census=2010
        )
        assert project_engine == engines.tceduca.via_births

    def test_via_census_2019_9(self):

        project_engine = engines.tceduca.get_projection_engine(
            year=2019, age=9, year_census=2010
        )
        assert project_engine == engines.tceduca.via_census

    def test_via_census_2019_10(self):

        project_engine = engines.tceduca.get_projection_engine(
            year=2019, age=10, year_census=2010
        )
        assert project_engine == engines.tceduca.via_census

    def test_year_census_smaller_than_year(self):

        with pytest.raises(ValueError):
            engines.tceduca.get_projection_engine(year=2009, age=10, year_census=2010)

    def test_age_smaller_than_0(self):

        with pytest.raises(ValueError):
            engines.tceduca.get_projection_engine(year=2019, age=-1, year_census=2010)

    def test_age_equal_0(self):

        try:
            engines.tceduca.get_projection_engine(year=2019, age=0, year_census=2010)
        except ValueError:
            raise pytest.fail("Raise {0}".format(ValueError))


class Test_dataset:

    def test_dataset_census_columns_ok(self):
        df_census = pd.DataFrame(data=[[0, 100, 1100015, 2010],
                                       [1, 200, 1100015, 2010]],
                                 columns=["age", "population", "place", "year"]
                                 )
        try:
            engines.tceduca.validate_dataset_census(df_census)
        except ValueError:
            raise pytest.fail("Raise {0}".format(ValueError))

    def test_dataset_census_columns_fail(self):
        df_census = pd.DataFrame(data=[[0, 100, 1100015, 2010],
                                       [1, 200, 1100015, 2010]],
                                 columns=["age", "population", "local", "year"]
                                 )
        with pytest.raises(ValueError):
            engines.tceduca.validate_dataset_census(df_census)

    def test_dataset_births_columns_ok(self):
        df_births = pd.DataFrame(data=[[2011, 1100015, 128],
                                       [2012, 1100015, 141]],
                                 columns=['year', 'place', 'births']
                                 )
        try:
            engines.tceduca.validate_dataset_births(df_births)
        except ValueError:
            raise pytest.fail("Raise {0}".format(ValueError))

    def test_dataset_births_columns_fail(self):
        df_births = pd.DataFrame(data=[[2011, 1100015, 128],
                                       [2012, 1100015, 141]],
                                 columns=['year', 'place', 'born']
                                 )
        with pytest.raises(ValueError):
            engines.tceduca.validate_dataset_births(df_births)

    def test_dataset_population_columns_ok(self):
        df_population = pd.DataFrame(data=[[2011, 1100015, 2939],
                                           [2012, 1100015, 2897]],
                                     columns=['year', 'place', 'population']
                                    )
        try:
            engines.tceduca.validate_dataset_population(df_population)
        except ValueError:
            raise pytest.fail("Raise {0}".format(ValueError))

    def test_dataset_population_columns_fail(self):
        df_population = pd.DataFrame(data=[[2011, 1100015, 2939],
                                           [2012, 1100015, 2897]],
                                     columns=['year', 'place', 'peoples']
                                    )
        with pytest.raises(ValueError):
            engines.tceduca.validate_dataset_population(df_population)

class Test_get_pop_place_census_age:
    def test_none_register_found(self):
        list_dict = [
            {
                "age": 0,
                "population": 100,
                "place": 1100015,
                "year": 2010,
            },
            {
                "age": 1,
                "population": 200,
                "place": 1100015,
                "year": 2010,
            },
            {
                "age": 2,
                "population": 150,
                "place": 1100015,
                "year": 2010,
            },
        ]
        df_census = pd.DataFrame(list_dict)
        with pytest.raises(ValueError):
            engines.tceduca.get_pop_place_census_age(
                df_census=df_census, place=1100015, age=3
            )

    def test_one_register_found(self):

        # fmt: off
        list_df = [
            {"age": 0, "population": 100, "place": 1100015, "year": 2010},
            {"age": 1, "population": 200, "place": 1100015, "year": 2010},
            {"age": 2, "population": 150, "place": 1100015, "year": 2010}
            ]
        df_census = pd.DataFrame(list_df)
        qtd=engines.tceduca.get_pop_place_census_age(df_census=df_census, place=1100015,age=2)
        assert qtd == 150

    def test_multiple_register_found(self):

        # fmt: off
        list_df = [
            {"age": 0, "population": 100, "place": 1100015, "year": 2010},
            {"age": 2, "population": 200, "place": 1100015, "year": 2010},
            {"age": 2, "population": 150, "place": 1100015, "year": 2010}
            ]
        df_census = pd.DataFrame(list_df)
        with pytest.raises(ValueError):
            engines.tceduca.get_pop_place_census_age(df_census=df_census, place=1100015,age=2)

        # def test_command_line_interface():
        #     """Test the CLI."""
        #     runner = CliRunner()
        #     result = runner.invoke(cli.main)
        #     # assert result.exit_code == 0
        #     assert "popro.cli.main" in result.output
        #     help_result = runner.invoke(cli.main, ["--help"])
        #     assert help_result.exit_code == 0
        #     assert "--help  Show this message and exit." in help_result.output
