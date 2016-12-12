import sys

def Log(log):
    print("Log: " + str(log) + "\n")

def Warn(warn):
    print("Warnning: " + str(warn) + "\n")

def Error(error):
    print("Error: " + str(error) + "\n")
    exit(1)
