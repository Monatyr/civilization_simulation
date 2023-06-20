from simulation_agent.civilization_type import CivilizationType
import matplotlib.pyplot as plt
import pickle

def renderPointsOverTime(pointsOverTime):
    for civilizationType, points in pointsOverTime.items():
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
    
    plt.xlabel('Time')
    plt.ylabel('Points')
    plt.title('Points Over Time')

    plt.legend()

    plt.show()
