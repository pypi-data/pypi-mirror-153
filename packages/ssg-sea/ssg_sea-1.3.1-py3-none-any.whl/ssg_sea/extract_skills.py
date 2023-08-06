# module doc string
"""
This module extracts skills from free text and output them in accordance to SST skill terms
author: - Lois Ji
        - Leo Li
date: Mar 1, 2022
"""
import pickle
import yaml
from ssg_sea.utils import *
from ssg_sea.config.core import CONFIG_FILE_PATH, PICKLE_FILE_PATH

from flashtext import KeywordProcessor

params = yaml.safe_load(open(CONFIG_FILE_PATH))
pickle_input = PICKLE_FILE_PATH

# Load data artefacts
file = open(pickle_input, 'rb')
stem_flashtext_dict = pickle.load(file)
stemsDict = pickle.load(file)
context_flashtext_dict = pickle.load(file)
contextsDict = pickle.load(file)
stemToSkillDict = pickle.load(file)
skillToContextDict = pickle.load(file)
skillSetIndptContext = pickle.load(file)
ccs_flashtext_dict = pickle.load(file)
app_tool_flashtext_dict = pickle.load(file)
file.close()

# Load KeywordProcessors
context_keyword_processor = KeywordProcessor()
context_keyword_processor.add_keywords_from_dict(context_flashtext_dict)
stem_keyword_processor = KeywordProcessor()
stem_keyword_processor.add_keywords_from_dict(stem_flashtext_dict)
app_keyword_processor = KeywordProcessor()
app_keyword_processor.add_keywords_from_dict(app_tool_flashtext_dict)
ccs_keyword_processor = KeywordProcessor()
ccs_keyword_processor.add_keywords_from_dict(ccs_flashtext_dict)


def extract_skills(text):
    """
    output the extraction results of the skills extraction algorithm
    :param text: input text for skills extraction
    :return:
        output_list: list of skills with weight and tpye
    """
    context_list = extractionFrTxt(text, flashProcessor=context_keyword_processor,
                                   usedDict=contextsDict)
    stem_list = extractionFrTxt(text, flashProcessor=stem_keyword_processor,
                                usedDict=stemsDict)
    app_word_list = extractionFrTxt(text, flashProcessor=app_keyword_processor,
                                    usedDict="noDict")
    ccs_word_list = extractionFrTxt(text, flashProcessor=ccs_keyword_processor,
                                    usedDict="noDict")

    tsc_list = extractTSC(context_list=context_list, stem_list=stem_list,
                          skill_to_context_dict=skillToContextDict, stem_to_skill_dict=stemToSkillDict,
                          skill_indpt_context_set=skillSetIndptContext)
    app_list = extractAPP(app_word_list)
    ccs_list = extractCCS(ccs_word_list)

    tsc_output = getSkillWeight(skillExtractionList=tsc_list, skillForm="TSC")
    app_output = getSkillWeight(skillExtractionList=app_list, skillForm="App/Tools")
    ccs_output = getSkillWeight(skillExtractionList=ccs_list, skillForm="CCS")

    output_list = tsc_output + app_output + ccs_output

    results = {}
    _list = []
    keys = range(len(output_list))

    for tuple in output_list:
        extractDict = {
            "skill name": tuple[0],
            "skill weight": tuple[1],
            "skill form": tuple[2]
        }
        _list.append(extractDict)

    for i in keys:
        results[i] = _list[i]

    if len(results) == 0:
        output = {}
    else:
        output = {
            "extractions": results
        }

    return output
