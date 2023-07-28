
            insert_query = f"INSERT INTO Dim_Customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)"  
            print(dataTable[row][27])
            self.db.execute(insert_query, dataTable[row][0],dataTable[row][1],dataTable[row][2],dataTable[row][3],dataTable[row][4],dataTable[row][5],dataTable[row][6],dataTable[row][27])
            insert_query = f"INSERT INTO Dim_Date VALUES (?, ?, ?, ?)"  
            date_object = datetime.strptime(dataTable[row][7], '%m/%d/%Y')  # Adjust the format if needed
            

            # Getting the day, month, and year from the datetime object
            day = date_object.day
            month = date_object.month
            year = date_object.year
            self.db.execute(insert_query, dateId ,year, month,day)

            insert_query = f"INSERT INTO FACT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"  
            self.db.execute(insert_query, dataTable[row][0], dateId, dataTable[row][15],dataTable[row][16], dataTable[row][17],dataTable[row][18],dataTable[row][19],dataTable[row][9],dataTable[row][10],dataTable[row][11],dataTable[row][12],dataTable[row][13],dataTable[row][14],dataTable[row][20],dataTable[row][21],dataTable[row][22],dataTable[row][23],dataTable[row][24],dataTable[row][25],dataTable[row][26],dataTable[row][8])
            dateId +=1