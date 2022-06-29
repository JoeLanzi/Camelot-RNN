from IPython import display
import matplotlib.pyplot as plt

def plot(stat):
    display.display(plt.gcf())
    display.clear_output(wait=True)
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Steps')
    plt.ylabel('Scores')
    plt.plot(stat[0])
    plt.plot(stat[1])
    plt.plot(stat[2])
    plt.plot(stat[3])
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.text(len(stat[0])-1,stat[0][-1],'health:'+str(stat[0][-1]))
    plt.text(len(stat[1])-1,stat[1][-1],'hunger:'+str(stat[1][-1]))
    plt.text(len(stat[2])-1,stat[2][-1],'energy:'+str(stat[2][-1]))
    plt.text(len(stat[3])-1,stat[3][-1],'wealth:'+str(stat[3][-1]))
    plt.show(block=False)
    plt.pause(.01)