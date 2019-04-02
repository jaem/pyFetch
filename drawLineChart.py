import argparse
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re

## ----------------------------------------------------------------------------
## Main code block
## ----------------------------------------------------------------------------
def main ():
   ## get the command line args
   args = processArgs()
   
   if (args.d):
   	# print some debug stuff
       print(args.csv[0])
       print(args.d)
   
   ## Read the CSV file
   with open(args.csv[0]) as csvFile:
       reader = csv.reader(csvFile)
       data = [r for r in reader]
   
   if (args.d):
       print(len(data))
       print(len(data[0]))
   
   ## Data is loaded, create the plot
   plotOurData(args, data)

## ----------------------------------------------------------------------------
## Methods
## ----------------------------------------------------------------------------
def processArgs():
	## Put all the arg parsing in a method and return the args.
    parser = argparse.ArgumentParser(description='Create chart from CSV data.')

    parser.add_argument('csv', metavar='c', type=str, nargs=1,
                   help='CSV filename')

    parser.add_argument('-d', action="store_true", help='Print debug')

    parser.add_argument('-t', default='ePetition Revoke A50. UK: ', type=str,
                   help='Print debug help')

    parser.add_argument('-x', default=10, type=int,
                   help='X axis tick spacing')

    parser.add_argument('-s', default=6, type=int,
                   help='Starting sample')

    args = parser.parse_args()
    return args

## ----------------------------------------------------------------------------
## 
## ----------------------------------------------------------------------------
def plotOurData(args, data):
   ## form our data to plot
   yaxis  = [re.sub('\:[0-9]{2}\..+', '', data[i][0]) for i in range(args.s,len(data), 1)]
   
   ## as we read from a csv, these are strings, 
   xaxis1 = [int(data[i][1]) for i in range(args.s,len(data))]
   xaxis2 = [int(data[i][3]) for i in range(args.s,len(data))]

   xaxis3 = [((int(data[i][1]) - 0) - (int(data[i-1][1]) - 0)) for i in range(args.s,len(data))]
   xaxis4 = [((int(data[i][3]) - 0) - (int(data[i-1][3]) - 0)) for i in range(args.s,len(data))]
   
   if (args.d):
       print(yaxis)
       print(xaxis1)
       print(xaxis2)
   
   ## plot the data
   fig, ax = plt.subplots()
   ax.set_title(args.t + '{:12,}'.format(int(data[len(data) - 1][3])))
   line1 = ax.plot(yaxis, xaxis1, label="Total Count")
   line2 = ax.plot(yaxis, xaxis2, label="UK Count")
   
   ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
   line3 = ax2.plot(yaxis, xaxis3, label="Total change", color='tab:red')
   line4 = ax2.plot(yaxis, xaxis4, label="UK change", color='tab:olive')
   
   ## add some space at the bottom for the length of the time string
   plt.subplots_adjust(bottom=0.30)
   
   ## Add the legend
   leg = ax.legend(loc='upper left', fancybox=True, shadow=True)
   leg2 = ax2.legend(loc='center right', fancybox=True, shadow=True)
   leg.get_frame().set_alpha(0.4)

   # Once moved to 2 axes, need to use the following method to rotate the tick labels   
   plt.xticks(range(0, len(data), args.x))
   for tick in ax.get_xticklabels():
       tick.set_rotation(90)
      
   plt.show()
   
## ----------------------------------------------------------------------------
## 
## ----------------------------------------------------------------------------
if __name__=="__main__":
   main()

## ----------------------------------------------------------------------------
## The end
## ----------------------------------------------------------------------------

