from simulation_agent.civilization_type import CivilizationType
import matplotlib.pyplot as plt
import pickle

def renderOverTime(data, xlabel='Time', ylabel='Points', title='Points Over Time'):
    for civilizationType, points in data.items():
        if civilizationType == CivilizationType.RED:
            civilizationName = 'red'
            color = 'red'
        elif civilizationType == CivilizationType.BLUE:
            civilizationName = 'blue'
            color = 'blue'
        else:
            civilizationName = '???'
            color = 'yellow'
        
        plt.plot(points, label=civilizationName, color=color)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.legend()

    plt.show()
