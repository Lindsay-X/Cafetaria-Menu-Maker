class School: # parent class
    # class with all the attributes everyone in the school has in common
    def __init__(self, firstName, lastName, id):
        self.firstName = firstName
        self.lastName = lastName
        self.id = id

class Student(School): # child class
    def __init__(self, fn, ln, id, grade): # overriding School’s initialization
        super().__init__(fn, ln, id) # inheritance
        self.grade = grade

    def __str__(self): # override of built-in method
        return "Student: %s %s %s in Grade %d" % (self.firstName, self.lastName, self.id, self.grade)
    
    def __repr__(self): # override of built-in method
        return self.__str__
    
    def __eq__(self, person2): # override of built-in method
        if self.firstName == person2.firstName and self.lastName == person2.lastName and self.id == person2.id and self.grade == person2.grade:
            return True
        else:
            return False


class Teacher(School): # child class
    def __init__(self, fn, ln, id):
        super().__init__(fn, ln, id) # inheritance
        
    def __str__(self): # override of built-in method
        return "Teacher: %s %s %s" % (self.firstName, self.lastName, self.id)
    
    def __repr__(self): # override of built-in method
        return self.__str__
    
    def __eq__(self, person2): # override of built-in method
        if self.firstName == person2.firstName and self.lastName == person2.lastName and self.id == person2.id:
            return True
        else:
            return False

class Food: # all the individual foods
    def __init__(self, name, price, amountMade):
        self.name = name
        self.price = price
        self.amount = amountMade
    
    def __str__(self): # override of built-in method
        txt = "{}: ${:.2f}".format(self.name, self.price) # .2f --> rounds to 2nd decimal
        return txt
    
    def __repr__(self): # override of built-in method
        return self.__str__

    def __eq__(self, food2): # override of built-in method
        if self.name == food2.name:
            return True
        else:
            return False

class FoodMenu:
    def __init__(self, peopleNum):
        self.peopleNum = peopleNum # number of people in the school
        self.menu = [] # used for recursion
        self.finalMenu = [] 
        self.pastData = [] # ensure no repeat of meals on consecutive days

        self.main = self.__getPrice("./MainMeal.txt")
        self.side = self.__getPrice("./Side.txt")
        self.dessert= self.__getPrice("./DessertAndSnack.txt")
        self.main.sort(key = lambda x: x.price, reverse = True) # sorting based on price from greatest to smallest
        self.side.sort(key = lambda x: x.price, reverse = True)
        self.dessert.sort(key = lambda x: x.price, reverse = True)

    def __getPrice(self, fileName):
        potenMenu = []
        with open(fileName, "r") as file_obj: # r --> reading
            for x in file_obj.readlines(): # reading through each line on the file as a string
                f = x.replace("\n", "").split(": ") # list 
                f = Food(f[0], float(f[1]), int (self.peopleNum/2 + 1))
                potenMenu.append(f)
        
        return potenMenu
    
    def setMenu(self, budget, save):
        self.budget = budget
        self.save = save

        self.__setter(0)
        for food in self.finalMenu:
            self.budget -= food.price * (food.amount)
            self.pastData.append(food)
    
    def __setter(self, num): # recursion 
        if self.budget >= self.save and num == 6:
            if not self.finalMenu:
                self.finalMenu = tuple(self.menu) # tuples are immutable
            return

        x = 0
        temp = []
        if num == 0 or num == 1:
            x = len(self.main)
            temp = self.main
        elif num == 2 or num == 3:
            x = len(self.side)
            temp = self.side
        else:
            x = len(self.dessert)
            temp = self.dessert
        

        for i in range(x): # backtracking
            pastBudget = self.budget
            self.budget -= round(temp[i].price*0.85, 2) * (temp[i].amount)
            if temp[i] in self.pastData[-6:] or temp[i] in self.menu or self.budget < self.save: # ensures no repeat meals from day before, no duplicates in current menu, and enough money for next day
                continue
            self.menu.append(temp[i])
            self.__setter(num+1)
            self.menu.remove(temp[i]) # recovering the list for next combo
            self.budget = pastBudget
    
    def displayMenu (self):
        for num in range(len(self.finalMenu)):
            if num == 0:
                print("\nMAIN MEAL")
            elif num == 2:
                print("\nSIDE DISH")
            elif num == 4:
                print("\nDESSERT/SNACK")

            txt = "{} ({})".format(self.finalMenu[num], (num%2 + 1))
            print(txt)

