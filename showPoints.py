import sys
import pickle
import utils.plots
import utils.pickle

picklePath = 'points_over_time.pkl'
xlabel = 'Time'
ylabel = 'Points'
title = 'Points Over Time'

if len(sys.argv) > 1:
    picklePath = sys.argv[1]
    ylabel = 'Population'
    title = 'Civilization population over time'


loaded_pointsOverTime = utils.pickle.loadPickle(picklePath)
utils.plots.renderOverTime(loaded_pointsOverTime, xlabel=xlabel, ylabel=ylabel, title=title)
