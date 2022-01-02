from os import system
import requests
from random import randint, uniform, choice
import urllib.request
import time
from hangmanAssets import *

def rgb(r,g,b): return f'\033[38;2;{r};{g};{b}m'
r = '\033[0m'
b = '\033[1m'
err = rgb(255,0,0)
dim = rgb(130,169,255)
opt = rgb(80,120,200)
lg = rgb(150,200,255)
inf = rgb(170,190,190)


def clear(): system('clear')
def error(txt): print(err+txt+r)

cmd = ''
parameters = []
def isCmd(c):
  global cmd, parameters, tooManyArgs
  tooManyArgs = False
  stringType = None

  cmd2 = ''
  itr = -1
  for i in cmd:
    itr += 1
    if i == stringType: stringType = None
    if i == "'": stringType = "'"
    if i == '"': stringType = '"'
    if i == ' ' and stringType: 
      cmd2 += '¯'
    else: cmd2 += i

  cmd = cmd2.replace("'",'').replace('"','')

  if len(cmd) > 0:
    if cmd[-1] == ' ': 
      cmd = cmd[:-1]
  parameters = cmd.split(' ')

  if parameters[0] == c:
    valid = True
  else: valid = False


  if parameters[0] == '' and len(parameters) == 1:
    return False
  else:
    try:
      #global tooManyArgs
      if len(parameters) > cmdInfo[parameters[0]]['args'][1] and valid:
        error(f"Unexpected parameter '{parameters[len(cmdInfo[c]['usage'].split(' '))]}'")
        tooManyArgs = True
        return False
      elif len(parameters) < cmdInfo[parameters[0]]['args'][0] and valid:
        tooManyArgs = True
        error(f"Unexpected end of command.")
        return False
      elif valid and tooManyArgs == False:
        return True
    except:
      return False

# end isCmd

variables = {}
def includeVars(t):
  t = t.replace('¯', ' ')
  for i in list(variables):
    t = t.replace(f'@{i}', variables[i])
  return t
    
cmdInfo =  {
  'help': {
    'info': 'Tell what every command does',
    'usage': 'help [command]',
    'args': [1,2]
  },
  'clear': {
    'info': 'Clears history',
    'usage': 'clear',
    'args': [1,1]
  },
  'calc': {
    'info': 'Calculate something',
    'usage': 'calc <expression>'
    ,
    'args': [2,2]
  },
  'source': {
    'info': 'Get the source code of a website',
    'usage': 'source <url> [file]',
    'args': [2,3]
  },
  'set': {
    'info': 'Create or edit a variable',
    'usage': 'set <name> <value>',
    'args': [3,3]
  },
  'variables': {
    'info': 'View all variables',
    'usage': 'variables',
    'args': [1,1]
  },
  'log': {
    'info': 'Print out text',
    'usage': 'log <text>',
    'args': [2,2]
  },
  'translate': {
    'info': 'Translate something using language codes',
    'usage': 'translate <langFrom> <langTo> <text>',
    'args': [4,4]
  },
  'credits': {
    'info': 'View the credits',
    'usage': 'credits',
    'args': [1,1]
  },
  'kitten': {
    'info': 'Generate a kitten image (placekitten.com)',
    'usage': 'kitten [width <height>]',
    'args': [1,3]
  },
  'clock': {
    'info': 'Check the current time and date',
    'usage': 'clock',
    'args': [1,1]
  },
  'random': {
    'info': 'Get a random number between two numbers',
    'usage': 'random <start> <end> [type]',
    'args': [3,4]
  },
  'prompt': {
    'info': 'Change the prompt color.',
    'usage': 'color {list, <color>}',
    'args': [2,2]
  },
  'hangman': {
    'info': 'Can you guess the word before Billy gets... drawn?',
    'usage': 'hangman',
    'args': [1,1]
  },
  'hacker': {
    'info': 'Code the VooShell :O',
    'usage': 'hacker',
    'args': [1,1]
  }
}

colors = {
  'red': err,
  'orange': rgb(255,127,0),
  'yellow': rgb(255,255,0),
  'lime': rgb(0,255,0),
  'green': rgb(0,130,0),
  'cyan': rgb(0,130,140),
  'blue': rgb(0,127,255),
  'navy': rgb(20,20,200),
  'sky': rgb(0,255,255),
  'pink': rgb(255,160,200),
  'magenta': rgb(255,0,255),
  'purple': rgb(135,40,255),
  'white': rgb(255,255,255),
  'light_gray': rgb(170,170,170),
  'gray': rgb(85,85,85),
  'black': rgb(0,0,0)
}