class Cafetaria:
    def __init__(self, money):
        self.validStudent = self.__getStudents()
        self.validTeacher = self.__getTeachers()
        self.money = money
        self.peopleNum = len(self.validStudent) + len(self.validTeacher)
        self.menu = FoodMenu(self.peopleNum)

    def __getStudents(self):
        tempStu = []
        with open("./Student.txt", "r") as file_obj: # r --> reading
            for person in file_obj.readlines(): # reading through each line on the file as a string
                stu = person.replace("\n", "").replace(":","").split(" ") # list 
                stu = Student(stu[0], stu[1], stu[2], int(stu[3]))
                tempStu.append(stu)

        return tempStu

    def __getTeachers(self):
        tempTeach = []
        with open("./Teacher.txt", "r") as file_obj: # r --> reading
            for person in file_obj.readlines(): # reading through each line on the file as a string
                teach = person.replace("\n", "").replace(":","").split(" ") # list
                teach = Teacher(teach[0], teach[1], teach[2])
                tempTeach.append(teach)

        return tempTeach

    def newDay(self, save):
        self.menu.setMenu(self.money, save)
        self.money = self.menu.budget
        self.menu.displayMenu()
        self.lunchHour()
        txt = "There is ${:.2f}".format(self.money)
        print("There is $", txt)

    def lunchHour(self):
        identity = input("\nTeacher or Student or End Lunch Period(t/s/e): ")[0].lower()

        while(identity != "e"):
            name = input("Full Name: ").split(" ")
            id = input("ID: ")
            payment = 0

            if identity == "t":
                teach = Teacher(name[0], name[1], id)
                if teach in self.validTeacher:
                    payment = round(self.purchase()*0.90, 2)
                    print("\nThe total price is $", payment)
                else:
                    print("\nInvalid: teacher is not in the system")

            else:
                grade = input("Student's grade: ")
                stu = Student(name[0], name[1], id, int(grade))
                if stu in self.validStudent and stu.grade == 9:
                    payment = round(self.purchase()*0.90, 2)
                    print("\nThe total price is $", payment)
                elif stu in self.validStudent and stu.grade != 9:
                    payment = self.purchase()
                    print("\nThe total price is $", payment)
                else:
                    print("\nInvalid: student is not in the system")

            self.money += payment

            identity = input("\nTeacher or Student or End Lunch Period (t/s/e): ")[0].lower()
        
    def purchase(self):
        payment = 0
        for i in range(3):
            if i==0:
                category = "Main Meal (1/2): "
            elif i==1:
                category = "Side Meal (1/2): "
            else:
                category = "Dessert/Snack (1/2): "

            meal = int(input(category)) 
            while(meal>2):
                meal = int(input("Invalid, try again: "))

            meal = self.menu.finalMenu[meal + i*2 - 1]
            if meal.amount <= 0:
                print("There is no more", meal.name)
                i -= 1
            else:
                meal.amount -= 1
                payment += meal.price
            
            txt = "${:.2f}".format(payment)
            print(txt)
        return payment
        
c = Cafetaria(800)

cmd= input("Start day or end all (s/e)? ").lower()[0]
while(cmd == "s"):
    num = int(input("Before starting to make the menu, how much money must be left? "))
    c.newDay(num)
    cmd= input("Start day or end all? (s/e)").lower()[0]


""" 
Inputs:
-s
-50

- s
- Rimuru Tempest
- 969
- 9
- 1
- 3
- 2
- 2

- student
- Mavis Vermillion
- 976
- 12
- 1
- 2
- 2

- s
- Peppa Pig
- 432
- 100

- t
- Rick Roll
- 121
- 1
- 1
- 1

- e
"""