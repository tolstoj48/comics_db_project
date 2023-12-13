import pandas as pd
import sqlite3

def fetch_df_from_db(cursor, sql):
    """Gets cursor and SQL code and runs the SQL code on the cursor. Returns ready dataframe from the db data."""
    try:
        result = cursor.execute(sql)
        rows = result.fetchall()
        columns = [column[0] for column in cursor.description]
    except:
        print("Error - have not fetched all the data from sqlite3 db - in the fetch_df_from_db()")
    else:
        return pd.DataFrame(rows, columns=columns)

def get_all_data(type_of_search):
    """Gets all the data from sqlite3 db based on user input."""
    try:
        conn = sqlite3.connect("./db/comics.db")
        cur = conn.cursor()
        if type_of_search in ["t"]:
            data_from_db = fetch_df_from_db(cur, "SELECT * FROM titles;")
        else:
            data_from_db = fetch_df_from_db(cur, "SELECT * FROM publishers;")
    except:
        print("Error - have not fetched all the data from sqlite3 db - in the get_all_data()")
    else:
        return data_from_db
    finally:
        conn.close()

def fetch_searching_opt_type(what):
        """Gets the input info from an user and returns values to decide what type of info user wants."""
        if what == "t":
            user_input_type = input(f"Would you like to do fulltext search of titles [FT] or would you like to find titles in a choosen year [Y]?  ")
            print("--------------------------------------------------------------------------")
            user_input_type = user_input_type.strip().lower()
        elif what == "p":
            user_input_type = input(f"Would you like to get summary of a publisher [S] or fetch all the titles [A]?   ")
            print("--------------------------------------------------------------------------")
            user_input_type = user_input_type.strip().lower()
        else:
            user_input_type = None
        return  user_input_type

def fetch_searching_opt_what():
        """Gets the input info from an user and returns values to decide what to do next."""
        user_input_what = input(f"Would you like to search for titles [T] / publishers [P] / to quit [Q]?  ")
        print("--------------------------------------------------------------------------")
        user_input_what = user_input_what.strip().lower()
        if user_input_what in ["q", "quit", "quits"]:
            user_input_what = "q"
        elif user_input_what in ["t", "titles", "title", "tit"]:
            user_input_what = "t"
        elif user_input_what in ["p", "pub", "publishers", "publisher"]:
            user_input_what = "p"
        else:
            user_input_what = None
        return  user_input_what

def main():
    """Driver of the whole tool. Must be called to start search db. No parameters needed."""
    while True:
        what_to_search = fetch_searching_opt_what()
        type_of_search = fetch_searching_opt_type(what_to_search)
        if what_to_search  == "q":
            break
        if what_to_search not in ["t", "p"]:
            print("--------------------------------------------------------------------------")
            print("Please, give me [T] for titles, [P] for publishers, [Q] for quit. Other choices are incorrect.")
        if what_to_search == "t" and type_of_search not in ["ft", "y"]:
            type_of_search = fetch_searching_opt_type(what_to_search)
            if type_of_search not in ["ft", "y"]:
                print("Please, start over and provide correct input [FT] or [Y] for titles search.")
                print("--------------------------------------------------------------------------")
        elif what_to_search == "p" and type_of_search not in ["s", "a"]:
            type_of_search = fetch_searching_opt_type(what_to_search)
            if type_of_search not in ["s", "a"]:
                print("Please, start over and provide correct input [S] or [A] for publishers search.")
                print("--------------------------------------------------------------------------")
        else:
            data = get_all_data(what_to_search)
        if what_to_search == "t" and type_of_search == "ft":
            ft_input = input(f"What word/phrase should a title contain?   ")
            ft_input = ft_input.strip().lower()
            data = data[data["title"].str.contains(ft_input, case=False, na=False)]
        elif what_to_search == "t" and type_of_search == "y":
            ft_input = input(f"What year do you want to search for?   ")
            ft_input = int(ft_input.strip().lower())
            data = data[data["year"] == ft_input]
        if what_to_search == "p" and type_of_search == "s":
            pass
        elif what_to_search == "p" and type_of_search == "a":
            pass
        if data.empty:
            print("--------------------------------------------------------------------------")
            print(f"There are no results for the given search of: {ft_input}! Please try again.")
            print("--------------------------------------------------------------------------")
        else:
            print(data)

if __name__ == "__main__":
    main()