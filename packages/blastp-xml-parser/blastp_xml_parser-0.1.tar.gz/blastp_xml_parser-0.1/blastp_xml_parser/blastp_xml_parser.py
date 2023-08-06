def parser(file,out_file):

    from Bio.Blast import NCBIXML
    import pandas as pd
    from itertools import islice



    a = []

    for blast_record in NCBIXML.parse(open(file)):
            count=0
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    count+=1
                    c = [x for x in hsp.match.replace("+"," ").split() if len(x) >=9]
                    if c != []:
                        a.append(blast_record.query_id)
                        a.append(count)
                        a.append(alignment.accession)
                        a.append(hsp.expect)
                        a.append(hsp.query)
                        a.append(c)
                        a.append(hsp.match)
                        a.append(hsp.sbjct)
                        a.append(alignment.title)
                    else:
                        continue

    number = int(len(a)/9)
    o = [9] * number
    inn = iter(a)
    output= [list(islice(inn,i)) for i in o]
    new = pd.Series(output)
    df = pd.DataFrame(output, columns = ("Query Name","Hit Number","Hit Accession Number","E-value","Query","Match (Midline)","Subject","Matching Hit Sequence","Hit Description"))
    df.index.name = "Serial Number"
    df.to_csv("{0}.csv".format(out_file))
