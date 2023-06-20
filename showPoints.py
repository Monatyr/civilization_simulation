import sys
import pickle
import utils.plots
import utils.pickle

picklePath = 'points_over_time.pkl'

if len(sys.argv) > 1:
    picklePath = sys.argv[1]

loaded_pointsOverTime = utils.pickle.loadPickle(picklePath)
utils.plots.renderPointsOverTime(loaded_pointsOverTime)
