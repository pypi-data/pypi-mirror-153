# library doc string
"""
This is a library of functions and classes for the skills extraction algorithm.
author: - Lois Ji
        - Leo Li
date: Feb 28, 2022
"""

import pandas as pd
import numpy as np


def df_to_dict(branchCol, leafCol):
    """
    convert dataframe to dictionary
    :param branchCol: branch column from the dataframe
    :param leafCol: leaf column from the dataframe
    :return: Dict: output dictionary with branch column values as key and leaf column values as value
    """
    Dict = {}
    for abranch, aleaf in zip(branchCol, leafCol):
        if abranch not in Dict:
            Dict[abranch] = []
            Dict[abranch] += [aleaf]
        else:
            Dict[abranch] += [aleaf]
    return Dict


def searchValListForKey(astring, Dict):
    """
    return list of skills keys using a search string

    :param astring: the search string
    :param Dict: dictionary object
    :return: skillList: list of keys of the skills based on the value of the dictionary
    """
    skillList = [k.lower() for k, v in Dict.items() if astring.lower() in v]
    return skillList


# Extract the skills, accounting for the number of times they appeared in the text
def extractionFrTxt(text, flashProcessor, usedDict="noDict"):
    """
    extract list of skills/apps&tools from dictionaries with fuzzy-matching processors
    :param text: text for the extraction
    :param flashProcessor: keyword-matching processors with word boundary conditions
    :param usedDict: dictionary for extraction
    :return:
        extracts: list of skills from the extraction
    """
    extracts = []

    if usedDict != "noDict":
        for abranch, aleaf in usedDict.items():
            for leaf in aleaf:
                if leaf in str(text).lower():
                    leafFreq = str(text).lower().count(leaf)
                    extracts += [abranch] * leafFreq
                else:
                    pass

        flashRes = flashProcessor.extract_keywords(text.lower())
        for askill in flashRes:
            skillFreq = flashRes.count(askill)
            extracts += [askill] * skillFreq
    else:
        flashRes = flashProcessor.extract_keywords(text.lower())
        for askill in flashRes:
            skillFreq = flashRes.count(askill)
            extracts += [askill] * skillFreq

    return extracts


def getSkillWeight(skillExtractionList, skillForm):
    """
    output skills weight and skills form from the extracted skills list
    :param skillExtractionList: list of the skills from the skills extraction process
    :param skillForm: type of skills; TSC or Apps and Tools or CCS
    :return:
        output_list: list of skills output with weight and skills form
    """
    skillList = []
    skillWeightList = []

    skillFreqDict = {}
    for askill in skillExtractionList:
        freq = askill.count(askill)
        if askill not in skillFreqDict:
            skillFreqDict[askill] = int()
        skillFreqDict[askill] += freq
    odict = dict(sorted(skillFreqDict.items(), key=lambda item: item[1], reverse=True))
    for askill, afreq in odict.items():
        wtAvg = sum(odict.values()) / len(odict)
        aWeight = np.round(((odict[askill]) / wtAvg), 3)

        skillList += [askill]
        skillWeightList += [aWeight]

    output_list = []
    for i in range(len(skillList)):
        output_with_weight = (skillList[i], skillWeightList[i], skillForm)
        output_list.append(output_with_weight)

    return output_list


def extractTSC(context_list, stem_list, skill_to_context_dict, stem_to_skill_dict, skill_indpt_context_set):
    """
    output a list of tsc skills from the contexts and stems
    :param context_list: context list of the context extraction
    :param stem_list: stem list of the stem extraction
    :param skill_to_context_dict: dictionary for skills to context matching
    :param stem_to_skill_dict: dictionary for stem to skill matching
    :param skill_indpt_context_set: independent skill set
    :return:
        skillExtracts: list of the skills according to tsc skill titles
    """
    skillExtracts = []
    uniqueSkillCnts = []

    skillListFrContext = []
    for context in context_list:
        skillListFrContext.extend(searchValListForKey(context, skill_to_context_dict))
    skillListFrStem = []
    if len(stem_list) == 0:
        pass
    else:
        for stem in stem_list:
            skillListFrStem_skills = list(stem_to_skill_dict.get(stem))
            skillListFrStem.extend(skillListFrStem_skills)
    setFrContext = set(skillListFrContext)
    setFrStem = set(skillListFrStem)
    resultSet = set.union(setFrContext.intersection(setFrStem), setFrContext.intersection(skill_indpt_context_set))
    nbrUniqueSkillsExtracted = len(resultSet)

    for askill in list(resultSet):
        skillFreqContext = skillListFrContext.count(askill)
        skillFreqStem = skillListFrStem.count(askill)
        resultantSkillFreq = max(skillFreqContext, skillFreqStem)

        skillExtracts += [askill] * resultantSkillFreq
        uniqueSkillCnts += [nbrUniqueSkillsExtracted] * resultantSkillFreq

    return skillExtracts


def extractAPP(app_list):
    """
    getting extracted apps/tools with frequency count
    :param app_list: list of apps/tools extracted from the keyword matching
    :return:
        skillExtracts: list of the skills according to apps/tools skill master list
    """
    # Getting extracted apps/tools with frequency count
    skillExtracts = []
    uniqueSkillCnts = []

    nbrUniqueAppsExtracted = len(set(app_list))

    for app in list(set(app_list)):
        skillFreqApp = app_list.count(app)
        skillExtracts += [app] * skillFreqApp
        uniqueSkillCnts += [nbrUniqueAppsExtracted] * skillFreqApp

    return skillExtracts


def extractCCS(ccs_list):
    """
    getting extracted ccs with frequency count
    :param ccs_list: list of ccs extracted from the keyword matching
    :return:
        skillExtracts: list of the skills according to ccs skill master list
    """
    # Getting extracted ccs with frequency count
    skillExtracts = []
    uniqueSkillCnts = []

    nbrUniqueCCSExtracted = len(set(ccs_list))

    for ccs in list(set(ccs_list)):
        skillFreqCCS = ccs_list.count(ccs)
        skillExtracts += [ccs] * skillFreqCCS
        uniqueSkillCnts += [nbrUniqueCCSExtracted] * skillFreqCCS

    return skillExtracts
