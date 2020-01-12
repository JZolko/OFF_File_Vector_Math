'''
project 05
This program will read the data off of an 'off' file and calculate values of area and connectivity based on the given data.
The program wil pull the face data from the file and compare it to the corresponding vertex to complete any calculations.
Many of the functions are called within one another to increase efficiency and shorten the code.
'''

#Retain these import statements  
import math

def check_index(index):
    index = str(index)
    try:
        int(index)
        return True
        #index % 1 == 0
    except ValueError:
        return False
    else:
        return True


def display_options():
    ''' This function displays the menu of options'''
    
    menu = '''\nPlease choose an option below:
        1- display the information of the first 5 faces
        2- compute face normal
        3- compute face area
        4- check two faces connectivity
        5- use another file
        6- exit
       '''
       
    return menu
    
def open_file(file):
    '''This function checks to see if the inputed file name actually exists'''
    #file = ('"' + str(file) + '"')
    
    try:
        open(file , 'r')
        return True
        
    except FileNotFoundError:
        return False
    


def check_valid(fp,index,shape):
    '''This will check to see if a face or vertex actually exists in the file using a comparison to the max number of faces and verticies given in the file'''
    final = True
    shape = str(shape)
    shape = shape.replace("'", '')
    
    fp.seek(0) # move to the beginning of the file -- necessary for multiple calls to this function
    fp.readline()
    
    dest = str(fp.readline())
    
    vertex = int(dest[0:5].strip())
    face = int(dest[5:10].strip())
    
    index = str(index)   
    
    if index.isalpha() or not(check_index(index)):
        return False
    else:
        index = float(index)
        if shape.lower() == 'vertex':
            if index >= vertex or index < 0 or (index % 1 != 0):
                final = False        
        if shape.lower() == 'face':
            if index >= face or index < 0 or (index % 1 != 0):
                final = False    
        
        return final

        


def read_face_data(fp, index):
    '''This function pulls the face data from a given index and returns the value as an integer'''
    index = int(index)
    
    fp.seek(0) # move to the beginning of the file -- necessary for multiple calls to this function
    fp.readline()
    
    dest = fp.readline()    #   skips over the OFF line and uses the info from the face andvertex line to skip over more lines until the right index is read
    fp.readline()
    
    vertex = int(dest[0:5].strip())
    #face = int(dest[5:10].strip())
    real = ''
    
    for i in range(vertex-1):   # skips over all the verticies 
        fp.readline()
    
    for i in range(index):  #   jumps to desired face
        fp.readline()
        
    real = fp.readline()        # reads data from desired line
    
    f1 = real[2:7].strip() # splits the three 
    f2 = real[7:12].strip()     #   Uses strip function to get rid of the blank spaces
    f3 = real[12:17].strip()    #   gets the three face data points and stores them in an int
    
    return int(f1), int(f2), int(f3)
    #return dest[0][0]
    
    
def read_vertex_data(fp, index):             
    '''This is similar to the previous function where the coordinates of the x y and z planes are found within the file using a given index and are returned as floats'''
    index = int(index)
    
    fp.seek(0) # move to the beginning of the file -- necessary for multiple calls to this function
    fp.readline() # Skips the first line that says OFF
    
    dest = fp.readline()
    
    
    #vertex = int(dest[0:5].strip())
    #face = int(dest[5:10].strip())

    real = ''
    for i in range(index): #jumps to desired line
        fp.readline()
        
        
    real = fp.readline()    #   Reads data on desired line
    
    v1 = real[0:15].strip()         #   Takes info and moves it into individual tags with a float format. will return these values
    v2 = real[15:30].strip()
    v3 = real[30:45].strip()

    #return dest[0][0]

    
    return float(v1), float(v2), float(v3)
        
def compute_cross(v1,v2,v3,w1,w2,w3):
    '''This function finds the cross product of 2 given faces'''
    f_1 = float(v2*w3 - v3*w2)  #Does some math
    f_2 = float(v3*w1 - v1*w3)#Does some math
    f_3 = float(v1*w2 - v2*w1)#Does some math
    return round(f_1, 5),round(f_2, 5),round(f_3, 5)    #returns the cross products with a float length of 5
    
def compute_distance(x1,y1,z1,x2,y2,z2):
    '''This calculates the distance from one vertex to another'''
    D = math.sqrt((((x1-x2)**2)+((y1-y2)**2)+((z1-z2)**2))) #Does some math
    
    return round(D, 2) # returns that math into a float with a length of 2

