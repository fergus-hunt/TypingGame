import pandas, json
import pandas, json, numpy
df = pandas.read_csv("positions.csv")

dict = {}
for row in df.iterrows(): 
    seat_number = row[0]
    if seat_number % 7 == 0 or seat_number == 0: 
        if seat_number == 21: 
            neighbours = [22, 14]
        elif  seat_number == 0: 
            neighbours = [1, 7]
        else: 
            neighbours = [seat_number + 1, seat_number - 7, seat_number + 7]

    elif seat_number % 7 == 6: 
        if seat_number == 6: 
            neighbours = [seat_number - 1, seat_number + 7]
        elif seat_number == 27:
            neighbours = [seat_number -1, seat_number-7]
        else: 
            neighbours = [seat_number - 1, seat_number + 7, seat_number - 7]
        
    elif seat_number >20: 
        neighbours = [seat_number + 1, seat_number -1 , seat_number - 7]
    else: 
        neighbours = [seat_number + 1, seat_number -1, seat_number + 7, seat_number - 7]

    connections = {}
    for person in neighbours:
         
        tuuple = df.iloc[person]
        print(tuuple)
        x = tuuple.x 
        y = tuuple.y
        print(x, y)
        hypot = (x*x + y*y)
        distance = (numpy.sqrt(hypot))
        connections[f"{tuuple.seat}"] = hypot

    dict[f"{seat_number}"] = connections

print(dict)