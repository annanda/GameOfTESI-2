def mos_common(lst):
    return max(set(lst), key=lst.count)

def dictKmeansToData(data, labelList, kmeansVariable):
    dic = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8}
    #size = []
    for i in range(kmeansVariable):
        indices = [j for j, x in enumerate(labelList) if x == i]   
        topics = []
        for item in indices:
            topics.append(int(data[item]["assunto"]))
           
        mostCommon = mos_common(topics)
        #print(accuracy(topics, mostCommon))
        dic[i] = mostCommon
    return dic
    
lista = [1,0,0,0,2,3,2,2,2,2,1,2]
data = 0

print(dictKmeansToData(data, lista, 8))
