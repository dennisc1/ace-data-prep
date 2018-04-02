import json

import os
from concrete.inspect import get_tokens_for_entityMention, print_entities
from concrete.util import read_communication_from_file


def print_situation_mentions(comm):
    """Print information for all SituationMentions (some of which may not have Situations)

    Args:

    - `comm`: A Concrete Communication
    """
    if comm.situationMentionSetList:
        for situationMentionSet_index, situationMentionSet in enumerate(comm.situationMentionSetList):
            if situationMentionSet.metadata:
                print u"Situation Set %d (%s):" % (situationMentionSet_index, situationMentionSet.metadata.tool)
            else:
                print u"Situation Set %d:" % situationMentionSet_index
            for situationMention_index, situationMention in enumerate(situationMentionSet.mentionList):
                print u"  SituationMention %d-%d:" % (situationMentionSet_index, situationMention_index)
                _print_situation_mention(situationMention)
                print
            print


def _p(indent_level, justified_width, fieldname, content):
    """Text alignment helper function"""
    print u" " * indent_level + (fieldname + u":").ljust(justified_width) + content


def _print_situation_mention(situationMention):
    """Helper function for printing info for a SituationMention"""
    if situationMention.text:
        _p(10, 20, u"text", situationMention.text)
    if situationMention.situationType:
        _p(10, 20, u"situationType", situationMention.situationType)
    if situationMention.situationKind:
        _p(10, 20, u"situationKind", situationMention.situationKind)
    if situationMention.argumentList:
        for argument_index, mentionArgument in enumerate(situationMention.argumentList):
            print u" " * 10 + u"Argument %d:" % argument_index
            if mentionArgument.role:
                _p(14, 16, u"role", mentionArgument.role)
            if mentionArgument.entityMention:
                _p(14, 16, u"entityMention",
                   u" ".join(get_tokens_for_entityMention(mentionArgument.entityMention)))
            # A SituationMention can have an argumentList with a MentionArgument that
            # points to another SituationMention - which could conceivably lead to
            # loops.  We currently don't traverse the list recursively, instead looking
            # at only SituationMentions referenced by top-level SituationMentions
            if mentionArgument.situationMention:
                print u" " * 14 + u"situationMention:"
                if situationMention.text:
                    _p(18, 20, u"text", situationMention.text)
                if situationMention.situationType:
                    _p(18, 20, u"situationType", situationMention.situationType)


def comm2json(comm):
    js = {}
    # sms = comm.situationMentionSetList[0].mentionList
    # for event in sms:
    #     pass
    print_situation_mentions(comm)
    print_entities(comm)
    return js


def main():
    # usage = "%prog [options] <input path> <output path>"
    # parser = optparse.OptionParser(usage=usage)
    # (options, args) = parser.parse_args(sys.argv)
    #
    # if len(args) != 3:
    #     parser.print_help()
    #     sys.exit(1)

    in_path = "/mnt/d/MyProjects/ACE2005/preprocess/ace-05-comms/AFP_ENG_20030616.0715.concrete"
    out_path = "/mnt/d/MyProjects/AFP_ENG_20030616.0715.json"

    if not os.path.exists(in_path):
        raise Exception("Input path doesn't exist: " + in_path)

    comm = read_communication_from_file(in_path)
    js = comm2json(comm)

    with open(out_path, "wb") as out_file:
        json.dump(js, out_file, encoding="utf-8")

        # Serialize
        # write_communication_to_file(comm, out_file)


if __name__ == "__main__":
    main()
