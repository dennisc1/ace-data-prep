import json
import optparse
import sys

import os


def main():
    usage = "%prog [options] <input path> <output path>"
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args(sys.argv)

    if len(args) != 3:
        parser.print_help()
        sys.exit(1)

    in_path = args[1]
    out_path = args[2]

    # in_path = "/mnt/d/MyProjects/AFP_ENG_20030616.0715.json"
    # out_path = "/mnt/d/MyProjects/brat/brat-v1.3_Crunchy_Frog/data/try"

    if not os.path.exists(in_path):
        raise Exception("Input path doesn't exist: " + in_path)

    file_name = in_path.split(os.path.sep)[-1]

    out_txt = open(os.path.join(out_path, file_name + ".txt"), "wb")
    out_ann = open(os.path.join(out_path, file_name + ".ann"), "wb")

    document_char_offset = 0
    entity_no = 0
    event_no = 0
    with open(in_path, "rb") as in_file:
        js = json.load(in_file, encoding="utf-8")
        for sentence_json in js:
            entity_pos2label = {}
            words = sentence_json["words"]
            entities = sentence_json["golden-entity-mentions"]
            events = sentence_json["golden-event-mentions"]
            text = " ".join(words)
            out_txt.write(text + "\n")
            word_char_offset = []
            sentence_char_offset = 0
            for word in words:
                word_char_offset.append(sentence_char_offset)
                sentence_char_offset += len(word) + 1
            for entity in entities:
                entity_type = entity["entity-type"].split(":")[0]
                start_token_offset = entity["start"]
                end_token_offset = entity["end"]
                entity_text = entity["text"]
                if "%d-%d:%s:%s" % (start_token_offset, end_token_offset, entity_text, entity_type) in entity_pos2label:
                    continue
                start_sentence_char_offset = word_char_offset[start_token_offset]
                end_sentence_char_offset = word_char_offset[end_token_offset - 1] + len(words[end_token_offset - 1])
                entity_no += 1
                out_ann.write("T%d\t%s %d %d\t%s\n" % (entity_no,
                                                       entity_type,
                                                       start_sentence_char_offset + document_char_offset,
                                                       end_sentence_char_offset + document_char_offset,
                                                       entity_text))
                entity_pos2label["%d-%d:%s:%s" % (
                start_token_offset, end_token_offset, entity_text, entity_type)] = "T%d" % entity_no

            for event in events:
                # for trigger
                event_type = event["event_type"].split(":")[-1]
                trigger = event["trigger"]
                trigger_text = trigger["text"]
                start_token_offset = trigger["start"]
                end_token_offset = trigger["end"]
                start_sentence_char_offset = word_char_offset[start_token_offset]
                end_sentence_char_offset = word_char_offset[end_token_offset - 1] + len(words[end_token_offset - 1])
                entity_no += 1
                out_ann.write("T%d\t%s %d %d\t%s\n" % (entity_no,
                                                       event_type,
                                                       start_sentence_char_offset + document_char_offset,
                                                       end_sentence_char_offset + document_char_offset,
                                                       trigger_text))
                entity_pos2label["%d-%d:%s:%s" % (
                start_token_offset, end_token_offset, trigger_text, event_type)] = "T%d" % entity_no

                # for event
                event_no += 1
                out_ann.write("E%d\t%s:T%d" % (event_no, event_type, entity_no))
                for argument in event["arguments"]:
                    start_token_offset = argument["start"]
                    end_token_offset = argument["end"]
                    argument_type = argument["entity-type"].split(":")[0]
                    argument_text = argument["text"]
                    argument_role = argument["role"]
                    found_entity_no = entity_pos2label[
                        "%d-%d:%s:%s" % (start_token_offset, end_token_offset, argument_text, argument_type)]
                    out_ann.write(" %s:%s" % (argument_role, found_entity_no))
                out_ann.write("\n")

            document_char_offset += len(text) + 1

    print("From %s to %s done." % (in_path, out_path))
    out_txt.close()
    out_ann.close()


if __name__ == "__main__":
    main()
