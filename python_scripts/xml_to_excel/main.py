import pandas as pd
from lxml import etree

def cln_data(n):
    x=n
    x=x.replace("[","*[")
    x=x.replace("]","]*")
    y=x.split("*")
    res=[]
    for i in y:
        if len(i)!=0:
            if i[0]=="[" and i[-1]=="]":
                pass
            else:
                res.append(i)
    res="".join(res)
    return res

def get_temp_arry():
    global temp_row    
    temp_row=[]
    for i in range(0,len(final_col_list)):
        temp_row.append("")
    return temp_row

data = "sample.xml"
output_dict={}
pd.set_option("max_rows", None)
pd.set_option('max_columns', None)
tree = etree.parse(data)
lstKey = []
lstValue = []
for p in tree.iter() :
    cln=tree.getpath(p).replace("/",".")[1:]
    lstKey.append(cln)
    lstValue.append(p.text)
    output_dict[lstKey[-1]]=lstValue[-1]
df = pd.DataFrame({'key' : lstKey, 'value' : lstValue})
df.sort_values('key')
column_name={"root"}
rows_dist={"0000"}
max_cols=0
for k in output_dict:
    rows_dist.add(k.split("]")[0])
    column_name.add(cln_data(k))
max_rows=len(rows_dist)-2
temp_col_dict={}
for i in column_name:
    if i=="root":
        continue
    else:
        temp_col_dict[i]=i.count(".")
final_col_list = sorted(temp_col_dict)
final_col_dict={}
for i in final_col_list:
    final_col_dict[i]=final_col_list.index(i)
temp_row=[]
for i in range(0,len(final_col_list)):
    temp_row.append("")
all_rows=[]
arn=-1
i=0
while True:
    k=lstKey[i]
    if "[" in k and "]" in k:
        c=cln_data(k)
        ci=final_col_list.index(c)
        v=lstValue[i]
        crn=int(k[k.index("[")+1:k.index("]")])-1
        if crn!=arn:
            arn+=1
            all_rows.append(temp_row)
            temp_row=get_temp_arry()
        temp_row[ci]=v
    if len(all_rows)==max_rows:
        all_rows.append(temp_row)
        break
    i+=1
all_rows.pop(0)
df = pd.DataFrame(all_rows, columns= final_col_list)
df.to_excel("output.xlsx")