def compute_face_normal(fp, face_index):
    '''This calculates the perpendicular vector to two diffeerent vectors'''
    f1, f2, f3 = read_face_data(fp, int(face_index))
    
    va, vaa, vaaa = read_vertex_data(fp, f1)    # i used an array for this the first time, but I dont want reduced points
    vb, vbb, vbbb = read_vertex_data(fp, f2)    # gets data and moves it into approptiately named tags
    vc, vcc, vccc = read_vertex_data(fp, f3)    # these are then referenced below to be used in more math
     
    ab1, ab2, ab3 = (float(vb) - float(va)), (float(vbb) - float(vaa)), (float(vbbb) - float(vaaa)) # dummy ugly code, but it works to get the normal
    ac1, ac2, ac3 = (float(vc) - float(va)), (float(vcc) - float(vaa)), (float(vccc) - float(vaaa))
    
    nv1, nv2, nv3 = compute_cross(ab1, ab2, ab3, ac1, ac2, ac3)
    
    return round(nv1, 5), round(nv2, 5), round(nv3, 5)  # returns the normal value in 3 floats of lenth 5

def compute_face_area(fp, face_index):
    ''' This calculates the area of a face and returns a rounded float'''
    f1, f2, f3 = read_face_data(fp, int(face_index))
    
    va, vaa, vaaa = read_vertex_data(fp, f1)    # does some math to get the area of the individual triangle
    vb, vbb, vbbb = read_vertex_data(fp, f2)
    vc, vcc, vccc = read_vertex_data(fp, f3)
    
    ab = compute_distance(va, vaa, vaaa, vb, vbb, vbbb)     # gets length of specific vector
    ac = compute_distance(va, vaa, vaaa, vc, vcc, vccc)
    bc = compute_distance(vb, vbb, vbbb, vc, vcc, vccc)
    
    p = (ab + ac + bc)/2
    
    area = math.sqrt(p*(p-ab)*(p-ac)*(p-bc)) # more math that gets the final area of the face
    return round(area, 2)

def is_connected_faces(fp, f1_ind, f2_ind):
    '''This checks the two inputed faces to check for any two connecting points and returns a bool'''
    f1_1, f1_2, f1_3 = read_face_data(fp, f1_ind)
    f2_1, f2_2, f2_3 = read_face_data(fp, f2_ind)
    f1_connect, f2_connect, f3_connect = False, False, False
    
    f1_1, f1_2, f1_3 = int(f1_1), int(f1_2), int(f1_3)
    f2_1, f2_2, f2_3 = int(f2_1), int(f2_2), int(f2_3)
    
    if f1_1 == f2_1 or f1_1 == f2_2 or f1_1 == f2_3: # relates all the sides and goes true if theyre touching
        f1_connect = True
    
    if f1_2 == f2_1 or f1_2 == f2_2 or f1_2 == f2_3:
        f2_connect = True
    
    if f1_3 == f2_1 or f1_3 == f2_2 or f1_3 == f2_3:
        f3_connect = True
    
    if (f1_connect and f2_connect) or (f1_connect and f3_connect) or (f2_connect and f3_connect): # if more than one node is touching then the function returns true
        return True
    else:      
        return False


 
         
