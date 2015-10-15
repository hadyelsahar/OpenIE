__author__ = 'heni'

import os
import argparse


def _ollie_output_to_log(ollie_groundtruth_file,log_file_name):
    ollie_groundtruth=open(ollie_groundtruth_file,'r')
    ollie_sentences=open('/data/ollie_trainset.txt','w')

    groundtruth_lines=ollie_groundtruth.readlines()
    written_sentences=[]
    for line in groundtruth_lines:
        parts=line.split('\t')
        sentence=parts[3]
        if sentence not in written_sentences:
            ollie_sentences.write(sentence)
            written_sentences.append(sentence)

    ollie_sentences.close()
    ollie_groundtruth.close()

    os.system("cd ../ollie/ && java -Xmx512m -jar ollie-app-latest.jar ../evaluation/data/ollie_trainset.txt >"
              " ../evaluation/"+log_file_name)


def _spo_to_iob(spo_bloc):
    to_write=''
    assert len(spo_bloc)==3
    for i in range(0,len(spo_bloc)):
        label=spo_bloc[i].split(' ')
        if i==0:
            for elem in label:
                first_subj_written=False
                if label.index(elem)==0 and not first_subj_written:
                    to_write+='<B-Subj>'+elem+'</B-Subj>'+' '
                    first_subj_written=True
                else:
                    to_write+='<I-Subj>'+elem+'</I-Subj>'+' '

        elif i==1:
            for elem in label:
                first_pred_written=False
                if label.index(elem)==0 and not first_pred_written:
                    to_write+='<B-Pred>'+elem+'</B-Pred>'+' '
                    first_pred_written=True
                else:
                    to_write+='<I-Pred>'+elem+'</I-Pred>'+' '

        else:
            for elem in label:
                first_obj_written=False
                if label.index(elem)==0 and not first_obj_written:
                    to_write+='<B-Obj>'+elem+'</B-Obj>'+' '
                    first_obj_written=True
                else:
                    to_write+='<I-Obj>'+elem+'</I-Obj>'+' '

    return to_write


def _context_to_iob(context_extraction):
    to_write=''
    context_sep=context_extraction[:-2].split('=')
    i=0
    context_phrase=context_sep[1].split(' ')
    for i in range(0,len(context_phrase)):
        elem=context_phrase[i]
        if i==0:
            to_write+='<B-'+str(context_sep[0])+'>'+elem+'</B-'+str(context_sep[0])+'>'+' '
        else:
            to_write+='<I-'+str(context_sep[0])+'>'+elem+'</I-'+str(context_sep[0])+'>'+' '

    return to_write


def _write_to_output(ollie_output_file_iob,sentence_bloc):
    ollie_output_file_iob.write(sentence_bloc[0])
    if sentence_bloc[1]=='No extractions found.\n':
        ollie_output_file_iob.write('No extractions found.\n')
    else:
        for i in range(1,len(sentence_bloc)):
            spo_cont_separation=sentence_bloc[i].split(')[')
            ollie_output_file_iob.write(sentence_bloc[i].split(': (')[0] + '\t')
            spo_extraction=spo_cont_separation[0].split(': (')[1].split(';')
            assert len(spo_extraction)==3
            spo_ext_prep=[]
            for phrase in spo_extraction:
                if not phrase[0].isalnum():
                    phrase=phrase[1:]
                if not phrase[-1].isalnum():
                    phrase=phrase[:-2]

                spo_ext_prep.append(phrase)

            assert len(spo_ext_prep)==3
            if len(spo_cont_separation)==1:
                ollie_output_file_iob.write(_spo_to_iob(spo_ext_prep)+'\n')
            else:
                context_extraction=spo_cont_separation[1]
                ollie_output_file_iob.write(_spo_to_iob(spo_ext_prep)+' | '+_context_to_iob(context_extraction)+'\n')

    ollie_output_file_iob.write('\n')


def ollie_output_to_iob(ollie_groundtruth_file,ollie_log_file,ollie_output_iob):
    _ollie_output_to_log(ollie_groundtruth_file,ollie_log_file)
    ollie_output_file=open(ollie_log_file,'r')
    ollie_output_lines=ollie_output_file.readlines()

    ollie_output_file_iob=open(ollie_output_iob,'w')

    ext_lines=ollie_output_lines[:]
    # sentence_bloc=[]
    i=0
    while i in range(0,len(ext_lines)):
        if ext_lines[i]=='\n':
            sentence_bloc=ext_lines[:i]
            _write_to_output(ollie_output_file_iob,sentence_bloc)
            ext_lines=ext_lines[i+1:]
            i=0
        else:
            i+=1

    ollie_output_file.close()
    ollie_output_file_iob.close()


# ollie_output_to_iob('data/ollie-scored.txt','data/ollie_log.txt','data/ollie_output.iob.txt')

parser=argparse.ArgumentParser(description='Experiments on Ollie using the IOB format')
parser.add_argument('-g','--groundtruth', help='groundtruth',required=True)
parser.add_argument('-l','--log', help='log file of the Ollie output',required=True)
parser.add_argument('-o','--output', help='output file under the IOB format',required=True)
args = parser.parse_args()

ollie_output_to_iob(args.groundtruth,args.log,args.output)