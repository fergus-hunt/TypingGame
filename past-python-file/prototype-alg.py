import pandas, json
df = pandas.read_csv("positions.csv")
print(df.loc[3].x)

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
        
    else: 
        neighbours = [seat_number + 1, seat_number -1, seat_number + 7, seat_number - 7]
    dict[f"{seat_number}"] = [neighbour for neighbour in neighbours]
    




print(dict)