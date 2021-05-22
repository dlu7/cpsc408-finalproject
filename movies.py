import mysql.connector
import pandas as pd
from faker import Faker
import re

# connection to database
db = mysql.connector.connect(
    host="34.94.182.22",
    user="dlu@chapman.edu",
    passwd="barfoo",
    database="dlu_db"
)
mycursor = db.cursor()

# setting options to show full dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# display records of tables in database
def displayData():
    while True:
        print("\n\nWhat information would you like to display?")
        print("-------------------------------------------------")
        print("1. Movie Information")
        print("2. Available Streaming Services")
        print("3. Genres")
        print("4. All User Information")
        print("5. Your Plan to Watch List")
        print("6. Your Watched List")
        print("7. Return to Main Menu")
        print("-------------------------------------------------")
        display = input("Enter the corresponding number: ")

        if display == "1":
            print("\n     Movie Information")
            print("-----------------------------------------------------------------------")
            mycursor.execute("SELECT MovieID, Title, Year, GenreID, ContentRating, Director, RunningTime,"
                             "Actor1, Actor2, Actor3, Actor4, StreamingServiceID FROM Movie WHERE isDeleted = 0;")
            movieRecords = mycursor.fetchall()
            df = pd.DataFrame(movieRecords, columns = ['MovieID', 'Title', 'Year', 'GenreID', 'ContentRating', 'Director',
                                                       'RunningTime', 'Actor1', 'Actor2', 'Actor3', 'Actor4', 'StreamingServiceID'])
            print(df)
            print("-----------------------------------------------------------------------")

        elif display == "2":
            print("\n     Available Streaming Services")
            print("-----------------------------------------------------------------------")
            mycursor.execute("SELECT * FROM StreamingService;")
            ssRecords = mycursor.fetchall()
            df = pd.DataFrame(ssRecords, columns = ['StreamingServiceID', 'Name'])
            print(df)
            print("-----------------------------------------------------------------------")

        elif display == "3":
            print("\n     Genres")
            print("-----------------------------------------------------------------------")
            mycursor.execute("SELECT * FROM Genre;")
            genreRecords = mycursor.fetchall()
            df = pd.DataFrame(genreRecords, columns = ['GenreID', 'Type'])
            print(df)
            print("-----------------------------------------------------------------------")

        elif display == "4":
            print("\n     User Information")
            print("-----------------------------------------------------------------------")
            mycursor.execute("SELECT UserID, FirstName, LastName, Email FROM User WHERE isDeleted = 0;")
            userRecords = mycursor.fetchall()
            df = pd.DataFrame(userRecords, columns = ['UserID', 'FirstName', 'LastName', 'Email'])
            print(df)
            print("-----------------------------------------------------------------------")

        elif display == "5":
            userID = input("Enter your user ID: ")
            print("\n     User Planning to Watch")
            print("-----------------------------------------------------------------------")
            mycursor.callproc('Planned', args = (userID, ))
            for i in mycursor.stored_results():
                plannedRecords = i.fetchall()
            if len(plannedRecords) > 0:
                df = pd.DataFrame(plannedRecords, columns = ['MovieID', 'Title', 'Genre', 'Director', 'Actor1', 'Streaming Platform'])
                print(df)
                print("-----------------------------------------------------------------------")
            else:
                print("You do not have anything in your planned list!")

        elif display == "6":
            userID = input("Enter your user ID: ")
            print("\n     User Already Watched")
            print("-----------------------------------------------------------------------")
            mycursor.callproc('Watched', args=(userID,))
            for i in mycursor.stored_results():
                watchedRecords = i.fetchall()
            if len(watchedRecords) > 0:
                df = pd.DataFrame(watchedRecords, columns = ['MovieID', 'Title', 'Genre', 'Director', 'Actor1', 'Streaming Platform'])
                print(df)
                print("-----------------------------------------------------------------------")
            else:
                print("You do not have anything in your watched list!")

        elif display == "7":
            break

        else:
            print("Invalid option - please choose a number between 1 and 7.")
            continue

