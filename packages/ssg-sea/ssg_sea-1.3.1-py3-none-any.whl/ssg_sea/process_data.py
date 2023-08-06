# module doc string
"""
This module process the data to prepare for the skills extraction algorithm.
author: - Lois Ji
        - Leo Li
date: Feb 28, 2022
"""

import pandas as pd
import yaml
import pickle

from utils import df_to_dict

params = yaml.safe_load(open("params.yaml"))
short_alias_skill_context_table_output = params["load_data"]["short_alias_skill_context_table_output"]
short_alias_skill_stem_table_output = params["load_data"]["short_alias_skill_stem_table_output"]
stem_alias_table_output = params["load_data"]["stem_alias_table_output"]
context_alias_table_output = params["load_data"]["context_alias_table_output"]
stem_to_skill_mapping_table_output = params["load_data"]["stem_to_skill_mapping_table_output"]
skill_to_context_mapping_table_output = params["load_data"]["skill_to_context_mapping_table_output"]
context_indept_skill_table_output = params["load_data"]["context_indept_skill_table_output"]
ccs_skill_table_output = params["load_data"]["ccs_skill_table_output"]
app_skill_table_output = params["load_data"]["app_skill_table_output"]
pickle_output = params["process_data"]["pickle_output"]


def create_stem_dic(short_alias_path=short_alias_skill_stem_table_output,
                    stem_alias_table_path=stem_alias_table_output):
    """
    function to create dictionaries for skills stems, with both short and long aliases
    :param short_alias_path: data path of the short alias table
    :param stem_alias_table_path: data path of the stem alias table
    :return:
        stem_flashtext_dict: stem dictionary for keywords-matching with word boundary conditions
        stemsDict: stem dictionary with fuzzy-matching logic
    """
    get_short_alias_skill = pd.read_csv(short_alias_path)
    stem_alias = pd.read_csv(stem_alias_table_path)
    stem_alias_short = stem_alias.copy()
    stem_alias_short = stem_alias_short[
        stem_alias_short.skill_component_id.isin(list(get_short_alias_skill.skill_component_id))]
    stem_flashtext_dict = df_to_dict(stem_alias_short.skill_component_stem, stem_alias_short.skill_component_alias)
    stem_alias_long = stem_alias.copy()
    stem_alias_long = stem_alias_long[
        ~stem_alias_long.skill_component_id.isin(list(get_short_alias_skill.skill_component_id))]
    stemsDict = df_to_dict(stem_alias_long.skill_component_stem, stem_alias_long.skill_component_alias)

    return stem_flashtext_dict, stemsDict


def create_context_dic(context_alias_path=context_alias_table_output,
                       short_alias_path=short_alias_skill_context_table_output):
    """
    function to create dictionaries for skills context, with both short and long aliases
    :param context_alias_path: data path of the context alias table
    :param short_alias_path: data path of the short alias table
    :return:
        context_flashtext_dict: context dictionary for keywords-matching with word boundary conditions
        contextsDict: context dictionary with fuzzy-matching logic
    """
    context_alias = pd.read_csv(context_alias_path)
    get_short_alias_skill = pd.read_csv(short_alias_path)
    context_alias_short = context_alias.copy()
    context_alias_short = context_alias_short[
        context_alias_short.skill_component_id.isin(list(get_short_alias_skill.skill_component_id))]
    context_flashtext_dict = df_to_dict(context_alias_short.skill_component_context,
                                        context_alias_short.skill_component_alias)
    context_alias_long = context_alias.copy()
    context_alias_long = context_alias_long[
        ~context_alias_long.skill_component_id.isin(list(get_short_alias_skill.skill_component_id))]
    contextsDict = df_to_dict(context_alias_long.skill_component_context, context_alias_long.skill_component_alias)

    return context_flashtext_dict, contextsDict


def create_stem_to_skill_dic(stem_to_skill_path=stem_to_skill_mapping_table_output):
    """
    function to create stem-to-skill dictionary
    :param stem_to_skill_path: data path to the stem to skills mapping table
    :return:
        stemToSkillDict: stem-to-skill dictionary
    """
    stem_to_skill_mapping = pd.read_csv(stem_to_skill_path)
    stemToSkillDict = df_to_dict(stem_to_skill_mapping.skill_component_stem, stem_to_skill_mapping.skill_title)

    return stemToSkillDict


def create_skill_to_context_dic(skill_to_context_path=skill_to_context_mapping_table_output):
    """
    function to create skill-to-context dictionary
    :param skill_to_context_path: data path to the skill to context mapping table
    :return:
        skillToContextDict: skill-to-context dictionary
    """
    skill_to_context_mapping = pd.read_csv(skill_to_context_path)
    skillToContextDict = df_to_dict(skill_to_context_mapping.skill_title,
                                    skill_to_context_mapping.skill_component_context)
    return skillToContextDict


def create_context_indept_skill(context_indept_skill_path=context_indept_skill_table_output):
    """
    function to create context independent skills set
    :param context_indept_skill_path:
    :return:
        skillSetIndptContext: context independent skills set
    """
    context_indept_skill = pd.read_csv(context_indept_skill_path)
    skillSetIndptContext = set(context_indept_skill.skill_title)

    return skillSetIndptContext


def create_ccs_skill_dic(ccs_skill_path=ccs_skill_table_output):
    """
    function to create ccs skills dictionary
    :param ccs_skill_path: data path to the ccs skills alias table
    :return:
        ccs_flashtext_dict: ccs skills alias dictionary for flashtext extraction
    """
    ccs_skill = pd.read_csv(ccs_skill_path)
    ccs_flashtext_dict = df_to_dict(ccs_skill.skill_title, ccs_skill.skill_component_alias)
    return ccs_flashtext_dict


def create_app_tool_dic(app_tool_path=app_skill_table_output):
    """
    function to create apps and tools dictionary
    :param app_tool_path: data path to the apps and tools skills alias table
    :return:
        app_tool_flashtext_dict: apps and tools alias dictionary for flashtext extraction
    """
    app_tool = pd.read_csv(app_tool_path)
    app_tool_flashtext_dict = df_to_dict(app_tool.skill_title, app_tool.skill_component_alias)
    return app_tool_flashtext_dict


def main(pickle_path=pickle_output):
    """
    function to execute dictionary/set creations, save as a pickle dump
    :param pickle_path: output path of the pickle dump
    :return: None
    """
    stem_flashtext_dict, stemsDict = create_stem_dic()
    context_flashtext_dict, contextsDict = create_context_dic()
    ccs_flashtext_dict = create_ccs_skill_dic()
    app_tool_flashtext_dict = create_app_tool_dic()
    stemToSkillDict = create_stem_to_skill_dic()
    skillToContextDict = create_skill_to_context_dic()
    skillSetIndptContext = create_context_indept_skill()

    dict_list = [stem_flashtext_dict, stemsDict, context_flashtext_dict, contextsDict,
                 stemToSkillDict, skillToContextDict, skillSetIndptContext,
                 ccs_flashtext_dict, app_tool_flashtext_dict]

    file = open(pickle_path, 'wb')
    for dict in dict_list:
        pickle.dump(dict, file)
    file.close()


if __name__ == '__main__':
    main()
