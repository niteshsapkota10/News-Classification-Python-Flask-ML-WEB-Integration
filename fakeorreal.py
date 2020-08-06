import pickle

def model():
    file=open('trained_algos/fakeorreal/fakemultinomial.pickle','rb')
    mnb=pickle.load(file)
    file.close()
    return mnb
def mnbscore():
    file1=open('trained_algos/fakeorreal/mnbscore.pickle',"rb")
    score=pickle.load(file1)
    file1.close()
    return score

def clfrepmnb():
    file2=open("trained_algos/fakeorreal/classificationreportmnv.pickle","rb")
    repmnb=pickle.load(file2)
    file2.close()
    return repmnb

def cnfmatmnb():
    file3=open("trained_algos/fakeorreal/confusionmatrixmnv.pickle","rb")
    cnfmatrixmnb=pickle.load(file3)
    file3.close()
    return cnfmatrixmnb

def model2():
    file=open('trained_algos/fakeorreal/fakesvm.pickle',"rb")
    svm=pickle.load(file)
    file.close()
    return svm

def svmscore():
    file1=open('trained_algos/fakeorreal/svmscore.pickle',"rb")
    score=pickle.load(file1)
    file1.close()
    return score

def clfrepsvm():
    file3=open('trained_algos/fakeorreal/classificationreportsvm.pickle',"rb")
    repsvm=pickle.load(file3)
    file3.close()
    return repsvm

def cnfmatsvm():
    file4=open('trained_algos/fakeorreal/confusionmatrixsvm.pickle',"rb")
    matrixsvm=pickle.load(file4)
    file4.close()
    return matrixsvm
    