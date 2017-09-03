import csv
import sys
import numpy as np

nameIn = sys.argv[1]
prof = sys.argv[2]
# nameOut = sys.argv[2] + '.csv'
with open(nameIn,'r') as csvinput:
    # with open(nameOut, 'wb') as csvoutput:
        # writer = csv.writer(csvoutput, quoting=csv.QUOTE_ALL)
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        a = row
        b = row
        c = []
        # print("HEHEHEHEHEHEH " + str(b))

        # a= ['Sheet name','Sheet index','Column name','Column index','Data type','Empty count','Nonempty count','Density','Max length str','Min length str','Max number','Min number','Max date','Min date','Unique count','Unique values']
        # a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # b = [][]
        column_nb = len(a)
        # row_nb = len(reader)
        # for j in (1, column_nb):
        #     r.apend(r[j])
        # row.append('test')
        # all.append(r)
        # print('TOTOTTOOTOTO  ' + str(column_nb))

        j = 1
        # for (is_last, row) in enumerate(ax.isLast(reader)):
        for row in reader:
            for i in range(0, column_nb):
                # print('rrrrr ' + str(row))
                c.append(row[i])
                if(j > 1):
                    b.append(a[i] + str(j))
            j = j + 1
                # row.append(row[0])
                # all.append(row)
        # b.append('\n' + str(c))
        b.insert(0, 'Profil')
        c.insert(0, prof)
        print(str(b).translate(None, "'[]"))
        print(str(c).translate(None, "'[]"))
        # np.savetxt("FILENAME.csv", b, delimiter=",")
        # print(type(b))
        # print(c)
        # writer.writerows(b)
        # writer.writerows(b)
        # writer.writerows(c)
