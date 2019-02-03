from tkinter import *
from random import *
import time
import datetime
from PIL import Image, ImageTk
from sort import *

houses = ["gryffindor","slytherin","hufflepuff","ravenclaw"] #house names
colors = ["red"       ,"green"    ,"yellow"    ,"cyan"] #respective colors for fonts
pic_width    = 600
pic_height   = 360
my_font      = "Harry P"
my_font_size = 140


end_time = 1534055400 #epoch time for August 12th at 2:25am



#function to build the scoreboard in Tkinter
def make_scoreboard(root, houses, colors, alignment, photos):
  score         = {}
  member_count  = {}
  bottom_row = Frame(root,bg="black")
  bottom_row.pack(side=BOTTOM,fill=X,padx=5,pady=5)
  
  bottom_row_label = Frame(root,bg="black")
  member_count_lab = Label(bottom_row_label,text="Member Count:",fg="white",bg="black",font=(my_font,20))
  bottom_row_label.pack(side=BOTTOM,fill=X,padx=5,pady=5)
  member_count_lab.pack(side=LEFT)
  
  for ii in range(int(len(houses)/2)):
    row1          = Frame(root,bg="black")
    row2          = Frame(root,bg="black")
    
    score1        = Label(row2,text="0",font=(my_font,my_font_size),fg=colors[2*ii],bg="black",width=3)
    pic1          = Label
    score_up1     = Button(row1, text="+1",padx=20,fg=colors[2*ii],bg="black",command=(lambda l = score1: add_lab(l)))
    score_down1   = Button(row1, text="-1",padx=20,fg=colors[2*ii],bg="black",command=(lambda l = score1: sub_lab(l)))
    pic1          = Label(row2,image=photos[ii*2],width=pic_width,height=pic_height)
    
    score2        = Label(row2,text="0",font=(my_font,my_font_size),fg=colors[2*ii+1],bg="black",width=3)
    score_up2     = Button(row1, text="+1",padx=20,fg=colors[2*ii+1],bg="black",command=(lambda l = score2: add_lab(l)))
    score_down2   = Button(row1, text="-1",padx=20,fg=colors[2*ii+1],bg="black",command=(lambda l = score2: sub_lab(l)))
    pic2          = Label(row2,image=photos[ii*2+1],width=pic_width,height=pic_height)
    
    row1.pack(side=alignment[ii], fill=X, padx=5, pady=5)
    score_down1.pack(side=LEFT, fill=X, padx=5)
    score_up1.pack(side=LEFT, padx=5)
    score_up2.pack(side=RIGHT, padx=5)
    score_down2.pack(side=RIGHT, fill=X, padx=5)
    
    row2.pack(side=alignment[ii], fill=X, padx=5, pady=5)
    score1.pack(side=LEFT)
    score2.pack(side=RIGHT)
    pic1.pack(side=LEFT)
    pic2.pack(side=RIGHT)
    
  
    score[houses[ii*2]] = score1["text"]
    
    score[houses[ii*2+1]] = score2["text"]
    

  mem_num = {}
  for ii in range(len(houses)):
    mem_num[houses[ii]]   = Label(bottom_row,text="1",font =(my_font,20),fg=colors[ii],bg="black",width=2)
    mem_up    = Button(bottom_row,text="+1",padx=10,fg=colors[ii],bg="black",command=(lambda l = mem_num[houses[ii]]: add_lab(l)))
    mem_down  = Button(bottom_row,text="-1",padx=10,fg=colors[ii],bg="black",command=(lambda l = mem_num[houses[ii]]: sub_lab(l)))
    mem_down.pack(side=LEFT, padx=(30,5))
    mem_num[houses[ii]].pack(side=LEFT)
    mem_up.pack(side=LEFT, padx=(5,30))
    member_count[houses[ii]] = mem_num[houses[ii]]["text"]
  sort_button = Button(bottom_row,text="SORT NEW PERSON",padx=10,fg="white",bg="black",command=(lambda num_mems = mem_num: sort_new_person(num_mems)))
  sort_button.pack(side=RIGHT)
  return [score,member_count]

  
