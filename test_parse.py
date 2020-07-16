import argparse
from stanford_corenlp_pywrapper import sockwrap
from petrarch2 import petrarch2, PETRglobals, PETRreader, utilities
from petrarch2 import PETRtree as ptree
import sys
import logging
import datetime


def test_simple():

    text = "Germany invaded France"
    parse = "(ROOT (S (NP (NNP Germany)) (VP (VBD invaded) (NP (NNP France)))))"
    parsed = utilities._format_parsed_str(parse)

    dict = {u'test123': {u'sents': {u'0': {u'content': text, u'parsed': parsed}},
                u'meta': {u'date': u'20010101'}}}

    return_dict = petrarch2.do_coding(dict)
    print(return_dict)
    events = return_dict['test123']['sents']['0']['events']
    print(events)
    #print(return_dict)
    #assert return_dict['test123']['sents']['0']['events'] == [('DEU','FRA','192')]


def parse_sentence(stanford_parser, date, text):
    
    nlp = stanford_parser.parse_doc(text)
    parse = nlp['sentences'][0]['parse']
    parsed = utilities._format_parsed_str(parse)

    dict = {u'doc': {
                u'sents': {
                    u'0': {
                        u'content': text,
                        u'parsed': parsed
                    }
                },
                u'meta': {
                    u'date': date
                }


            }
        }

    return_dict = petrarch2.do_coding(dict)

    has_events = False
    
    if  "events" in return_dict['doc']['sents']['0']:
        #events = return_dict['doc']['sents']['0']['events']
        has_events = True

    return_dict['has_events'] = has_events
    return_dict['sentence_date'] = date

    print(str(return_dict))

    return return_dict


def write_non_event(f, nonevent):

    sent0 = nonevent['doc']['sents']['0']
    content = sent0['content'].encode('utf-8').strip()
    sent_date = nonevent['sentence_date']
    f.write("SENTENCE:\n" + content + "\n")
    f.write("sentence date: " + sent_date[:4] + " " + 
                               sent_date[5:7] + " " + sent_date[7:] + "\n")
    f.write("# of events: 0\n\n\n")


# return the actor & verb codes
def get_codes(triple):
    estring = str(triple)[1:-1]
    estring = estring.replace("u", "")
    estring = estring.replace("'", "")
    elist = estring.split(",")
    actor1 = elist[0]
    actor2 = elist[1]
    verbcode = elist[2]

    return actor1, actor2, verbcode

def write_event_text(f, eventtext):
    idx = 1
    for key, value in eventtext.iteritems():
        actor1, actor2, verbcode = get_codes(key)
        verblabel = str(value).replace("u", "")
        verblabel = verblabel.replace("u", "")

        f.write("Event " + str(idx) + ": ")
        f.write(actor1 + "\t" + actor2 + "\t" + verbcode + "\t" + verblabel + "\n")

        idx += 1

def write_actor_text(f, actortext):
    idx = 1
    for key, value in actortext.iteritems():
        actor1, actor2, verbcode = get_codes(key)
        label1 = value[0].encode('utf-8')   
        label2 = value[1].encode('utf-8')   

        f.write("Actors for event " + str(idx) + "\n")
        f.write("\tSoure actor: " + label1 + " => " + actor1 + "\n")
        f.write("\tTarget actor: " + label2 + " => " + actor2 + "\n")
        f.write("\tVerb code: " + verbcode + "\n\n")

        idx += 1
     


def write_has_events(f, sent_with_events):

    sent0 = sent_with_events['doc']['sents']['0']
    content = sent0['content'].encode('utf-8').strip()
    events = sent0['events']
    meta = sent_with_events['doc']['meta']
    sent_date = sent_with_events['sentence_date']

    # Standard mode uses verbs
    if 'verbs' in meta:
        verbs = meta['verbs']
        eventtext = verbs['eventtext']
        actortext = verbs['actortext']
    else:   
        # null actors mode does not use verbs
        eventtext = meta['eventtext']
        actortext = meta['actortext']


    f.write("SENTENCE:\n" + content + "\n\n")
    f.write("sentence date: " + sent_date[:4] + " " + 
                               sent_date[5:7] + " " + 
                               sent_date[7:] + "\n\n")
    f.write("Events: " + str(len(events)) + "\n\n")
    f.write("Source Actor, Target Actor, Verb Code, Verb Label\n")
    write_event_text(f, eventtext)
    f.write("\n")
    #f.write("actor text" + str(actortext) + "\n")
    write_actor_text(f, actortext)
    f.write("\n\n")



def main():

    INPUT_FILENAME = "input.txt"
    OUTPUT_FILENAME = "results.txt"

    # Get running mode. 'Standard' produces events normally. 'Null Actors' records the actor labels.
    parser = argparse.ArgumentParser(description='Run petrarch in standard mode or null-actors mode')
    parser.add_argument("event_mode", help="Specify [s]tandard or [n]ull actors mode.")
    args = parser.parse_args()
    print ("Running mode: " + args.event_mode)

    config_file = "not_specified"
    mode = args.event_mode.lower()
    if mode.startswith("s"):
        config_file = "PETR_config_standard.ini"
    elif mode.startswith("n"):
        config_file = "PETR_config_null_actors.ini"
    else: 
        print("Must specify [s]tandard or [n]ull actors mode as an argument.\nExiting.")
        sys.exit()


    # Read input
    entries = []
    try:
        with open(INPUT_FILENAME,"r") as f:
            lines = f.readlines()

    except: 
        logging.error("Input file: " +  INPUT_FILENAME + " not able to be read.")   
        sys.exit()


    for line in lines:
        line = line.strip()
        if (len(line) > 0) and not line.startswith("#"):
            entries.append(line)


    config_dir = 'data/config/'
    config = petrarch2.utilities._get_data(config_dir, config_file)
    config_path = config_dir + config_file
    print("Reading config: " + config_path)
    
    petrarch2.PETRreader.parse_Config(config)
    print("reading dicts")
    petrarch2.read_dictionaries()

    stanford_parser = sockwrap.SockWrap(mode='justparse',
                                        configfile='stanford_config.ini',
                                        corenlp_libdir="stanford_corenlp_pywrapper/stanford-corenlp")


    # test = stanford_parser.parse_doc("hello world. how are you?")
    # print(test)
    #test_simple()
    results = []
    for entry in entries:
        date = entry[:8]
        sent = entry[9:].decode('utf-8')
        sent = unicode(sent)
        t = type(sent)
        coding_result = parse_sentence(stanford_parser, date, sent)
        results.append(coding_result) 

    try:
        with open(OUTPUT_FILENAME, 'w') as f:

            f.write("SENTENCE PARSE RESULTS\n")
            f.write(str(datetime.datetime.now()) + "\n")
            f.write("# sentences: " + str(len(results)) + "\n")

            if mode.startswith('s'):
                f.write("Coding Mode:  Null Actors = FALSE\n\n")
            else:
                f.write("Coding Mode:  Null Actors = TRUE\n\n")

            for coding_result in results:
                if coding_result['has_events']:
                    write_has_events(f, coding_result)
                else:
                    write_non_event(f, coding_result)
                
    except: 
        logging.error("Error writing output")   
        sys.exit()    

if __name__ == '__main__':
    main()    