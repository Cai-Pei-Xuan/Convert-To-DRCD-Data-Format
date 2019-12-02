# -*-coding:UTF-8 -*-
import json
import os
import time
import re

global num
num = 0
global num2
num2 = 0
global num3
num3 = 0

# 儲存数据
def SaveJson(filepath, filename):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(filename, f, ensure_ascii=False)

# 读取数据
def LoadJson(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        AllData = json.load(f)
    return AllData

# 創造測試資料
def createTest(path):
    test = {}
    test["context"] = "基督新教與天主教均繼承普世教會歷史上許多傳統教義，如三位一體、聖經作為上帝的啟示、原罪、認罪、最後審判等等，但有別於天主教和東正教，新教在行政上沒有單一組織架構或領導，而且在教義上強調因信稱義、信徒皆祭司， 以聖經作為最高權威，亦因此否定以教宗為首的聖統制、拒絕天主教教條中關於聖傳與聖經具同等地位的教導。新教各宗派間教義不盡相同，但一致認同五個唯獨：唯獨恩典：人的靈魂得拯救唯獨是神的恩典，是上帝送給人的禮物。唯獨信心：人唯獨藉信心接受神的赦罪、拯救。唯獨基督：作為人類的代罪羔羊，耶穌基督是人與上帝之間唯一的調解者。唯獨聖經：唯有聖經是信仰的終極權威。唯獨上帝的榮耀：唯獨上帝配得讚美、榮耀"
    a = []
    answer = {}
    answer["tag"] = "陳水扁"
    answer["start_at"] = "5"
    answer["question"] = "產生的問題1"
    a.append(answer)
    answer = {}
    answer["tag"] = "韓國瑜"
    answer["start_at"] = "12"
    answer["question"] = "產生的問題2"
    a.append(answer)
    test["question_detail"] = a

    SaveJson(path + "/test.json", test)
    return test

# 創造轉換成台達電資料格式的結果資料
def createResult(test):
    global num

    result = {}
    result["version"] = "udic1.0"
    AllData = []
    data = {}
    title = test["context"]
    titleList = re.split(r"[,，]", title)
    data["title"] = titleList[0]
    id = 10000
    data["id"] = str(id)
    paragraphs = []
    paragraph = {}
    context = test["context"]
    paragraph["context"] = context
    paragraph["id"] = str(id) + "-1"
    qas = []
    for index, detail in enumerate(test["question_detail"]):
        qa = {}
        qa["id"] = str(id) + "-1-" + str(index+1)
        qa["question"] = detail["question"]
        answers = []
        answer = {}
        answer["id"] = "1"
        answer["text"] = detail["tag"]
        try:
            tag_padding = context.index(detail["context"])
            answer["answer_start"] = detail["start_at"] + tag_padding
            answers.append(answer)
            qa["answers"] = answers
            qas.append(qa)
            num += 1    #  計算數量
        except:
            print(1)
    paragraph["qas"] = qas
    paragraphs.append(paragraph)
    data["paragraphs"] = paragraphs
    AllData.append(data)


    result["data"] = AllData

    return result

# 更新結果資料
def UpdateResult(test, result):
    global num

    data = {}
    title = test["context"]
    titleList = re.split(r"[,，]", title)           # 以,或，將文章切割
    data["title"] = titleList[0]                    # 取第一句當標題
    id = 10000 + len(result["data"])
    data["id"] = str(id)
    paragraphs = []
    paragraph = {}
    context = test["context"]
    paragraph["context"] = context
    paragraph["id"] = str(id) + "-1"
    qas = []
    for index, detail in enumerate(test["question_detail"]):
        qa = {}
        qa["id"] = str(id) + "-1-" + str(index+1)
        qa["question"] = detail["question"]
        answers = []
        answer = {}
        answer["id"] = "1"
        answer["text"] = detail["tag"]
        try:
            tag_padding = context.index(detail["context"])
            answer["answer_start"] = detail["start_at"] + tag_padding
            answers.append(answer)
            qa["answers"] = answers
            qas.append(qa)
            num += 1    #  計算數量
        except:
            print(1)

    paragraph["qas"] = qas
    paragraphs.append(paragraph)
    data["paragraphs"] = paragraphs
    result["data"].append(data)

    return result

# 有些context和tag對不上，所以要檢查，並校正
def regulate_data(test):
    global num2
    global num3
    n = 0
    result = {}

    try :
        result["context"] = test["context"]
        a = []
        for index_1, detail_1 in enumerate(test["question_detail"]):
            num3 += 1
            n += 1
            regulate_T_F = 0        #定義是否校正成功
            for index_2, detail_2 in enumerate(test["question_detail"]):
                if  regulate_T_F:
                    continue
                try :
                    if detail_1["start_at"] == detail_2["context"].index(detail_1["tag"], detail_1["start_at"]):
                        answer = {}
                        answer["tag"] = detail_1["tag"]
                        answer["start_at"] = detail_1["start_at"]
                        answer["question"] = detail_1["question"]
                        answer["context"] = detail_2["context"]
                        a.append(answer)
                        regulate_T_F = 1
                        num2 += 1
                except:
                    continue  
        print(n)
    except:
        print("有問題")
    
    
    result["question_detail"] = a

    return result

if __name__ == '__main__':
    n = 0
    execute = 1
    path = os.getcwd()  # 當前路徑

    # Python读取文件夹下的所有文件，參考網站:https://blog.csdn.net/LZGS_4/article/details/50371030
    try:
        filepath = path + "/data" #文件夹目录
        files = os.listdir(filepath) #得到文件夹下的所有文件名称
    except:
        execute = 0
        print("系統找不到指定的路徑")
    
    
    if execute:

        result_T_F = 0
        try:
            result = LoadJson(path + '/Example.json')
            result_T_F = 1
        except:
            result_T_F = 0

        for file in files: #遍历文件夹
            if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
                print(file)
                n += 1
                test = LoadJson(filepath + '/' + file)
                if result_T_F:
                    result = UpdateResult(regulate_data(test), result)
                else:
                    result = createResult(regulate_data(test))
                    result_T_F = 1
            
        SaveJson(path + "/Example.json", result)
        print("總文件數量:" + str(n))
        print("原本總數量:" + str(num3))
        print("校正後總數量:" + str(num2))
        print("產出總數量:" + str(num))