from collections import defaultdict

with open("words.txt", "r") as f:
  text = f.readlines()[0]

wordslist = text.split()

def result(guess, answer):
  outcome = [0 for _ in range(5)]
  for i in range(5):
    if guess[i] == answer[i]:
      outcome[i] = 2
    elif guess[:i].count(guess[i]) < answer.count(guess[i]):
      outcome[i] = 1

  return outcome

def findbestword(wordslist):
  best_guess = ""
  best_E = 1000000
  for guess in wordslist:
    PossibleResults = defaultdict(int)
    for possible_answer in wordslist:
      res = result(guess, possible_answer)
      PossibleResults[str(res)] += 1
    E = sum([res**2 for res in PossibleResults.values()])
    if E < best_E:
      best_E = E
      best_guess = guess

  return best_guess

def removewords(wordslist, guess, hint):
  return [word for word in wordslist if result(guess,word) == hint]

if __name__ == "__main__":
  number = ['first', 'second', 'third','fourth','fifth','sixth','seventh','eighth']
  counter = 0
  running = True
  while running:
    hint = [0,0,0,0,0]
    if len(wordslist) == 0:
      print("Word cannot be found.  An invalid entry was made.")
      break
    elif len(wordslist) == 1:
      bestword = findbestword(wordslist)
      print(f"The correct word is: {bestword.upper()}. \n Solved on {number[counter]} try.")
      break
    else:
      bestword = findbestword(wordslist)
      print(f"The {number[counter]} guess is: {bestword.upper()}")
      print(f"There are {len(wordslist)} possible words left.")

    letter = 0
    while letter <= 4:
      userinput = input(f'Enter color of the {number[letter]} letter; 0 for grey, 1 for yellow, 2 for green, Q to quit: \n')
      if userinput in ['0','1','2']:
        hint[letter] = int(userinput)
        letter += 1
      elif userinput.upper() == 'Q':
        running = False
        break
      else:
        print("Not a valid answer.  Please enter 0, 1, 2 or Q.")

    if hint == [2,2,2,2,2]:
      print(f"The correct word is: {bestword.upper()}. \n Solved on {number[counter]} try.")
      running = False
    counter += 1

    if running:
      wordslist = removewords(wordslist,bestword,hint)