# query with various parameters/filters
def searchData():
    while True:
        print("\n\nWhat would you like to search by?")
        print("---------------------------------------")
        print("1. Title")
        print("2. Year")
        print("3. Genre")
        print("4. Content Rating")
        print("5. Director")
        print("6. Actor")
        print("7. Average Rating")
        print("8. Streaming Platform")
        print("9. Top Rated Movie by User")
        print("10. Return to Main Menu")
        print("---------------------------------------")
        search = input("Enter the corresponding number: ")

        # search by Title
        if search == '1':
            user_input = input("\nEnter the movie title: ")
            titleList = (" " or ":" or "-" or "!" or "?" or "&")
            if titleList in user_input or user_input.isalnum():
                mycursor.callproc('SearchTitle', (user_input, ))
                for i in mycursor.stored_results():
                    output = i.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output, columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                                       'Director', 'Actor1', 'Actor2',
                                                       'Avg Rating', 'Streaming Platform'])
                    print(df)
                else:
                    print("No records were found for the movie " + str(user_input) + ".")
            else:
                print("Invalid - please try again.")

        # search by year
        elif search == '2':
            while True:
                user_input = input("\nEnter the year: ")
                if user_input.isdigit():
                    user_input = int(user_input)
                    if user_input >= 1900 and user_input <= 2021:
                            mycursor.callproc('SearchYear', [user_input])
                            for i in mycursor.stored_results():
                                output = i.fetchall()
                            if len(output) > 0:
                                df = pd.DataFrame(output,
                                                columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                                        'Director', 'Actor1', 'Actor2',
                                                        'Avg Rating', 'Streaming Platform'])
                                print(df)
                                break
                            else:
                                print("No records were found for the year " + str(user_input) + ".")
                                break
                    else:
                        print("Invalid year - please enter a year between 1900 and 2021.")
                        continue
                else:
                    print("Invalid - please enter numbers.")
                    continue

        # search by Genre
        elif search == '3':
            print("\nPick a genre from below: \n")
            print("--------------------------------\n"
                  "Action\n"
                  "Adventure\n"
                  "Comedy\n"
                  "Crime\n"
                  "Documentary\n"
                  "Drama\n"
                  "Fantasy\n"
                  "Horror\n"
                  "Musical\n"
                  "Romance\n"
                  "Romantic Comedy\n"
                  "Science Fiction\n"
                  "Thriller\n"
                  "Western")
            print("--------------------------------")
            user_input = input("Enter a genre: ")

            genreList = ("a", "A", "c", "C", "d", "D", "f", "F", "h", "H", "m", "M", "r", "R", "s", "S", "t", "T", "w", "W")
            if user_input.startswith(genreList):
                mycursor.callproc('SearchGenre', [user_input])
                for i in mycursor.stored_results():
                    output = i.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output,
                                      columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                               'Director', 'Actor1', 'Actor2',
                                               'Avg Rating', 'Streaming Platform'])
                    print(df)
                else:
                    print("No records were found for the genre " + str(user_input) + ".")
            else:
                print("Invalid genre - please choose one from the list below.")
                continue

        # search by content rating
        elif search == "4":
            while True:
                print("\nPick a content rating from below: \n"
                      "---------------------------------------\n"
                      "G\n"
                      "PG\n"
                      "PG-13\n"
                      "R\n"
                      "NC-17\n"
                      "---------------------------------------")
                user_input = input("Enter a movie content rating: ")
                crList = ['G', 'PG', 'PG-13', 'R', 'NC-17']

                if (user_input.isalnum() or "-" in user_input) and user_input in crList:
                    mycursor.callproc('SearchContentRating', [user_input])
                    for i in mycursor.stored_results():
                        output = i.fetchall()
                    if len(output) > 0:
                        df = pd.DataFrame(output,
                                          columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                                   'Director', 'Actor1', 'Actor2',
                                                   'Avg Rating', 'Streaming Platform'])
                        print(df)
                        break
                    else:
                        print("No records were found for the content rating " + str(user_input) + ".")
                        break
                else:
                    print("Invalid - please enter one of the below content ratings.")
                    continue

        # search by director
        elif search == "5":
            user_input = input("\nEnter the name of a director: ")
            if " " in user_input or user_input.isalpha():
                if user_input.isdigit():
                    print("Invalid - please enter A-Z characters.")
                else:
                    mycursor.callproc('SearchDirector', [user_input])
                    for i in mycursor.stored_results():
                        output = i.fetchall()
                    if len(output) > 0:
                        df = pd.DataFrame(output,
                                          columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                                   'Director', 'Actor1', 'Actor2',
                                                   'Avg Rating', 'Streaming Platform'])
                        print(df)
                    else:
                        print("No records were found for the director " + str(user_input) + ".")
            else:
                print("Invalid - please try again.")
                continue

        # search by actor
        elif search == "6":
            while True:
                user_input = input("\nEnter the name of an actor: ")
                if " " in user_input or user_input.isalpha():
                    if user_input.isdigit():
                        print("Invalid - please enter A-Z characters.")
                        continue
                    else:
                        mycursor.callproc('SearchActor', [user_input])
                        for i in mycursor.stored_results():
                            output = i.fetchall()
                        if len(output) > 0:
                            df = pd.DataFrame(output,
                                              columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                                       'Director', 'Actor1', 'Actor2',
                                                       'Avg Rating', 'Streaming Platform'])
                            print(df)
                            break
                        else:
                            print("No records were found for the actor " + str(user_input) + ".")
                            break
                else:
                    print("Invalid - please try again.")
                    continue

        # search by average rating
        elif search == "7":
            while True:
                user_input = input("\nEnter an average rating between 0 and 10: ")
                if "." in user_input or user_input.isdecimal():
                    user_input = float(user_input)
                    if user_input <= -1 or user_input >= 11:
                        print("Invalid: please enter a number between 0-10.")
                    else:
                        mycursor.callproc('SearchAverageRating', (user_input,))
                        for i in mycursor.stored_results():
                            output = i.fetchall()
                        if len(output) > 0:
                            df = pd.DataFrame(output,
                                              columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                                       'Director', 'Actor1', 'Actor2',
                                                       'Avg Rating', 'Streaming Platform'])
                            print(df)
                            break
                        else:
                            print("No records were found for the average rating " + str(user_input) + ".")
                            break
                else:
                    print("Invalid - please enter a number.")
                    continue


        # search by streaming platform
        elif search == "8":
            print("\nPick a streaming service platform from below: \n"
                  "--------------------------------------------------\n"
                  "Hulu\n"
                  "Netflix\n"
                  "Disney+\n"
                  "Paramount+\n"
                  "Prime Video\n"
                  "Apple TV+\n"
                  "HBO Max\n"
                  "Peacock\n"
                  "Crunchyroll\n"
                  "--------------------------------------------------")
            user_input = input("Enter a streaming service platform: ")
            genreList = ("a", "A", "c", "C", "d", "D", "h", "H", "n", "N", "p", "P")
            if user_input.startswith(genreList):
                mycursor.callproc('SearchStreamingService', [user_input])
                for i in mycursor.stored_results():
                    output = i.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output,
                                      columns=['MovieID', 'Title', 'Year', 'Genre', 'Content Rating',
                                               'Director', 'Actor1', 'Actor2',
                                               'Avg Rating', 'Streaming Platform'])
                    print(df)
                else:
                    print("No records were found for the streaming service platform " + str(user_input) + ".")
            else:
                print("Invalid streaming platform - please choose one from the list below.")
                continue

        elif search == "9":
            user_input = input("Enter your user ID: ")
            mycursor.callproc('AllTimeMovie', args = (user_input, ))
            for i in mycursor.stored_results():
                output = i.fetchall()
            if len(output) > 0:
                df = pd.DataFrame(output, columns=['Title', 'Rating'])
                print(df)
            else:
                print("No records were found for user ID #" + str(user_input) + ".")

        elif search == "10":
            break

        else:
            print("\nInvalid option - please choose one from the list below.")
            continue


