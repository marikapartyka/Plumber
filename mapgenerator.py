import random
from GameObjects import Pipe
from GameObjects import PipeType



def generate_map(rows, columns):                    #glowna funkcja, tylko z niej musisz skorzystac zeby generowac mapke, reszta jest pomocnicza
    pipe_list = generate_first_row(columns)
    pipe_list += generate_middle_rows(rows-2,columns)
    pipe_list += generate_last_row(columns)
    return pipe_list #zwraca liste rurek, zeby pasowala do Twojej implementacji mapki

def generate_first_row(columns):
    first_row = [Pipe(PipeType.STRAIGHT,0,True)] +\
                [Pipe(PipeType.EMPTY) for i in range(columns-1)]
    return first_row

def generate_last_row(columns): 
    last_row = [Pipe(PipeType.EMPTY) for i in range(columns-1)] +\
               [Pipe(PipeType.STRAIGHT,0,True)]
    return last_row

def generate_middle_rows(rows,columns): #False to krok w dol, True to w prawo
    sequence = [True for i in range(columns-1)] + [False for i in range(rows-1)]
    random.shuffle(sequence)
    sequence.append(False)
    current_direction = False
    middle_rows = []
    iterator = 0
    for direction in sequence:
        iterator+=1
        if(direction != current_direction):
            middle_rows.append(Pipe(PipeType(1),get_random_angle()))
            current_direction = not current_direction
        else:
            middle_rows.append(Pipe(PipeType.STRAIGHT))
        if direction == False and iterator != len(sequence):
            middle_rows += [get_random_pipe() for i in range(columns-1)]#Pipe(PipeType.EMPTY) for i in range(columns-1)]

    return middle_rows

def get_random_pipe():
    random_number = random.randint(0,1)
    return Pipe(PipeType(random_number),get_random_angle())

# def get_random_direction_change_pipe():
#     random_number = random.randint(1,2) #enumy typu rurki to dla 1 Corner a dla 2 Cross
#     return Pipe(PipeType(random_number),get_random_angle())

def get_random_angle():
   return 90*random.randint(0,3)
