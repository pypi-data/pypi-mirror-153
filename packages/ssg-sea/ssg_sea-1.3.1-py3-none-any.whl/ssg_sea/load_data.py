# module doc string
"""
This module extract skills meta tables from the database and output to the data folder for processing.
author: - Lois Ji
        - Leo Li
date: Feb 28, 2022
"""

from sqlalchemy import create_engine
import pandas as pd
import yaml

# Load all the parameters
params = yaml.safe_load(open("params.yaml"))
database_filepath = params["load_data"]["database_filepath"]
short_alias_skill_context_table_output = params["load_data"]["short_alias_skill_context_table_output"]
short_alias_skill_stem_table_output = params["load_data"]["short_alias_skill_stem_table_output"]
stem_alias_table_output = params["load_data"]["stem_alias_table_output"]
context_alias_table_output = params["load_data"]["context_alias_table_output"]
stem_to_skill_mapping_table_output = params["load_data"]["stem_to_skill_mapping_table_output"]
skill_to_context_mapping_table_output = params["load_data"]["skill_to_context_mapping_table_output"]
context_indept_skill_table_output = params["load_data"]["context_indept_skill_table_output"]
ccs_skill_table_output = params["load_data"]["ccs_skill_table_output"]
app_skill_table_output = params["load_data"]["app_skill_table_output"]

# Create engine to connect the database
engine = create_engine('sqlite:///' + database_filepath)


def get_short_alias_skill_context():
    """
    extract a dataframe of skills ids of contexts with short alias, where len(alias) <= 4
    :return:
        short_alias_skill_context_table: short alias for contexts dataframe
    """
    short_alias_skill_context_table = pd.read_sql("""
    SELECT DISTINCT(cm.skill_component_id) 
    FROM skill_context_mapping cm
    LEFT JOIN skill_component_alias ca
    ON cm.skill_component_id = ca.skill_component_id
    WHERE cm.skill_id IN (
    SELECT md.skill_id 
    FROM skill_master_dedup md 
    WHERE skill_source = 'SFw TSC' 
    AND duplicated = 0)
    AND LENGTH(ca.skill_component_alias) <= 4;
    """, engine)
    return short_alias_skill_context_table


def get_short_alias_skill_stem():
    """
    extract a dataframe of skills ids of stems with short alias, where len(alias) <= 4
    :return:
        short_alias_skill_stem_table: component ids of stems with short aliases dataframe
    """
    short_alias_skill_stem_table = pd.read_sql("""
    SELECT DISTINCT(sm.skill_component_id) 
    FROM skill_stem_mapping sm
    LEFT JOIN skill_component_alias ca
    ON sm.skill_component_id = ca.skill_component_id
    WHERE sm.skill_id IN (
    SELECT md.skill_id 
    FROM skill_master_dedup md 
    WHERE skill_source = 'SFw TSC' 
    AND duplicated = 0)
    AND LENGTH(ca.skill_component_alias) <= 4;
    """, engine)
    return short_alias_skill_stem_table


def get_stem_alias_table():
    """
    extract a dataframe of the stem alias
    :return:
        stem_alias_table: stem alias dataframe
    """
    stem_alias_table = pd.read_sql("""
    SELECT DISTINCT sm.skill_component_id, sm.skill_component_stem, ca.skill_component_alias 
    FROM skill_component_alias ca 
    LEFT JOIN skill_stem_mapping sm 
    ON sm.skill_component_id = ca.skill_component_id
    WHERE sm.skill_id IN (
    SELECT md.skill_id 
    FROM skill_master_dedup md 
    WHERE md.skill_source = 'SFw TSC' 
    AND duplicated = 0);
    """, engine)
    return stem_alias_table


def get_context_alias_table():
    """
    extract a dataframe of the context alias
    :return:
        context_alias_table: context alias dataframe
    """
    context_alias_table = pd.read_sql("""
    SELECT DISTINCT cm.skill_component_id, cm.skill_component_context, ca.skill_component_alias 
    FROM skill_component_alias ca 
    LEFT JOIN skill_context_mapping cm 
    ON cm.skill_component_id = ca.skill_component_id
    WHERE cm.skill_id IN (
    SELECT md.skill_id 
    FROM skill_master_dedup md 
    WHERE md.skill_source = 'SFw TSC' 
    AND duplicated = 0);
    """, engine)
    return context_alias_table