# creating new records
def createRecord():
    while True:
        print("\n\nWhere would you like to create a new record?")
        print("--------------------------------------------------")
        print("1. Movie Information Table")
        print("2. User Information Table")
        print("3. User Plan to Watch")
        print("4. User Watched")
        print("5. Return to Main Menu")
        print("--------------------------------------------------")
        create = input("Enter a corresponding number: ")

        # adding to movie table
        if create == "1":
            while True:
                title = input("\nEnter the movie title: ")
                titleList = (" " or ":" or "-" or "!" or "?" or "&")
                if titleList in title or title.isalnum():
                    break
                else:
                    print("Invalid - please enter alphanumeric characters.")
                    continue

            # Year
            while True:
                year = input("Enter the year the movie was made: ")
                if year.isdigit():
                    year = int(year)
                    if year >= 1900 and year <= 2021:
                        break
                    else:
                        print("Invalid - please enter a valid year between 1900 and 2021.")
                        continue
                else:
                    print("Invalid - please enter a valid year.")
                    continue

            # Genre
            print("Pick a genre from below: \n"
                  "------------------------------\n"
                  "1. Action\n"
                  "2. Adventure\n"
                  "3. Comedy\n"
                  "4. Crime\n"
                  "5. Documentary\n"
                  "6. Drama\n"
                  "7. Fantasy\n"
                  "8. Horror\n"
                  "9. Musical\n"
                  "10. Romance\n"
                  "11. Romantic Comedy\n"
                  "12. Science Fiction\n"
                  "13. Thriller\n"
                  "14. Western\n"
                  "------------------------------")
            while True:
                genre = int(input("Enter the corresponding number: "))
                try:
                    if genre <= 0 and genre >= 15:
                        print("Invalid - choose a numbered genre between 1 and 14.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Invalid input - please enter a number from the list.")
                    continue

            # Content Rating
            while True:
                print("Pick a content rating from below: \n"
                      "---------------------------------------\n"
                      "G\n"
                      "PG\n"
                      "PG-13\n"
                      "R\n"
                      "NC-17\n"
                      "---------------------------------------")
                crating = input("Enter the movie content rating: ")
                crList = ['G', 'PG', 'PG-13', 'R', 'NC-17']

                if (crating.isalnum() or "-" in crating) and crating in crList:
                    break
                else:
                    print("Invalid - please enter one of the below content ratings.")
                    continue

            # Director
            while True:
                director = input("Enter the full name of the director: ")
                if " " in director:
                    if director.isdigit():
                        print("Invalid - please enter A-Z characters.")
                        continue
                    else:
                        break
                else:
                    print("Invalid - please enter a full name.")
                    continue

            # Running Time
            while True:
                runningtime = input("Enter the movie running time (ex. 01:05:10 in Hours:Minutes:Seconds): ")
                format = "^((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$)"
                isTime = re.match(format, runningtime)

                if isTime:
                    break
                else:
                    print("Invalid - please enter in the format specified.")
                    continue

            # Actor 1
            while True:
                actor1 = input("Enter the first actor's full name: ")
                if " " in actor1:
                    if actor1.isdigit():
                        print("Invalid - please enter A-Z characters.")
                        continue
                    else:
                        break
                else:
                    print("Invalid - please enter a full name.")
                    continue

            # Actor 2
            while True:
                actor2 = input("Enter the second actor's full name: ")
                if " " in actor2:
                    if actor2.isdigit():
                        print("Invalid - please enter A-Z characters.")
                        continue
                    else:
                        break
                else:
                    print("Invalid - please enter a full name.")
                    continue

            # Actor 3
            while True:
                actor3 = input("Enter the third actor's full name: ")
                if " " in actor3:
                    if actor3.isdigit():
                        print("Invalid - please enter A-Z characters.")
                        continue
                    else:
                        break
                else:
                    print("Invalid - please enter a full name.")
                    continue

            # Actor 4
            while True:
                actor4 = input("Enter the fourth actor's full name: ")
                if " " in actor4:
                    if actor4.isdigit():
                        print("Invalid - please enter A-Z characters.")
                        continue
                    else:
                        break
                else:
                    print("Invalid - please enter a full name.")
                    continue

            # Streaming Platform if applicable
            print("Pick a streaming service platform from below: \n"
                  "-----------------------------------------------\n"
                  "1. Hulu\n"
                  "2. Netflix\n"
                  "3. Disney+\n"
                  "4. Paramount+\n"
                  "5. Prime Video\n"
                  "6. Apple TV+\n"
                  "7. HBO Max\n"
                  "8. Peacock\n"
                  "9. Crunchyroll\n"
                  "-----------------------------------------------")

            while True:
                ssplatform = input("Enter the corresponding number for a streaming platform if applicable.\n"
                                   "If not available on a streaming platform yet, enter 10: ")

                if int(ssplatform) <= 0 and int(ssplatform) >= 11:
                    print("Invalid - please try again.")
                    continue
                else:
                    break

            try:
                # adding to database
                mycursor.callproc('AddMovie', args = (title, year, genre, crating, director, runningtime, actor1, actor2, actor3, actor4, ssplatform))
                for i in mycursor.stored_results():
                    movie = i.fetchall()
                    print(movie)
                print("\nMovie added successfully!")
                db.commit()
                break
            except mysql.connector.Error:
                print("Failed to add movie -- rolling back.")
                db.rollback()
                continue

        # adding to user info table
        elif create == "2":
            # first name
            while True:
                firstname = input("\nEnter first name: ")
                if firstname.isalpha():
                    break
                else:
                    print("Invalid - please enter A-Z characters only.")
                    continue

            # last name
            while True:
                lastname = input("Enter last name: ")
                if lastname.isalpha():
                    break
                else:
                    print("Invalid - please enter A-Z characters only.")
                    continue

            # email
            while True:
                email = input("Enter an email: ")
                if "@" in email:
                    break
                else:
                    print("Invalid - please enter a valid email.")
                    continue

            try:
                # adding to database
                mycursor.callproc('AddUser', args=(firstname, lastname, email))
                for i in mycursor.stored_results():
                    movie = i.fetchall()
                    print(movie)
                db.commit()
                print("\nUser added successfully!")
            except mysql.connector.Error:
                print("Failed to add user -- rolling back.")
                db.rollback()
                continue

        # adding to user plan to watch
        elif create == "3":
            while True:
                userID = input("\nEnter your user ID: ")
                if userID.isdigit():
                    break
                else:
                    print("Invalid - please enter a valid number.")
                    continue

            while True:
                movieID = input("Enter the movie ID: ")
                if movieID.isdigit():
                    break
                else:
                    print("Invalid - please enter a valid number.")
                    continue

            try:
                # adding to database
                mycursor.callproc('AddUserPlanned', args=(userID, movieID))
                for i in mycursor.stored_results():
                    userplanned = i.fetchall()
                    print(userplanned)
                db.commit()
                print("\nMovie added to planned list successfully!")
            except mysql.connector.Error:
                print("Failed to add -- rolling back.")
                db.rollback()
                continue

        elif create == "4":
            while True:
                userID = input("\nEnter your user ID: ")
                if userID.isdigit():
                    break
                else:
                    print("Invalid - please enter a valid number.")
                    continue

            while True:
                movieID = input("Enter the movie ID: ")
                if movieID.isdigit():
                    break
                else:
                    print("Invalid - please enter a valid number.")
                    continue

            while True:
                rating = input("Enter your personal rating (on a scale of 1 to 10): ")
                if rating.isdigit():
                    break
                else:
                    print("Invalid - please enter a number.")
                    continue

            try:
            # adding to database
                mycursor.callproc('AddUserWatched', args=(userID, movieID, rating))
                for i in mycursor.stored_results():
                    userplanned = i.fetchall()
                    print(userplanned)
                db.commit()
                print("\nMovie added to watched list successfully!")
            except mysql.connector.Error:
                print("Failed to add -- rolling back.")
                db.rollback()
                continue

        elif create == "5":
            break

        else:
            print("Invalid option - please enter a number between 1 and 4.")
            continue


