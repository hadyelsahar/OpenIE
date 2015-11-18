## install nltk dependencies
```
wget http://nlp.stanford.edu/software/stanford-ner-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-04-20.zip
unzip "*.zip"
rm *.zip
```

## add nltk 3rd parties dependencies

- add jar directories in the java class path. eg : 
```
export CLASSPATH=/home/ubuntu/workspace/nltk-external-resources/stanford-ner-2015-04-20/:/home/ubuntu/workspace/nltk-external-resources/stanford-postagger-full-2015-04-20/
```

- more details : https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software
- add directory of models in the stanfordmodels env variable

```
export STANFORD_MODELS=/home/ubuntu/workspace/nltk-external-resources/stanford-ner-2015-04-20/classes:/home/ubuntu/workspace/nltk-external-resources/stanford-postagger-full-2015-04-20/models
more details : https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software
``` 
