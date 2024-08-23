from main import Item,Console,Packer 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# assignment = pd.read_excel('./Data/OutputData/OptimisationSolutionFor-2660893353461949155.xlsx') #16
# assignment = pd.read_excel('./Data/OutputData/OptimisationSolutionFor3496209091753275137.xlsx') #41
assignment = pd.read_excel('./Data/OutputData/OptimisationSolutionFor-3588730938131414660.xlsx') #33
# assignment = pd.read_excel('./Data/OutputData/OptimisationSolutionFor-5788057936487630500.xlsx') #10
# assignment = pd.read_excel('./Data/OutputData/OptimisationSolutionFor6328215800676228263.xlsx') #0
# assignment = pd.read_excel('./Data/OutputData/OptimisationSolutionFor-6824274894038470334.xlsx') #4



consoleDF = pd.read_excel('./Data/InputData/ConsoleData.xlsx')

Items = pd.read_excel('./Data/InputData/cleanedItems.xlsx')
Items = Items[['id_x','weight_y']]
print(type(Items))

df=pd.read_csv('./Data/InputData/itemsList.csv')
# df = df[df['destination'] == -2660893353461949155]
items=[]

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

df = df.drop(axis=1,columns=['weight'])

df = df.merge(Items, on = ['id_x'], how= 'left')

df = df.rename(columns={'weight_y':'weight'})

assignment = assignment.merge(df, left_on = 'item_id',right_on = 'id_x', how = 'left')
assignment = assignment.drop(axis=1,columns=['id_x','x_ij'])
assignment.to_excel('./Data/OutputData/assignment.xlsx',index=False)

containerList = assignment['console_id'].unique().tolist()

item_r = list()
unfit_item = list()
count = 0
for container in containerList:

    new = assignment[assignment['console_id'] == container]
    new_console = consoleDF[consoleDF['Id'] == container]

    packer = Packer()

    for _, row in new.iterrows():
        id = row['item_id']
        width=row['width']
        height =row['height']
        length = row['length']
        weight = row['weight']
        stackable = row['stackable']
        availableDate=row['availableDate']
        dueDate=row['dueDate']
        origin = row['origin']
        destination = row['destination']
        
        packer.add_item(Item(id,width,length,height,weight,stackable,availableDate,dueDate,origin,destination))
        
    for _, row in new_console.iterrows():
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
    
        packer.add_console(Console(id,type_val,technical_max_weight,pivot_weight,rate_to_pivot_weight,rate_above_pivot_weight,fix_rate,height,depth,width,max_volume,origin,destination,departure,arrival))

    packer.pack()

    for console in packer.consoles:
        print('Console:',console.string())
        print('Filled Volume',console.get_total_volume())
        print('Total Weight',console.get_total_weight())
        print('Volume Used',(console.get_total_volume()/console.get_volume())*100)
        print('Weight Used',)
        print('Items:')
        c_id = str(console.id)
        H = console.height
        L = console.length
        W = console.width
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
            
            data = [c_id,i_id,w,l,h,p,rt,W,L,H,tot_v,max_v,vol_d,percentage_v_used]
            item_r.append(data)
        for item in console.unfitted_items:
            print('Unfitted items:')
            print('\n ', item.string())
            id = item.id
            h = item.height
            l = item.length
            w = item.width
            s = item.status

            ud = [c_id,id,w,l,h,W,L,H,s]
            unfit_item.append(ud)

    for item in packer.items:
        if item.is_packed == False:
            count += 1
    print(count)

        
packed_items = pd.DataFrame(item_r,columns=['Container_id','Item_id','Width','Length','Height','Position','Rotation','Console_Width','Console_Length','Console_Height','Console_utilised_volume','Console_Usable_Volume','Total_Volume','%Utilization'])
unfitted_items = pd.DataFrame(unfit_item,columns=['Container_id','Item_id','Width','Length','Height','Console_Width','Console_Length','Console_Height','Status'])
unfitted_items.to_excel('./Data/OutputData/UnfitItems'+str(count)+'.xlsx',index=False)
print(packed_items)
print(unfitted_items)