# deleting records (soft delete)
def deleteRecord():
    while True:
        user_delete = input("\n\nWhere would you like to delete? \n"
                            "------------------------------------\n"
                            "1. Movie Information\n"
                            "2. User Information\n"
                            "3. User Plan to Watch List\n"
                            "4. User Watched List\n"
                            "5. Return to Main Menu\n"
                            "------------------------------------\n"
                            "Enter a corresponding number: ")

        if user_delete == "1":
            user_input = input("Enter the ID number of the movie you'd like to delete: ")

            try:
                mycursor.callproc('DeleteMovie', args = (user_input, ))
                for i in mycursor.stored_results():
                    i.fetchall()
                db.commit()
                print("The movie corresponding to ID #" + user_input + " has been deleted.")
            except mysql.connector.Error:
                print("Failed to delete - rolling back.")
                db.rollback()
                continue


        elif user_delete == "2":
            user_input = input("Enter the ID number of the user you'd like to delete: ")

            try:
                mycursor.execute("UPDATE User SET isDeleted = 1 WHERE UserID = %s;", (user_input, ))
                mycursor.fetchall()
                db.commit()
                print("The user corresponding to ID #" + user_input + " has been deleted.")
            except mysql.connector.Error:
                print("Failed to delete - rolling back.")
                db.rollback()
                continue

        elif user_delete == "3":
            user_input = input("Enter the ID number of the user you'd like to delete: ")
            movie_input = input("Enter the ID number of the movie you'd like to delete: ")

            try:
                mycursor.execute("UPDATE UserPlanned SET isDeleted = 1 WHERE UserID = %s AND MovieID = %s;", (user_input, movie_input, ))
                mycursor.fetchall()
                db.commit()
                print("The planned movie corresponding to ID #" + movie_input + " has been deleted for user #" + user_input + ".")
            except mysql.connector.Error:
                print("Failed to delete - rolling back.")
                db.rollback()
                continue

        elif user_delete == "4":
            user_input = input("Enter the ID number of the user you'd like to delete: ")
            movie_input = input("Enter the ID number of the movie you'd like to delete: ")

            try:
                mycursor.execute("UPDATE UserWatched SET isDeleted = 1 WHERE UserID = %s AND MovieID = %s;", (user_input, movie_input, ))
                mycursor.fetchall()
                db.commit()
                print("The watched movie corresponding to ID #" + movie_input + " has been deleted for user #" + user_input + ".")
            except mysql.connector.Error:
                print("Failed to delete - rolling back.")
                db.rollback()
                continue

        elif user_delete == "5":
            break

        else:
            print("Invalid option - please choose a number between 1 and 5.")
            continue


