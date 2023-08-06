import sys, os

def hit(anything):
  """
  The same as printing but much cooler 😎
  """
  try:
    print(anything)
    
  except:
    print("Something went wrong! 😔")

def die(message):
  """
  Exit the program but much cooler 😎
  """
  try:
    sys.exit('\033[31m' + message + '\033[0m')

  except:
    print("Something went wrong! 😔")

def bye():
  """
  Note: Only works for windows (i think)\n
  Restart your computer but much cooler 😎
  """
  try:
    os.system("shutdown /s /t 1")
  
  except:
    print("Something went wrong! 😔 Are you on windows?")