def get_stem_to_skill_mapping_table():
    """
    extract the stem to skills mapping table, only for SFw TSCs
    :return:
        stem_to_skill_mapping_table: stem-skills mapping dataframe
    """
    stem_to_skill_mapping_table = pd.read_sql("""
    SELECT sm.skill_component_stem, md.skill_title, md.duplicated 
    FROM skill_stem_mapping sm 
    LEFT JOIN skill_master_dedup md 
    ON sm.skill_id = md.skill_id 
    WHERE skill_component_stem != "NA"
    AND md.skill_source = 'SFw TSC';
    """, engine)
    return stem_to_skill_mapping_table


def get_skill_to_context_mapping_table():
    """
    extract the skills to context mapping table, only for SFw TSCs
    :return:
        skill_to_context_mapping_table: skills-context mapping dataframe
    """
    skill_to_context_mapping_table = pd.read_sql("""
    SELECT cm.skill_component_context, md.skill_title, md.duplicated 
    FROM skill_context_mapping cm 
    LEFT JOIN skill_master_dedup md 
    ON cm.skill_id = md.skill_id 
    WHERE md.skill_source = 'SFw TSC';
    """, engine)
    return skill_to_context_mapping_table


def get_context_indept_skill_table():
    """
    extract the context independent skills table, only for SFw TSCs
    :return:
        context_indept_skill_table: dataframe of the context independent skills
    """
    context_indept_skill_table = pd.read_sql("""
    SELECT DISTINCT(md.skill_title)
    FROM skill_context_mapping cm 
    LEFT JOIN skill_master_dedup md 
    ON cm.skill_id = md.skill_id 
    WHERE md.skill_source = 'SFw TSC' 
    AND cm.context_indept = 1;
    """, engine)
    return context_indept_skill_table


def get_ccs_skill_table():
    """
    extract the SFw CCS skills leaf-branch dictionary from master_dedup, context_mapping, component_alias tables
    :return:
        ccs_skill_table: dataframe of ccs skills and their aliases
    """
    ccs_skill_table = pd.read_sql("""
    SELECT md.skill_title, ca.skill_component_alias
    FROM skill_master_dedup md
    LEFT JOIN skill_context_mapping cm
    ON cm.skill_id = md.skill_id
    LEFT JOIN skill_component_alias ca
    ON ca.skill_component_id = cm.skill_component_id
    WHERE md.skill_source = 'SFw CCS'; 
    """, engine)
    return ccs_skill_table


def get_app_skill_table():
    """
    extract the Apps and Tools leaf-branch dictionary from master_dedup, context_mapping, component_alias tables
    :return:
        app_skill_table: dataframe of apps and tools and their aliases
    """
    app_skill_table = pd.read_sql("""
    SELECT md.skill_title, ca.skill_component_alias
    FROM skill_master_dedup md
    LEFT JOIN skill_context_mapping cm
    ON cm.skill_id = md.skill_id
    LEFT JOIN skill_component_alias ca
    ON ca.skill_component_id = cm.skill_component_id
    WHERE md.skill_source = 'Apps and Tools';
    """, engine)
    return app_skill_table


def main():
    """
    Extract data artefacts from the database and save them to the output location
    :return: None
    """
    # extract tables from the database
    short_alias_skill_context_table = get_short_alias_skill_context()
    short_alias_skill_stem_table = get_short_alias_skill_stem()
    stem_alias_table = get_stem_alias_table()
    context_alias_table = get_context_alias_table()
    stem_to_skill_mapping_table = get_stem_to_skill_mapping_table()
    skill_to_context_mapping_table = get_skill_to_context_mapping_table()
    context_indept_skill_table = get_context_indept_skill_table()
    ccs_skill_table = get_ccs_skill_table()
    app_skill_table = get_app_skill_table()

    # save the tables to the data folder
    short_alias_skill_context_table.to_csv(short_alias_skill_context_table_output, index=False)
    short_alias_skill_stem_table.to_csv(short_alias_skill_stem_table_output, index=False)
    stem_alias_table.to_csv(stem_alias_table_output, index=False)
    context_alias_table.to_csv(context_alias_table_output, index=False)
    stem_to_skill_mapping_table.to_csv(stem_to_skill_mapping_table_output, index=False)
    skill_to_context_mapping_table.to_csv(skill_to_context_mapping_table_output, index=False)
    context_indept_skill_table.to_csv(context_indept_skill_table_output, index=False)
    ccs_skill_table.to_csv(ccs_skill_table_output, index=False)
    app_skill_table.to_csv(app_skill_table_output, index=False)


if __name__ == '__main__':
    main()