# updating records
def updateRecord():
    status = True
    while (status == True):
        print("\n\nWhat would you like to update?\n"
              "-----------------------------------\n"
              "1. Movie Information\n"
              "2. User Information\n"
              "3. User Planned List\n"
              "4. User Watched List\n"
              "5. Return to Main Menu\n"
              "-----------------------------------")
        update = input("Enter the corresponding number: ")

        if update == "1":
            user_input = input("Enter the corresponding movie ID that you'd like to update: ")

            if user_input.isdigit():
                print("\nWhat would you like to update for the movie ID# " + user_input + "?\n"
                      "------------------------------------------------------------------\n"
                      "1. Title\n"
                      "2. Year\n"
                      "3. Genre\n"
                      "4. Content Rating\n"
                      "5. Director\n"
                      "6. Running Time\n"
                      "7. Actor 1\n"
                      "8. Actor 2 \n"
                      "9. Actor 3 \n"
                      "10. Actor 4\n"
                      "11. Streaming Service\n"
                      "------------------------------------------------------------------")
                movie_input = input("Enter the corresponding number: ")

                try:
                    if movie_input == "1":
                        title = input("Enter the new title: ")
                        mycursor.execute("UPDATE Movie SET Title = %s WHERE MovieID = %s AND isDeleted = 0;", (title, user_input, ))
                        db.commit()
                        status = False
                    elif movie_input == "2":
                        year = input("Enter the new year: ")
                        mycursor.execute("UPDATE Movie SET Year = %s WHERE MovieID = %s AND isDeleted = 0;", (year, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "3":
                        print("\nPick a genre from below: \n"
                              "------------------------------\n"
                              "1. Action\n"
                              "2. Adventure\n"
                              "3. Comedy\n"
                              "4. Crime\n"
                              "5. Documentary\n"
                              "6. Drama\n"
                              "7. Fantasy\n"
                              "8. Horror\n"
                              "9. Musical\n"
                              "10. Romance\n"
                              "11. Romantic Comedy\n"
                              "12. Science Fiction\n"
                              "13. Thriller\n"
                              "14. Western\n"
                              "------------------------------")
                        genre = input("Enter the corresponding number for the new genre: ")
                        mycursor.execute("UPDATE Movie SET GenreID = %s WHERE MovieID = %s AND isDeleted = 0;", (genre, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "4":
                        print("\nPick a content rating from below: \n"
                              "G\n"
                              "PG\n"
                              "PG-13\n"
                              "R\n"
                              "NC-17")
                        crating = input("Enter the new movie content rating: ")
                        mycursor.execute("UPDATE Movie SET ContentRating = %s WHERE MovieID = %s AND isDeleted = 0;", (crating, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "5":
                        director = input("Enter the full name of the new director: ")
                        mycursor.execute("UPDATE Movie SET Director = %s WHERE MovieID = %s AND isDeleted = 0;", (director, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "6":
                        runningtime = input("Enter the new running time of the movie: ")
                        mycursor.execute("UPDATE Movie SET RunningTime = %s WHERE MovieID = %s AND isDeleted = 0;", (runningtime, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "7":
                        actor1 = input("Enter the new name of the first actor: ")
                        mycursor.execute("UPDATE Movie SET Actor1 = %s WHERE MovieID = %s AND isDeleted = 0;", (actor1, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "8":
                        actor2 = input("Enter the new name of the second actor: ")
                        mycursor.execute("UPDATE Movie SET Actor2 = %s WHERE MovieID = %s AND isDeleted = 0;", (actor2, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "9":
                        actor3 = input("Enter the new name of the third actor: ")
                        mycursor.execute("UPDATE Movie SET Actor3 = %s WHERE MovieID = %s AND isDeleted = 0;", (actor3, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "10":
                        actor4 = input("Enter the new name of the first actor: ")
                        mycursor.execute("UPDATE Movie SET Actor4 = %s WHERE MovieID = %s AND isDeleted = 0;", (actor4, user_input,))
                        db.commit()
                        status = False
                    elif movie_input == "11":
                        print("\nPick a streaming service platform from below: \n"
                              "------------------------------------------------\n"
                              "1. Hulu\n"
                              "2. Netflix\n"
                              "3. Disney+\n"
                              "4. Paramount+\n"
                              "5. Prime Video\n"
                              "6. Apple TV+\n"
                              "7. HBO Max\n"
                              "8. Peacock\n"
                              "9. Crunchyroll\n"
                              "------------------------------------------------")
                        ssplatform = input("Enter the corresponding number for the new streaming platform\n"
                                           "or enter 10 for none:  ")
                        mycursor.execute("UPDATE Movie SET StreamingServiceID = %s WHERE MovieID = %s AND isDeleted = 0);", (ssplatform, user_input,))
                        db.commit()
                        status = False
                    else:
                        print("Invalid option - please enter a number between 1 and 11.")
                        continue
                except mysql.connector.Error:
                    print("Failed to update -- rolling back.")
                    db.rollback()
                    continue
            else:
                print("Invalid - please enter a whole number.")
                continue

        elif update == "2":
            user_input = input("Enter the corresponding user ID that you'd like to update: ")

            if user_input.isdigit():
                print("\nWhat would you like to update for the user ID# " + user_input + "?\n"
                      "------------------------------------------------------------------\n"
                      "1. First Name\n"
                      "2. Last Name\n"
                      "3. Email\n"
                      "------------------------------------------------------------------")
                u_input = input("Enter the corresponding number: ")

                try:
                    if u_input == "1":
                        fname = input("Enter the new first name: ")
                        mycursor.execute("UPDATE User SET FirstName = %s WHERE UserID = %s AND isDeleted = 0;",
                                         (fname, user_input, ))
                        db.commit()
                        status = False
                    elif u_input == "2":
                        lname = input("Enter the new last name: ")
                        mycursor.execute("UPDATE User SET LastName = %s WHERE UserID = %s AND isDeleted = 0;",
                                         (lname, user_input, ))
                        db.commit()
                        status = False
                    elif u_input == "3":
                        email = input("Enter the new email: ")
                        mycursor.execute("UPDATE User SET Email = %s WHERE UserID = %s AND isDeleted = 0;",
                                         (title, user_input,))
                        db.commit()
                        status = False
                    else:
                        print("Invalid option - please choose between 1 and 3.")
                        continue
                except mysql.connector.Error:
                    print("Failed to update -- rolling back.")
                    db.rollback()
                    continue
            else:
                print("Invalid - please enter a whole number.")
                continue

        elif update == "3":
            user_input = input("Enter the corresponding user ID that you'd like to update: ")

            if user_input.isdigit():
                try:
                    movie_input = input("Enter the movie ID that you plan not to watch: ")
                    mycursor.execute("UPDATE UserPlanned SET Planned = 0 WHERE UserID = %s AND MovieID = %s AND isDeleted = 0;",
                                         (user_input, movie_input, ))
                    db.commit()
                    status = False

                except mysql.connector.Error:
                    print("Failed to update -- rolling back.")
                    db.rollback()
                    continue
            else:
                print("Invalid - please enter a whole number.")
                continue


        elif update == "4":
            user_input = input("Enter the corresponding user ID that you'd like to update: ")

            if user_input.isdigit():
                print("\nWhat would you like to update for the user ID# " + user_input + "?\n"
                        "------------------------------------------------------------------\n"
                        "1. Movie rating for a specific movie\n"
                        "------------------------------------------------------------------")
                u_input = input("Enter the corresponding number: ")

                try:
                    if u_input == "1":
                        movie_input = input("Enter the movie ID that you watched: ")
                        rating = input("Enter the new rating: ")
                        mycursor.execute("UPDATE UserWatched SET UserRating = %s WHERE UserID = %s AND MovieID = %s AND isDeleted = 0;",
                                         (rating, user_input, movie_input, ))
                        db.commit()
                        status = False
                    else:
                        print("Invalid option - please enter 1.")
                except mysql.connector.Error:
                    print("Failed to update -- rolling back.")
                    db.rollback()
                    continue
            else:
                print("Invalid - please enter a whole number.")
                continue

        elif update == "5":
            break

        else:
            print("Invalid option - please enter a number between 1 and 4.")
            continue

    print("Update successful!")

# generate reports that can be exported (excel or csv format)
def generateRecords():
    while True:
        user_input = input("\n\nPick an option from below to generate a file: \n"
                           "-----------------------------------------------------\n"
                           "1. Movie Information\n"
                           "2. User Information\n"
                           "3. User Plan to Watch List\n"
                           "4. User Watched List\n"
                           "-----------------------------------------------------\n"
                           "Enter a corresponding number: ")

        file = input("Enter a name for the file and the format [ex. 'movies.csv', 'users.xlsx']: ")
        fileformat = (".csv", "xlsx")

        while not file.endswith(fileformat):
            file = input("Enter a name for the file with '.csv' or '.xlsx': ")

        if user_input == "1":
            mycursor.execute("SELECT * FROM Movie WHERE Movie.isDeleted = 0;")
            output = mycursor.fetchall()

            if len(output) > 0:
                columns_names = [c[0] for c in mycursor.description]
                df = pd.DataFrame(output, columns = columns_names)

                if ".csv" in file:
                    df.to_csv(file)
                    break
                else:
                    df.to_excel(file)
                    break
            else:
                print("No records to print.")
                continue

        elif user_input == "2":
            mycursor.execute("SELECT * FROM User WHERE isDeleted = 0;")
            output = mycursor.fetchall()

            if len(output) > 0:
                columns_names = [c[0] for c in mycursor.description]
                df = pd.DataFrame(output, columns = columns_names)

                if ".csv" in file:
                    df.to_csv(file)
                    break
                else:
                    df.to_excel(file)
                    break
            else:
                print("No records to print.")
                continue

        elif user_input == "3":
            mycursor.execute("SELECT DISTINCT UserID, FirstName, LastName FROM Users ORDER BY UserID;")
            userRecords = mycursor.fetchall()
            columns_names = [c[0] for c in mycursor.description]
            df = pd.DataFrame(userRecords, columns = columns_names)
            print(df)
            user = input("Enter your user ID: ")

            mycursor.execute("SELECT DISTINCT Title, Year, Type FROM Users WHERE UserID = %s AND Planned = 1;", (user, ))
            output = mycursor.fetchall()

            if len(output) > 0:
                columns_names2 = [c[0] for c in mycursor.description]
                df = pd.DataFrame(output, columns = columns_names2)

                if ".csv" in file:
                    df.to_csv(file)
                    break
                else:
                    df.to_excel(file)
                    break
            else:
                print("No records to print.")
                continue

        elif user_input == "4":
            mycursor.execute("SELECT DISTINCT UserID, FirstName, LastName FROM Users ORDER BY UserID;")
            userRecords = mycursor.fetchall()
            columns_names = [c[0] for c in mycursor.description]
            df = pd.DataFrame(userRecords, columns = columns_names)
            print(df)
            user = input("Enter your user ID: ")

            mycursor.execute("SELECT DISTINCT Title, Year, Type FROM Users WHERE UserID = %s AND Watched = 1;", (user,))
            output = mycursor.fetchall()

            if len(output) > 0:
                columns_names2 = [c[0] for c in mycursor.description]
                df = pd.DataFrame(output, columns = columns_names2)

                if ".csv" in file:
                    df.to_csv(file)
                    break
                else:
                    df.to_excel(file)
                    break
            else:
                print("No records to print.")
                continue

        else:
            print("Invalid option - please choose a number between 1 and 4.")
            continue

    print("\nFile generated successfully!")


# menu
def main():
    print("\n\n\n             Movie Database                ")
    print("----------------------------------------")
    print("1. Display records")
    print("2. Search and display records")
    print("3. Create a record")
    print("4. Update a record")
    print("5. Delete a record")
    print("6. Generate records into a csv file")
    print("7. Exit program")
    print("----------------------------------------")
    return input("Choose a corresponding number: ")


# user is able to execute commands and reprompt menu until they exit
user_input = ""
while user_input != "7":
    user_input = main()

    if user_input == '1':
        displayData()
    elif user_input == '2':
        searchData()
    elif user_input == '3':
        createRecord()
    elif user_input == '4':
        updateRecord()
    elif user_input == '5':
        deleteRecord()
    elif user_input == '6':
        generateRecords()
    elif user_input == '7':
        print("\n             Goodbye!")
        quit()
    else:
        print("\nInvalid option: please try again.")


db.close()