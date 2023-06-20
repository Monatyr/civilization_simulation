import pickle

def savePickle(path, data):
    with open(path, 'wb') as file:
        pickle.dump(data, file)

def loadPickle(path):
    loaded_pointsOverTime = None

    with open(path, 'rb') as file:
        loaded_pointsOverTime = pickle.load(file)
    
    return loaded_pointsOverTime
