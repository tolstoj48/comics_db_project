import datetime
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
        print(
            "Error - have not fetched all the data from sqlite3 db - in the get_all_data()")
    else:
        return data_from_db
    finally:
        conn.close()


def fetch_searching_opt_type(what):
    """Gets the input info from an user and returns values to decide what type of info user wants."""
    if what == "t":
        user_input_type = input(
            f"Would you like to do fulltext search of titles [FT] or would you like to find titles published in a year [Y]?  ")
        print("--------------------------------------------------------------------------")
        user_input_type = user_input_type.strip().lower()
    elif what == "p":
        user_input_type = input(
            f"Would you like to get a summary and measures of central tendency of a publisher [S] or fetch all the titles of particular publisher[A]?   ")
        print("--------------------------------------------------------------------------")
        user_input_type = user_input_type.strip().lower()
    else:
        user_input_type = None
    return user_input_type


def fetch_searching_opt_what():
    """Gets the input info from an user and returns values to decide what to do next."""
    print("--------------------------------------------------------------------------")
    user_input_what = input(
        f"Would you like to search for titles [T] / publishers [P] / or quit [Q]?  ")
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
    return user_input_what


def main():
    """Driver of the whole tool. Must be called to start search db. No parameters needed."""
    while True:
        what_to_search = fetch_searching_opt_what()
        type_of_search = fetch_searching_opt_type(what_to_search)
        if what_to_search == "q":
            break
        if what_to_search not in ["t", "p"]:
            print(
                "--------------------------------------------------------------------------")
            print(
                "Please, give me [T] for titles, [P] for publishers, [Q] for quit. Other choices are incorrect.")
            continue
        if what_to_search == "t" and type_of_search not in ["ft", "y"]:
            type_of_search = fetch_searching_opt_type(what_to_search)
            if type_of_search not in ["ft", "y"]:
                print(
                    "Please, start over and provide correct input [FT] or [Y] for titles search.")
                print(
                    "--------------------------------------------------------------------------")
                continue
        elif what_to_search == "p" and type_of_search not in ["s", "a"]:
            type_of_search = fetch_searching_opt_type(what_to_search)
            if type_of_search not in ["s", "a"]:
                print(
                    "Please, start over and provide correct input [S] or [A] for publishers search.")
                print(
                    "--------------------------------------------------------------------------")
                continue
        else:
            data = get_all_data(what_to_search)
        if what_to_search == "t" and type_of_search == "ft":
            ft_input = input(f"What word/phrase should a title contain?   ")
            ft_input = ft_input.strip().lower()
            data = data[data["title"].str.contains(
                ft_input, case=False, na=False)]
        elif what_to_search == "t" and type_of_search == "y":
            ft_input = input(f"What year do you want to search for?   ")
            try:
                ft_input = int(ft_input.strip().lower())
                data = data[data["year"] == ft_input]
            except:
                continue
        elif what_to_search == "p" and type_of_search == "s":
            s_input = input(
                f"What publisher should I search for (the search is case insensitive)?   ")
            s_input = s_input.strip().lower()
            data_titles = get_all_data("t")
            data_publishers = data[data["name"].str.contains(
                s_input, case=False, na=False)]
            data_all = data_titles.merge(
                data_publishers, how="inner", on="publisher_id")
            data_count = data_all.groupby(
                "name")["title_id"].count().reset_index()
            publishers_count = data_count.values.tolist()
            data_price = data_all.groupby("name")["price"].mean().reset_index()
            publishers_mean_price = data_price.values.tolist()
            data_price = data_all.groupby(
                "name")["price"].median().reset_index()
            publishers_median_price = data_price.values.tolist()
            date = datetime.date.today()
            year = date.strftime("%Y")
            data_all["year_diff"] = int(year) - data_all["year"]
            avg_year_diff = data_all.groupby(
                "name")["year_diff"].mean().reset_index()
            publishers_mean_age = avg_year_diff.values.tolist()
            median_year_diff = data_all.groupby(
                "name")["year_diff"].median().reset_index()
            publishers_median_age = median_year_diff.values.tolist()
            [
                print("-------------------------- \n"
                f"{publisher[0].upper()}: \n"
                f"/ Number of titles: {publisher[1]} "
                f"/ Mean price of titles: {round(publishers_mean_price[index][1], 2)} "
                f"/ Median price of titles: {round(publishers_median_price[index][1], 2)} "
                f"/ Mean age of titles in years: {round(publishers_mean_age[index][1], 2)} "
                f"/ Median age of titles in years: {round(publishers_median_age[index][1], 2)}"
                ) 
                for index, publisher 
                in enumerate(publishers_count)
            ]
            data = data_all
        elif what_to_search == "p" and type_of_search == "a":
            s_input = input(
                f"What publisher should I search for (the search is case insensitive)?   ")
            s_input = s_input.strip().lower()
            data_titles = get_all_data("t")
            data_publishers = data[data["name"].str.contains(
                s_input, case=False, na=False)]
            data = data_titles.merge(
                data_publishers, how="inner", on="publisher_id")
        if data.empty:
            print(
                "--------------------------------------------------------------------------")
            print(
                f"There are no results for the given search of: {ft_input}! Please try again.")
            print(
                "--------------------------------------------------------------------------")
        elif what_to_search == "p" and type_of_search == "s":
            continue
        else:
            pd.set_option("display.max_rows", None)
            data.drop(["title_id", "publisher_id"], axis=1, inplace=True)
            data.reset_index(drop=True, inplace=True)
            print(data)


if __name__ == "__main__":
    main()
