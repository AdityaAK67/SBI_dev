# def ma(a):
    
#     ma1 = int(''.join(sorted(str(a), reverse=True)))
#     return ma1


# print(ma(a = (input("Enter the Number: "))) )


import random as rn
def r(a):
    
 while a==0:
    b = rn.choice(['rock', 'paper', 'scissor'])
    if a == b:
        return 'Tie'
    elif (a == '1' and b == 'scissor') or (a == '2' and b == 'rock') or (a == '3' and b == 'paper'):
        return 'You Win!'
    else:
        return 'You Lose!'
 return "Stopped"
    
print(r(a = (input('1- for rock 2- for paper 3-  for scissor:-   '))) )    
    