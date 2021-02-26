from pyfiglet import Figlet
import os 
import database
import time
from getpass import getpass
import sys
from account import Account
f = Figlet()

def clear():
    os.system('cls')

def render_startup():
    clear()
    
    print()
    print("               Welcome To               ")
    print('\033[92m' + f.renderText('Bamboo') + '\033[0m')
    print("       The Open-Source Mutual Fund       ")
    print("         (c) Rishabh Misra | 2021         ")
    print()

    print('\033[95m' + "1: Log In" + '\033[0m')
    print('\033[95m' + "2: Create Account" + '\033[0m')
    print()
    choice = int(input("Please Enter Choice: "))
    if choice == 1:
        login()
    elif choice == 2:
        create_account()
    

def login():
    clear()
    print('\033[93m' + f.renderText('Login') + '\033[0m')
    username = input("Username: ")
    password = getpass("Password: ")

    account = database.get_account(username, password)

    if(account == -1):
        for i in range(5):
            time.sleep(1)
            sys.stdout.write(u"\u001b[2000D" + '\033[91m' + "Incorrect username and/or password. Retrying login in " + str(5-i)  + '\033[0m')
            sys.stdout.flush()
        
        return login()
    
    else:
        print('\033[92m' + "Success! Redirecting you to your dashboard." + '\033[0m')
        time.sleep(1)
        return dashboard(Account(account['username'], account['password'], account))



def dashboard(account):
    clear()
    print('\033[96m' + f.renderText('Dashboard') + '\033[0m')
    
    print("Welcome, " + account.username + '!')

    print()
    print("ACCOUNT OVERVIEW:")
    print("-----------------")
    earnings = account.get_total_earnings()
    if(earnings > 0):
        color = '\033[92m'
    else:
        color = '\033[91m'
    print(color + "Earnings: $" + str(account.get_total_earnings()) + '\033[0m')
    print("-----------------")
    print("Portfolios: ")
    for i in range(len(account.portfolios)):
        print(str(i+1) + ".) " + account.portfolios[i].name + "; " + 
            "Strategy: " + account.portfolios[i].strategy.name)

    

def create_account():
    clear()
    print('\033[93m' + f.renderText('Create Account') + '\033[0m')
    username = input("Username: ")

    if(database.username_in_db(username)):
        print('\033[91m' + "Username already taken! Please choose a new username." + '\033[0m')
        time.sleep(2)
        return create_account()

    password = getpass("Password: ")
    check_password = getpass("Re-Enter Password: ")

    if password != check_password:
        print('\033[91m' + "Password don't match. Please try again." + '\033[0m')
        time.sleep(2)
        return create_account()

    acc = Account(username, password)
    database.add_account(acc)

    print('\033[92m' + "Account Creation Success! Redirecting you to your dashboard." + '\033[0m')
    time.sleep(1)
    
    acct = database.get_account(username, password)
    return dashboard(Account(username, password, acct))

render_startup()

print()