def main():
     '''The main is essentially what the user sees when selecting options to calculate data using the functions'''
     
     print('''\nWelcome to Computer Graphics!
    We are creating and handling shapes. Any shape can be represented by polygon meshes, 
    which is a collection of vertices, edges and faces.''')
     
     file_name =input("Enter an <off> file name: ")
        
     
     check = open_file(file_name) # checks to see if the file is valid and then prompts until true
     
     while not(check):
         print("Error. Please try again.")
         file_name =input("Enter an <off> file name: ")
         break
     option = '1'
     
     #print(display_options())
     #option = input()
     
     acceptable = ['1','2','3','4','5','6']
     print(display_options())
     while option:
         
         
         option = input(">> Choice: ")
     
         while not(option in acceptable):   # if the input isnt valid it asks for another input
             print('Please choose a valid option number.')
             #option = input(">> Choice: ")
             break
        
         
         if option == '1':       #   display info of first 5 faces
             f = []
             index = ['0', '1', '2', '3', '4']
             fp = open(file_name, 'r')
     
             for i in range(5): #condenses a bunch of variables into one array
                 f.append(read_face_data(fp,i))
     
             print("{:^7s}{:^15s}".format('face','vertices'))
             
             
             for i in range(len(f)):
                  print('{:>5}{:>5}{:>5}{:>5}'.format(index[i], str(f[i][0]), str(f[i][1]), str(f[i][2]))) # prints a bunch of faces
 
             print(display_options()) # displays menu for some more options
             

             
         elif option == '2':       #   compute face normal
             #print(">> Choice: {}".format(option))
             face_num = input("Enter face index as integer: ")  # these test to see if the inputs are actually valid and wont continue until theyre valid
             
             test = open(file_name, 'r')            
             valid_bool = check_valid(test, face_num, 'face')
             #face_num = str(face_num)
             is_real = check_index(face_num)
            
             # sets limits for acceptable inputs
             while face_num.isalpha() or not(face_num.isdigit()) or not(valid_bool) or\
             not(float(face_num) % 1 == 0) or not(is_real):
             
                 #while not(check_index(face_num) or not(face_num % 1 == 0)):    
                 print("This is not a valid face index.")
                 face_num = input("Enter face index as integer: ")
                 is_real = check_index(face_num)
                 valid_bool = check_valid(test, face_num, 'face')
                 #break
             
             else:
                 fp = open(file_name, 'r')
                 f_norm = []
                 f_norm = compute_face_normal(fp, face_num)
                 print("The normal of face {}:{:>9.5f}{:>9.5f}{:>9.5f}".format(str(face_num), f_norm[0], f_norm[1], f_norm[2])) # prints the normal for the face
                 
                 print(display_options())
                 
         elif option == '3':       #   compute area
             #print(">> Choice: {}".format(option))
             face_num = input("Enter face index as integer: ")
             
             test = open(file_name, 'r')            
             valid_bool = check_valid(test, face_num, 'face')
             is_real = check_index(face_num)
             
             
             # Checks the input and if its invalid, it prompts until its valid
             while face_num.isalpha() or not(face_num.isdigit()) or not(valid_bool) or\
             not(float(face_num) % 1 == 0) or not(is_real):
                
                 print("This is not a valid face index.")
                 face_num = input("Enter face index as integer: ")
                 is_real = check_index(face_num)
                 valid_bool = check_valid(test, face_num, 'face')
             
             else:
                 fp = open(file_name, 'r')
                 f_norm = compute_face_area(fp, face_num)
                 print("The area of face {}:{:>9.2f}".format(str(face_num), f_norm)) # computes area and prints
                 print(display_options()) # displays menu for next choice
         
            
         elif option == '4':       #   check for two face connectivity
             #print(">> Choice: {}".format(option))
             
             face_1 = input("Enter face 1 index as integer: ")
             
             test = open(file_name, 'r')            
             
             valid_bool = check_valid(test, face_1, 'face')
             is_real = check_index(face_1)
             
             
             # Checks the input and if its invalid, it prompts until its valid
             while face_1.isalpha() or not(face_1.isdigit()) or not(valid_bool) or\
             not(float(face_1) % 1 == 0) or not(is_real):
             
                 #while not(check_index(face_num) or not(face_num % 1 == 0)):    
                 print("This is not a valid face index.")
                 face_1 = input("Enter face 1 index as integer: ")
                 is_real = check_index(face_1)
                 valid_bool = check_valid(test, face_1, 'face')
                 
             
             else:
                 face_2 = input("Enter face 2 index as integer: ")
                 
                 
                 test = open(file_name, 'r')
                 
                 valid_bool = check_valid(test, face_2, 'face')
                 
                 is_real = check_index(face_2)    
                 
                 
                 # Checks the input and if its invalid, it prompts until its valid
                 while face_2.isalpha() or not(face_2.isdigit()) or not(valid_bool) or\
                 not(float(face_2) % 1 == 0) or not(is_real):
             
                     #while not(check_index(face_num) or not(face_num % 1 == 0)):    
                     print("This is not a valid face index.")
                     face_2 = input("Enter face 2 index as integer: ")
                     is_real = check_index(face_2)
                     valid_bool = check_valid(test, face_2, 'face')
                 
                 else:
                     fp = open(file_name, 'r')
                     connected = is_connected_faces(fp, face_1, face_2)
                     
                     if connected:
                         print("The two faces are connected.") # compares the two faces and returns a bool accordingly
                         print(display_options())
                         
                     else:
                         print("The two faces are NOT connected.")
                         print(display_options())
                         
         
         if option == '5':       #   use another file
             #print(">> Choice: {}".format(option))
             file_name = input("Enter an <off> file name: ") #  if the use wants to change files without restarting the program
             is_real = open_file(file_name)
             
             while not(is_real):
                 print("Error. Please try again")
                 file_name = input("Enter an <off> file name: ")        # Makes the user enter  file until the file is valid
                 is_real = open_file(file_name)      # uses the open_file() function to see if the file actually exists 
             
             else:
                 file_name = file_name # updates file
                 print(display_options())
                 
                     
                 
                    
         if option == '6':       #   exit
             print("Thank you, Goodbye!")  # breaks and prints message if the use doesn't want to continue
             break
             
             
     
# Do not modify the next two lines.
if __name__ == "__main__":
     main()
 
