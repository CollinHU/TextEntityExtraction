{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf100
{\fonttbl\f0\froman\fcharset0 TimesNewRomanPSMT;\f1\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red38\green38\blue38;\red255\green255\blue255;\red0\green0\blue0;
}
{\*\expandedcolortbl;;\cssrgb\c20000\c20000\c20000;\cssrgb\c100000\c100000\c100000;\cssrgb\c0\c0\c0;
}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}.}{\leveltext\leveltemplateid1\'02\'00.;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listname ;}\listid1}
{\list\listtemplateid2\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}.}{\leveltext\leveltemplateid101\'02\'00.;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listname ;}\listid2}
{\list\listtemplateid3\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}.}{\leveltext\leveltemplateid201\'02\'00.;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listname ;}\listid3}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}{\listoverride\listid2\listoverridecount0\ls2}{\listoverride\listid3\listoverridecount0\ls3}}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sl460\sa195\partightenfactor0

\f0\b\fs39 \cf2 \cb3 \expnd0\expndtw0\kerning0
README\
\pard\pardeftab720\sl360\sa156\partightenfactor0

\fs31\fsmilli15600 \cf2 Environment\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls1\ilvl0
\b0\fs30 \cf2 \kerning1\expnd0\expndtw0 {\listtext	1.	}\expnd0\expndtw0\kerning0
python 3.6\cb1 \
\ls1\ilvl0\cb3 \kerning1\expnd0\expndtw0 {\listtext	2.	}\expnd0\expndtw0\kerning0
python packages: \
\ls1\ilvl0\kerning1\expnd0\expndtw0 {\listtext	3.	}\expnd0\expndtw0\kerning0
NLTK, re, pandas, json.\cb1 \
\ls1\ilvl0\cb3 \kerning1\expnd0\expndtw0 {\listtext	4.	}\expnd0\expndtw0\kerning0
java package: \
\ls1\ilvl0\kerning1\expnd0\expndtw0 {\listtext	5.	}\expnd0\expndtw0\kerning0
stanford-corenlp-full-2017-06-09/stanford-corenlp-3.8.0.jar, \
\ls1\ilvl0\kerning1\expnd0\expndtw0 {\listtext	6.	}\expnd0\expndtw0\kerning0
stanford-corenlp-full-2017-06-09/stanford-corenlp-3.8.0-models.jar\cb1 \
\pard\pardeftab720\sl280\partightenfactor0

\f1\fs24 \cf4 \
\pard\pardeftab720\sl360\sa156\partightenfactor0

\f0\b\fs31\fsmilli15600 \cf2 \cb3 Code Explanation\
\pard\pardeftab720\sl540\sa240\partightenfactor0

\b0\fs30 \cf2 As stated in report, the whole process includes data cleaning, target extraction\
\pard\pardeftab720\sl360\sa156\partightenfactor0

\b\fs31\fsmilli15600 \cf2 Data Cleaning\
\pard\pardeftab720\sl540\sa240\partightenfactor0

\b0\fs30 \cf2 the codes are sotred in directory 
\i data_process
\i0 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls2\ilvl0
\i \cf2 \kerning1\expnd0\expndtw0 {\listtext	1.	}\expnd0\expndtw0\kerning0
clean_data.py
\i0  : this code is used to remove meaningless marks\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls2\ilvl0\cf2 \kerning1\expnd0\expndtw0 {\listtext	2.	}\expnd0\expndtw0\kerning0
input: 
\i raw_data.csv
\i0 , output: 
\i step1_data.csv
\i0 \cb1 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls2\ilvl0
\i \cf2 \cb3 \kerning1\expnd0\expndtw0 {\listtext	3.	}\expnd0\expndtw0\kerning0
remove_non_english_sents.py
\i0  : this code is used to remove reviews not writen in English\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls2\ilvl0\cf2 \kerning1\expnd0\expndtw0 {\listtext	4.	}\expnd0\expndtw0\kerning0
input: 
\i step1_data.csv
\i0 , output: 
\i step2_data.csv
\i0 \cb1 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls2\ilvl0
\i \cf2 \cb3 \kerning1\expnd0\expndtw0 {\listtext	5.	}\expnd0\expndtw0\kerning0
groupData_base_on_id.py
\i0 : group data based on course id.\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls2\ilvl0\cf2 \kerning1\expnd0\expndtw0 {\listtext	6.	}\expnd0\expndtw0\kerning0
input: 
\i step2_data.csv
\i0 . output: 36 course review files\cb1 \
\pard\pardeftab720\sl280\partightenfactor0

\f1\fs24 \cf4 \
\pard\pardeftab720\sl540\sa240\partightenfactor0

\f0\fs30 \cf2 \cb3 All data used in above are stored in directory 
\i data
\i0 , and 36 course review files are stored in the subdirectory 
\i course
\i0   under 
\i data
\i0 . These 36 files are named in form of 
\i course_"course_id".csv
\i0 \
\pard\pardeftab720\sl360\sa156\partightenfactor0

\b\fs31\fsmilli15600 \cf2 Target Extraction\
\pard\pardeftab720\sl540\sa240\partightenfactor0

\b0\fs30 \cf2 The codes are stored in directory 
\i extract_target
\i0 .\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls3\ilvl0
\i \cf2 \kerning1\expnd0\expndtw0 {\listtext	1.	}\expnd0\expndtw0\kerning0
extract_target_list.py
\i0 : this code is to grow target and opinion list by propagation\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls3\ilvl0\cf2 \kerning1\expnd0\expndtw0 {\listtext	2.	}\expnd0\expndtw0\kerning0
input: 
\i course_"course_id".csv
\i0 , output: 
\i course_"course_id"_target_list.txt
\i0 \cb1 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls3\ilvl0
\i \cf2 \cb3 \kerning1\expnd0\expndtw0 {\listtext	3.	}\expnd0\expndtw0\kerning0
extract_target_phrase.py
\i0 : this code is to extract target word or phrase for each review.\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls3\ilvl0\cf2 \kerning1\expnd0\expndtw0 {\listtext	4.	}\expnd0\expndtw0\kerning0
input: 
\i course_"course_id".csv
\i0 , 
\i course_"course_id"_target_list.txt
\i0 \
\ls3\ilvl0\kerning1\expnd0\expndtw0 {\listtext	5.	}\expnd0\expndtw0\kerning0
output: 
\i course_"course_id"_transaction.csv
\i0 \cb1 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls3\ilvl0
\i \cf2 \cb3 \kerning1\expnd0\expndtw0 {\listtext	6.	}\expnd0\expndtw0\kerning0
filter_target.py
\i0 : this coude is used to prun the targets.\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sl540\partightenfactor0
\ls3\ilvl0\cf2 \kerning1\expnd0\expndtw0 {\listtext	7.	}\expnd0\expndtw0\kerning0
inuput: 
\i course_"course_id"_transaction.csv
\i0 \
\ls3\ilvl0\kerning1\expnd0\expndtw0 {\listtext	8.	}\expnd0\expndtw0\kerning0
output: 
\i course_"course_id"_target_filtered.txt
\i0 \
\ls3\ilvl0\kerning1\expnd0\expndtw0 {\listtext	9.	}\expnd0\expndtw0\kerning0
 All output files produced by this part are stored under the directory 
\i result
\i0 .\cb1 \
\pard\pardeftab720\sl280\partightenfactor0

\f1\fs24 \cf4 \
\pard\pardeftab720\sl360\sa156\partightenfactor0

\f0\b\fs31\fsmilli15600 \cf2 \cb3 Result\
\pard\pardeftab720\sl540\sa240\partightenfactor0

\b0\fs30 \cf2 Final result stored in the files names as 
\i course_"course_id"_target_filtered.txt
\i0 .\
\pard\pardeftab720\sl360\sa156\partightenfactor0

\b\fs31\fsmilli15600 \cf2 Other code files\
\pard\pardeftab720\sl540\sa240\partightenfactor0

\b0\fs30 \cf2 other files not mentioned above are used for testing or experiments coulde be ignored.\
}