vooPrompt = rgb(0,127,255)

while True:
  cmd = input(b+vooPrompt+'Voo: '+r)
  parameters = []
  tooManyArgs = False

  if isCmd('help'):
    if len(parameters) == 1:
      helpSorted = list(cmdInfo)
      helpSorted.sort()
      for i in helpSorted:
        print(f'{cmdInfo[i]["usage"].replace("[",opt+"[").replace("]",opt+"]"+r).replace("<",dim+"<").replace(">",dim+">"+r).replace("{",lg+"{"+r).replace("}",lg+"}"+r).replace(",",lg+","+r)}:\n {inf}{cmdInfo[i]["info"]}{r}')
    else:
      i = includeVars(parameters[1])
      runHelp = True
      try: 
        i = cmdInfo[i]
        runHelp = True
      except: 
        error(f"Command '{parameters[1]}' doesn't exist.")
        runHelp = False

      if runHelp:
        i = parameters[1]
        print(f'{cmdInfo[i]["usage"].replace("[",opt+"[").replace("]","]"+r).replace("<",dim+"<").replace(">",">"+r).replace("{",lg+"{"+r).replace("}",lg+"}"+r).replace("|",lg+"|"+r)}: {inf}{cmdInfo[i]["info"]}{r}')





  

  elif isCmd('clear'):
    clear()




  

  elif isCmd('calc'):
    calculation = parameters[1]
    valid = True

    calculation = includeVars(calculation)

    if '**' in calculation:
      error("Unexpected '*'.")
    if '//' in calculation:
      error("Unexpected '/'.")
  
    calculation = calculation.replace('^','**')
    for i in '1234567890':
      calculation = calculation.replace(i+'(',i+'*(')
      calculation = calculation.replace(')'+i,')*'+i)
      
    for i in calculation:
      if i not in '1234567890+-*/()' and valid:
        valid = False
        error(f"Unexpected '{i}'.")

    if valid:
      try:
        result = eval(calculation)
        res2 = '{:,}'.format(result)
        
        print(res2)
        if len(str(result)) > 50:
          print(f'({"{:,}".format(len(str(result)))} digits)')
      except: error('Invalid equation.')




  

  elif isCmd('source'):
    url = includeVars(parameters[1])
    if len(parameters) > 2:
      fileName = includeVars(parameters[2])
    else: fileName = 'code'

    try:
      req = requests.get(url, 'html.parser')
      with open(f'{fileName}.html', 'w') as f:
        f.write(req.text)
        f.close()

      print(f"File named '{fileName}.html' written.")
      
    except:
      if url[:8] == 'https://':
        suggestion = 'Check the spelling of the URL'
      else:
        suggestion = f'Did you mean to type https://{url}?'
      error(f'A problem occurred. {suggestion}')
    



  

  elif isCmd('set'):
    variables[includeVars(parameters[1])] = includeVars(parameters[2])
    print(f"Set variable '{includeVars(parameters[1])}' to '{includeVars(parameters[2])}'.")

  



  

  elif isCmd('variables'):
    if len(variables) == 0:
      print('No variables created.')
    else:
      for i in list(variables):
        print(i+': '+variables[i])
      print('To use a variable, type @variableName.')





  

  elif isCmd('log'):
    print(includeVars(parameters[1]))





  

  elif isCmd('translate'):
    try:
      exec('from translate im'+'port Translator')
    except:
      print('Initializing translator... 1/1')
      system('pip install translate -q -q -q')
      exec('from translate im'+'port Translator')

    try:
      translator= Translator(from_lang=includeVars(parameters[1]), to_lang=includeVars(parameters[2]))
      translation = translator.translate(includeVars(parameters[3]))
    
      if 'IS AN INVALID TARGET LANGUAGE .' in translation:
        error('At least one of the specified languages are invalid. Make sure they are two letter codes.')
      else:
        print(translation)
    except:
      error('A problem occurred.')




  

  elif isCmd('credits'):
    print('Reviving the idea: @joecooldoo')
    print('Translator code:   @Revenger')
    print('Kitten gen idea:   @SwellCoding')
    print('Everything else:   @MrVoo')




  

  
  
  elif isCmd('kitten'):
    tooManyArgs = True
    if len(parameters) == 1:
      link = f'https://placekitten.com/{randint(100,500)}/{randint(100,500)}'
      tooManyArgs = False
        
    else:
      if len(parameters) == 2:
        error(f"Unexpected end of command.")
        tooManyArgs = True
        
      else:
          try:
            parameters[1] = int(parameters[1])
            parameters[2] = int(parameters[2])
            link = f'https://placekitten.com/{parameters[1]}/{parameters[2]}'
            tooManyArgs = False
          except:
            tooManyArgs = True
            error('Width and height must both be integers.')

    if tooManyArgs == False:
      try:
        respond = urllib.request.urlopen(link)
        fileDigits = randint(100,999)
        f = open(b'kitten'+str.encode(str(fileDigits))+b'.jpg','wb')
        f.write(respond.read())
        f.close()
    
        print(f'File named kitten{fileDigits}.jpg written.')
      except:
        error('An error occurred. Make sure the image dimensions are reasonable.')







  elif isCmd('clock'):
    now = time.localtime()
    print(time.strftime('%A, %B %-d, %Y at %-H:%M:%S or %-I:%M:%S %p (UTC+0)',now))
    print(time.strftime('Day of the year: %-j',now))






  elif isCmd('random'):
    try:
      startN = float(parameters[1])
      endN = float(parameters[2])

      try:
        if parameters[3] == 'int':
          print(randint(startN,endN))
        elif parameters[3] == 'float':
          print(uniform(startN,endN))
        else:
          error('Invalid type. Must be "int" or "float"')
      except:
        print(randint(startN,endN))
    except:
      error('Start and end bounds must be numbers.')




  

  elif isCmd('prompt'):
    if parameters[1] == 'list':
      colList = list(colors)
      colList.sort(key=len)
      for i in colors:
        print(f'{i}:{" "*max(0, (len(colList[-1]) - len(i))+1)}{colors[i]}#####{r}')
    else:
      try:
        vooPrompt = colors[parameters[1]]
        print('Color changed.')
      except:
        error("Invalid color. Type 'color list' for help.")








  elif isCmd('hangman'):
    word = choice(wordList)
    guessed = []
    incorrect = []
    guessNum = 0
    while True:
      output1 = word.replace('',' ')[1:-1]
      output2 = ''
      for i in output1:
        if i != ' ':
          if i in guessed:
            output2 += f'{i} '
          else:
            output2 += f'_ '

      if guessNum == 6 or output2.replace(' ','') == word:
        break
      
      print(hmIcons[guessNum])
      print(output2)

      incOutput = str(incorrect).replace('[','').replace(']','').replace("'",'')
      
      print('\nIncorrect guesses: '+ (incOutput if incOutput != '' else ''))
      guess = input('Guess a letter: ').lower()

      if len(guess) == 1:
        if guess in word:
          if guess in guessed:
            print('You already guessed that!')
          else:
            guessed.append(guess)
            print(f'"{guess}" was {colors["lime"]}in the word{r}!')

        elif guess in incorrect:
          print(f'That letter is {err}NOT{r} in the word!\n   ...but you knew that.')

        else:
          guessNum += 1
          print(f'That letter is {err}NOT{r} in the word!')
          incorrect.append(guess)
      else:
        print('Hey, your guess can only be a letter!')

      print('\n============\n')

      if guessNum == 6 or output2.replace(' ','') == word:
        break

    if guessNum == 6:
      print(f'{err}You lost D: \n{hmIcons[6]}The word was "{word}"{r}')
    else:
      print(f'{colors["lime"]}You win :D\nThe word was "{word}"{r}')
    print()









  elif isCmd('hacker'):
    file = open('main.py', 'r').read()
    print(colors['lime'], end='', flush=True)
    for i in file:
      print(i, end='', flush=True)
      time.sleep(0.002)
    print(r)
  
  


  
  else:
    finalCheck = True
    try:
      finalCheck = len(parameters) <= cmdInfo[parameters[0]]["args"][1]
    except:
      pass
      
    if cmd.replace(' ', '') != '' and tooManyArgs == False and finalCheck:
      error(f"Unknown command '{cmd}'. Type 'help' for a list.")