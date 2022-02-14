from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import time
import keyboard
import pyautogui

def ifSolved(grid):
    for x in range  (0,9):
        for y in range (0,9):
            if grid[x][y] == 0:
                return x,y
    return -1, -1

def Valid(grid, i, j, e):
    validrow = all([e != grid[i][x] for x in range(9)])
    if validrow:
        validcol = all([e != grid[x][j] for x in range(9)])
        if validcol:
            sectionx, sectiony = 3*(i//3), 3*(j//3)
            for x in range(sectionx, sectionx + 3):
                for y in range(sectiony, sectiony + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False

def solve(grid, i=0, j=0):
    i, j = ifSolved(grid)
    if i == -1:
        return True

    for e in range(1,10):
        if Valid(grid, i, j, e):
            grid[i][j] = e
            if solve(grid, i, j):
                return True
            grid[i][j] = 0
    return False

def sudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print(" ")
        print(row[0:3]," ",row[3:6], " ", row[6:9])
        numrow += 1
    return

browser = webdriver.Chrome(ChromeDriverManager().install())


browser.get("https://sudoku.puzzlebaron.com/init.php?d=e") 
default_delay = 1


while True:
    if keyboard.is_pressed('q'):
        break
        
while True:
    start_button = browser.find_element_by_class_name("button_orange")
    start_button.click()
    time.sleep(default_delay)
    
    sudoku_table = browser.find_element_by_id("sudoku")
    numbers = []
    
    rows = sudoku_table.find_elements_by_css_selector('tr')
    for r in range(len(rows)):
        if r % 4 == 0: continue
        row = rows[r]
        
        elements = row.find_elements_by_tag_name('td')
        
        for c in range(len(elements)):
            if c % 4 == 0: continue
            cell = elements[c]
            num = 0 if cell.text == '' else int(cell.text)
            numbers.append(num)
      
    unknown = [num == 0 for num in numbers]
    
    numbers = np.reshape(numbers, (9, 9))
    
    solve(numbers)
    numbers = numbers.flatten()
    idk = 0
    
    for r in range(len(rows)):
        if r % 4 == 0: continue
        row = rows[r]
        
        elements = row.find_elements_by_tag_name('td')
        for c in range(len(elements)):
            if c % 4 == 0: continue
        
            if not unknown[idk]:
                idk += 1
                continue
            
            cell = elements[c]
            cell.click()
            keyboard.write(str(numbers[idk]))
            idk += 1
        
    submit_button = browser.find_element_by_class_name("button_green")
    submit_button.click()
    time.sleep(default_delay)
    
    again_button = browser.find_element_by_class_name("button_green")
    again_button.click()
    
    time.sleep(default_delay)
        
    if keyboard.is_pressed('q'):
        break
   
