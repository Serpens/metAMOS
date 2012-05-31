#!/usr/bin/python

import sys, os, string
ROOT = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, os.path.join(ROOT, '..'))
#sys.path.append(ROOT+"/lib")
import  markup, datetime

contigs_by_class = { }
origContigsByClass = { }
origClassifiedCount = 0
classifiedCount = 0
id_class = { }
id_class["0"] = "UNKNOWN"

orig_class_file = open(sys.argv[1])
class_file = open(sys.argv[2])
class_key = open(sys.argv[3])
#pass outdir as argument
out_dir = sys.argv[4]
out = open(out_dir + os.sep + sys.argv[5], 'w')
orig_out = open(out_dir + os.sep + sys.argv[6], 'w')
taxa_level = sys.argv[7]

# parse in key file
for line in class_key:
    line = line.strip()
    fields = line.split("\t")
    # f1 is id, f2 is class name

    if len(fields) != 2:
        print "Error in file format\n"
    else:
        id_class[fields[0]] = fields[1]

# parse original file to identity ambiguous assignment (which is one more than max previous ID)
maxClassID = 0;
for line in orig_class_file:
    line = line.strip()
    fields = line.split()
    # f1 is contig, f2 is class

    if len(fields) != 2:
        print "Error in file format\n"

    elif maxClassID < int(fields[1]):
       maxClassID = int(fields[1])

    if origContigsByClass.has_key(fields[1]):
       origContigsByClass[fields[1]]+=1
    else:
       origContigsByClass[fields[1]] = 1
    origClassifiedCount += 1

id_class[str(maxClassID+1)] = "AMBIGUOUS"

# parse contig class file
for line in class_file:
    line = line.strip()
    fields = line.split()
    # f1 is contig, f2 is class

    if len(fields) != 2:
        print "Error in file format\n"
    elif contigs_by_class.has_key(fields[1]):
        contigs_by_class[fields[1]] += 1
    else:
        contigs_by_class[fields[1]] = 1

    if fields[1] > 0:
       classifiedCount += 1

# output stats
# todo: add info on ORFs and read counts
summary = markup.page()
summary.p("Originally classified contigs:")
summary.table(border="1")
for key in origContigsByClass:
   class_name = id_class[key]
   summary.tr()
   summary.add("<td align=\"left\">%s</td><td align=\"right\">%d</td><td align=\"right\">%3.2f%%</td>"%(class_name, origContigsByClass[key], origContigsByClass[key]/float(origClassifiedCount)*100))
   summary.tr.close()
summary.tr()
summary.add("<td align=\"left\"Total classified:</td><td align=\"right\">%d</td>"%(origClassifiedCount))
summary.tr.close()
summary.table.close()

classify = markup.page()
classify.p("Classified contigs:")
classify.table(border="1")
for key in contigs_by_class:
    class_name = id_class[key]
    classify.tr()
    classify.add("<td align=\"left\"><a target=\"_blank\" href=\"%s.classified/%s/%s.fasta\">%s</a></td><td align=\"right\">%d</td><td align=\"right\">%3.2f%%</td>"%(taxa_level, class_name, class_name, class_name, contigs_by_class[key], contigs_by_class[key]/float(classifiedCount)*100))
    classify.tr.close()
classify.tr()
classify.add("<td align=\"left\"Total classified:</td><td align=\"right\">%d</td>"%(classifiedCount))
classify.tr.close()
classify.table.close()

additional = classifiedCount - origClassifiedCount 
if additional >= 0:
   summary.p("Total additional classified contigs: %d"%(additional))
else:
   summary.p("Total contigs classified as unknown from known: %d"%(abs(additional)))
summary.p.close();
orig_out.write("var propagateHTML = '%s'"%(summary.__str__().replace("\n", "\\\n")))
out.write("var classifyHTML = '%s'"%(classify.__str__().replace("\n", "\\\n")))

orig_out.close()
out.close()