#Function to sort new person and update GUI 
def sort_new_person(num_members):
  members = []
  house_nums = [0,1,2,3]
  for ii in range(len(num_members)):
    members = members + [int(num_members[houses[ii]]["text"])]
  [members,house_nums] = sort_list(members,house_nums)
  new_member_house = pick_house(members,house_nums)
  #CALL SORT FUNCTION TO ANNOUNCE HOUSE
  sort(new_member_house)
  num_members[houses[new_member_house]]["text"] = str(int(num_members[houses[new_member_house]]["text"])+1)
  
#Randomly chooses house based on Mikey's algorithm 
def pick_house(current_nums,current_houses):
  if(sum(current_nums) < 8):
    max_dif = 1
  else:
    max_dif = 2

  if(max(current_nums)-min(current_nums) < max_dif):
     house = randint(0,3)
  elif(max(current_nums[1:])-min(current_nums[1:]) < max_dif):
     house = randint(1,3)
  elif(max(current_nums[2:])-min(current_nums[2:]) < max_dif):
     house = randint(2,3)
  else:
     house = 3
  return current_houses[house]


#Adds 1 to label input
def add_lab(lab):
  score = lab["text"]
  lab["text"] = str(int(score)+1)
  
#Subtracts 1 from label input
def sub_lab(lab):
  score = lab["text"]
  lab["text"] = str(int(score)-1)
  
  
#Sorts list of values and respective associations
def sort_list(values, association):
  new_values      = []
  new_association = []
  while(len(new_values) < 4):
    high = find(values,max(values))
    new_values = new_values + [values[high]]
    new_association = new_association + [high]
    values[high] = -100
  return new_values, new_association
  

#Finds index of value in list of numbers  
def find(nums, val):
  for ii in range(len(nums)):
    if nums[ii] == val:
      return ii
  return -1
  
  
#Function to update countdown timer every second
def countdown_timer():
  countdown["text"] = str(datetime.timedelta(seconds= (end_time - int(time.time()))%(60*60*24)))
  root.after(1000,countdown_timer)



#Main function
if __name__ == "__main__":
  res_pic_width  = pic_width
  res_pic_height = pic_height
  root = Tk()
  root.title("Harry Potter Scoreboard")
  root.configure(bg="black")
  gryff_pic = Image.open("house_pics/gryff_pic.jpg")
  gryff_pic = gryff_pic.resize((res_pic_width,res_pic_height),Image.ANTIALIAS)
  gryff_pic = ImageTk.PhotoImage(gryff_pic)
  slyth_pic = Image.open("house_pics/slyth_pic.jpg")
  slyth_pic = slyth_pic.resize((res_pic_width,res_pic_height),Image.ANTIALIAS)
  slyth_pic = ImageTk.PhotoImage(slyth_pic)
  huff_pic  = Image.open("house_pics/huff_pic.jpg")
  huff_pic  = huff_pic.resize((res_pic_width,res_pic_height),Image.ANTIALIAS)
  huff_pic  = ImageTk.PhotoImage(huff_pic)
  raven_pic = Image.open("house_pics/raven_pic.jpg")
  raven_pic = raven_pic.resize((res_pic_width,res_pic_height),Image.ANTIALIAS)
  raven_pic = ImageTk.PhotoImage(raven_pic)

  [scores,member_counts] = make_scoreboard(root,houses,colors,[TOP,BOTTOM],[gryff_pic,slyth_pic,huff_pic,raven_pic])
  
  #Make countdown timer
  countdown = Label(root,text="",font =(my_font,48),fg="white",bg="black",anchor="center")
  countdown.pack()
  root.after(1000,countdown_timer)
  
  root.mainloop()
