from main import Item,Console,Packer
import pandas as pd

#Read the file containing all the information regarding the items
df=pd.read_csv('itemsList.csv')
items=[]

#Code to order the dimensions of the items in descending order
dict = {}
for index, row in df.iterrows():
    x,y,z = row['length'],row['width'],row['height']
    l = [x,y,z]
    l.sort(reverse=True)
    d = {row['id_x'] : l}
    dict.update(d)

df1 = pd.DataFrame.from_dict(dict, orient='index').rename(columns={0:'width',1:'length',2:'height'})

df1['id_x'] = df1.index

df = df.drop(axis=1,columns=['height','length','width'])

df = df.merge(df1, on = ['id_x'], how='inner')

#Create a instance of the class Packer
packer = Packer()

#add all the items to the class Item
for _, row in df.iterrows():
    id = row['id_x']
    width=row['width']
    height =row['height']
    length = row['length']
    weight = row['weight']
    stackable = row['stackable']
    availableDate=row['availableDate']
    dueDate=row['dueDate']
    origin = row['origin']
    destination = row['destination']

    packer.add_item(Item(id,width,height,length,weight,stackable,availableDate,dueDate,origin,destination))

    
#Read the console Data
consoleDF=pd.read_csv('ConsoleData.csv')

#Add all the consoles to the class Console
for _, row in consoleDF.iterrows():
    id = row['Id']
    type_val = row['Type']
    max_weight = row['Max Weight']
    pivot_weight = row['Pivot Weight']
    rate_to_pivot_weight = row['Rate to Pivot Weight']
    rate_above_pivot_weight = row['Rate Above Pivot Weight']
    height = row['Height']
    depth = row['Depth']
    width = row['Width']
    max_volume = row['Max Vol']
    origin = row['Origin']
    destination = row['Destination']
    departure = row['Departure']
    arrival = row['Arrival']
    fix_rate = row['Fix Rate']
    technical_max_weight = row['Technical Max Weight']
    
    packer.add_console(Console(id,type_val,max_weight,pivot_weight,rate_to_pivot_weight,rate_above_pivot_weight,fix_rate,height,depth,width,max_volume,origin,destination,departure,arrival))

#Call the function pack to start packing 
packer.pack()

#create a list of all the items packed and related attributes
item_r = list()
for console in packer.consoles:
    c_id = str(console.id)
    max_v = console.max_volume
    tot_v = console.get_total_volume()
    vol_d = console.get_volume()
    percentage_v_used = tot_v/max_v*100
    for item in console.items:
        print(item.string())
        i_id = item.id
        h = item.height
        l = item.length
        w = item.width
        p = item.position
        rt = item.rotation_type
    
        data = [c_id,i_id,w,l,h,p,rt,tot_v,max_v,vol_d,percentage_v_used]
        item_r.append(data)

#Count the number of itens which didn't get packed
count = 0
for item in packer.items:
        if item.is_packed == False:
            count += 1
print(count)
        
#create a DB of the packed items
packed_items = pd.DataFrame(item_r,columns=['Container_id','Item_id','Width','Length','Height','Position','Rotation','Console_utilised_volume','Console_Usable_Volume','Total_Volume','%Utilization'])

#save the DB to get the packing of all the items along with the consoles in which they are packed and their respective postions and orientation
packed_items.to_excel("packed_items.xlsx",index=False)
