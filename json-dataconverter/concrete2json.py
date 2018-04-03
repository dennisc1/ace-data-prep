import json
import optparse
import sys

import os
import re
from concrete.inspect import get_tokenizations, get_lemma_tags_for_tokenization, get_pos_tags_for_tokenization, \
    get_tokentaggings_of_type, \
    get_conll_head_tags_for_tokenization, penn_treebank_for_parse, get_ner_tags_for_tokenization
from concrete.util import read_communication_from_file

header_fields = [u"words", u"lemma", u"pos-tags", u"stanford-ner", u"chunk", u"conll-head"]


def get_token_indices_for_entityMention(entityMention):
    token_indices = []
    for tokenIndex in entityMention.tokens.tokenIndexList:
        token_indices.append(tokenIndex)
    return token_indices


def find_which_sentence(tokenization, comm):
    for i, sentence in zip(range(len(get_tokenizations(comm))), get_tokenizations(comm)):
        if tokenization == sentence:
            return i
    return -1


def get_chunk_tags_for_tokenization(tokenization, chunk_tokentagging_index=0):
    if tokenization.tokenList:
        chunk_tags = [""] * len(tokenization.tokenList.tokenList)
        chunk_tokentaggings = get_tokentaggings_of_type(tokenization, u"CHUNK")
        if chunk_tokentaggings and len(chunk_tokentaggings) > chunk_tokentagging_index:
            tag_for_tokenIndex = {}
            for taggedToken in chunk_tokentaggings[chunk_tokentagging_index].taggedTokenList:
                tag_for_tokenIndex[taggedToken.tokenIndex] = taggedToken.tag
            for i, token in enumerate(tokenization.tokenList.tokenList):
                if i in tag_for_tokenIndex:
                    chunk_tags[i] = tag_for_tokenIndex[i]
        return chunk_tags


def get_penn_treebank_for_tokenization(tokenization):
    if tokenization.parseList:
        for parse in tokenization.parseList:
            return (penn_treebank_for_parse(parse) + u"\n\n").replace("\n", "")


def get_tokens_for_entityMention(entityMention):
    """Get list of token strings for an EntityMention

    Args:

    - `entityMention`: A Concrete EntityMention argument

    Returns:

    - A list of token strings
    """
    tokens = []
    for tokenIndex in entityMention.tokens.tokenIndexList:
        tokens.append(entityMention.tokens.tokenization.tokenList.tokenList[tokenIndex].text)
    return tokens


def comm2json(comm):
    js = []

    # sentence-level
    for i, tokenization in zip(range(len(get_tokenizations(comm))), get_tokenizations(comm)):
        js.append({})
        for header in header_fields:
            tag_lists = []
            if header == u"words":
                tag_lists = [token.text for token in tokenization.tokenList.tokenList]
            elif header == u"lemma":
                tag_lists = get_lemma_tags_for_tokenization(tokenization)
            elif header == u"pos-tags":
                tag_lists = get_pos_tags_for_tokenization(tokenization)
            elif header == u"chunk":
                tag_lists = get_chunk_tags_for_tokenization(tokenization)
            elif header == u"conll-head":
                tag_lists = get_conll_head_tags_for_tokenization(tokenization)
            elif header == u"stanford-ner":
                tag_lists = get_ner_tags_for_tokenization(tokenization)
            js[i][header] = tag_lists

        js[i][u"penn-treebank"] = re.sub(r'\s+', ' ', get_penn_treebank_for_tokenization(tokenization))
        js[i][u"golden-entity-mentions"] = []
        js[i][u"golden-event-mentions"] = []

    # entities
    if comm.entitySetList:
        entitySet_index = -1
        for i, entitySet in enumerate(comm.entitySetList):
            if entitySet.metadata.tool.startswith("Pacaya"):
                entitySet_index = i
        entitySet = comm.entitySetList[entitySet_index]

        for entity_index, entity in enumerate(entitySet.entityList):
            entity_id = u"E%d-%d:" % (entitySet_index, entity_index)
            for entityMention_index, entityMention in enumerate(entity.mentionList):
                entitymention_id = "EM %d-%d-%d:" % (entitySet_index, entity_index, entityMention_index)
                entityType = entityMention.entityType
                phraseType = entityMention.phraseType
                if phraseType == "TRIGGER":
                    continue
                indices = get_token_indices_for_entityMention(entityMention)
                sentence_index = find_which_sentence(entityMention.tokens.tokenization, comm)
                entity_json = {
                    "id": entitymention_id,
                    "start": indices[0],
                    "end": indices[-1] + 1,
                    "text": u" ".join(get_tokens_for_entityMention(entityMention)),
                    "entity-type": entityType,
                    "phrase-type": phraseType,
                }
                js[sentence_index][u"golden-entity-mentions"].append(entity_json)
    # events
    if comm.situationSetList:
        situationSet_index = -1
        for i, situationSet in enumerate(comm.situationSetList):
            if situationSet.metadata.tool.startswith("Pacaya"):
                situationSet_index = i
        situationSet = comm.situationSetList[situationSet_index]
        for situation_index, situation in enumerate(situationSet.situationList):
            if situation.mentionList:
                for situationMention_index, situationMention in enumerate(situation.mentionList):
                    event_id = u"SM %d-%d-%d:" % (situationSet_index, situation_index, situationMention_index)
                    sentence_index = -1
                    try:
                        sentence_index = find_which_sentence(situationMention.tokens.tokenization, comm)
                    except:
                        pass

                    event_type = situationMention.situationKind

                    trigger_json = {}
                    arguments_json = []
                    event_json = {
                        "id": event_id,
                        "event_type": event_type,
                        "trigger": trigger_json,
                        "arguments": arguments_json
                    }

                    if situationMention.argumentList:
                        for argument_index, mentionArgument in enumerate(situationMention.argumentList):
                            # print u" " * 10 + u"Argument %d:" % argument_index
                            if mentionArgument.role == "TRIGGER":
                                indices = get_token_indices_for_entityMention(mentionArgument.entityMention)
                                trigger_json["start"] = indices[0]
                                trigger_json["end"] = indices[-1] + 1
                                trigger_json["text"] = u" ".join(
                                    get_tokens_for_entityMention(mentionArgument.entityMention))
                            else:
                                role = mentionArgument.role
                                indices = get_token_indices_for_entityMention(mentionArgument.entityMention)
                                if sentence_index == -1:
                                    sentence_index = find_which_sentence(
                                        mentionArgument.entityMention.tokens.tokenization, comm)
                                argument_json = {
                                    "start": indices[0],
                                    "end": indices[-1] + 1,
                                    "text": u" ".join(get_tokens_for_entityMention(mentionArgument.entityMention)),
                                    "role": role
                                }
                                arguments_json.append(argument_json)
                    if sentence_index != -1:
                        js[sentence_index][u"golden-event-mentions"].append(event_json)

    return js


def main():
    usage = "%prog [options] <input path> <output path>"
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args(sys.argv)

    if len(args) != 3:
        parser.print_help()
        sys.exit(1)

    # in_path = "/mnt/d/MyProjects/AFP_ENG_20030616.0715.2.concrete"
    # out_path = "/mnt/d/MyProjects/AFP_ENG_20030616.0715.json"
    in_path = args[1]
    out_path = args[2]

    if not os.path.exists(in_path):
        raise Exception("Input path doesn't exist: " + in_path)

    comm = read_communication_from_file(in_path)
    js = comm2json(comm)

    with open(out_path, "wb") as out_file:
        json.dump(js, out_file, encoding="utf-8")

    print("From %s to %s done." % (in_path, out_path))


if __name__ == "__main__":
    main()
