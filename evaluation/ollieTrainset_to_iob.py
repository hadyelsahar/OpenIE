__author__ = 'heni'

import argparse


def _add_spo_tags(elem,spo_extraction):
    if elem in spo_extraction[0]:
        if spo_extraction[0].index(elem)==0:
            to_write='<B-Subj>'+elem+'</B-Subj>'
        else:
            to_write='<I-Subj>'+elem+'</I-Subj>'
    elif elem in spo_extraction[1]:
        if spo_extraction[1].index(elem)==0:
            to_write='<B-Pred>'+elem+'</B-Pred>'
        else:
            to_write='<I-Pred>'+elem+'</I-Pred>'
    else:
        if spo_extraction[2].index(elem)==0:
            to_write='<B-Obj>'+elem+'</B-Obj>'
        else:
            to_write='<I-Obj>'+elem+'</I-Obj>'
    return to_write


def _to_iob_tags(iob_schema_file,ollie_output_line,spo_extraction):
    sentence=ollie_output_line[3]
    sentence_split=sentence.split(' ')
    sub_sent=str(spo_extraction[0]+' '+spo_extraction[1]+' '+spo_extraction[2])
    spo_words=sub_sent.split(' ')

    iob_to_write=''
    redundant_words=[]
    for word in spo_words:
        if sentence.count(word)>1:
            redundant_words.append(word)
    for i in range(0,len(sentence_split)):
        elem=sentence_split[i]

        if elem in spo_words:
            if elem in redundant_words:
                if sentence_split[i+1] in spo_words:
                    iob_to_write+=_add_spo_tags(elem,spo_extraction)
                else:
                    iob_to_write+='<O>'+elem+'</O>'
            else:
                iob_to_write+=_add_spo_tags(elem,spo_extraction)
        else:
            iob_to_write+='<O>'+elem+'</O>'

        iob_to_write+=' '

    iob_schema_file.write(ollie_output_line[0]+'\t'+ollie_output_line[1]+'\t'+ollie_output_line[2]+'\t'+iob_to_write)


def convert_to_iob(ollie_input_file, ollie_output_file):
    ollie_file = open(ollie_input_file, 'r')
    ollie_lines = ollie_file.readlines()

    iob_schema_file = open(ollie_output_file, 'w')

    for line in ollie_lines:
        bad_extraction_representation=[]
        line_elements=line.split('\t')
        extractions=line_elements[2]
        spo_extraction=extractions.split(')(')[0].split(';')
        try:
            assert len(spo_extraction)==3
        except:
            bad_extraction_representation.append(line)
            continue
        spo_extraction_prep=[]
        for phrase in spo_extraction:
            if not phrase[0].isalnum():
                phrase=phrase[1:]
            if not phrase[-1].isalnum():
                phrase=phrase[:-1]

            spo_extraction_prep.append(phrase)

        assert len(spo_extraction_prep)==3
        _to_iob_tags(iob_schema_file,line_elements,spo_extraction_prep)

    ollie_file.close()
    iob_schema_file.close()


# convert_to_iob('data/ollie-scored.txt')


parser = argparse.ArgumentParser(description='converting the Ollie groundtruth to the IOB format')
parser.add_argument('-i', '--input', help='input file pathname contains gold standard annotated data, the ground-truth', required=True)
parser.add_argument('-o', '--output', help='output file pathname contains the same annotated dataset but in IOB formatted tags', required=False)

args = parser.parse_args()

if args.output is None:
    args.output = args.input.replace(".txt", ".iob.txt")

convert_to_iob(args.input, args.output)




