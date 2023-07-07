from __future__ import print_function

import time
import datetime

import numpy as np
import matplotlib.pyplot as plt

import temp_sens

sensor = temp_sens.temp_sens()

def main():

    print('start')

    tpn, tptat = sensor.readData()

    x = np.arange (1,9)
    y = tpn

    plt.plot(x,y)
    plt.savefig('test.png')
    plt.show()
    
    # while True:
    #         tpn, tptat = sensor.readData()
    #         if tpn != None and tptat != None:
    #             print(datetime.datetime.today().strftime("[%Y/%m/%d %H:%M:%S]"),"temperature=%.1f[degC]" %tptat)
    #             print(tpn[0:4])
    #             print(tpn[4:8])
    #             print(tpn[8:12])
    #             print(tpn[12:16])
                
    #             Z = np.array([tpn[0:4],
    #                       tpn[4:8],
    #                       tpn[8:12],
    #                       tpn[12:16]])

    #             X,Y = np.meshgrid(x, y)
                
    #             plt.clf()
    #             plt.pcolor(X,Y,Z,cmap="coolwarm",vmax=35,vmin=25)
                
    #             if visibleColorBar == False:
    #                 plt.colorbar()
    #                 visibleColorBar = True

    #             plt.xticks(x)
    #             plt.yticks(y)
    #             fig.tight_layout()
    #             fig.canvas.draw()
    #             plt.show()

if __name__ == '__main__':
  main()