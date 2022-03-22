import csv
import re
from io import TextIOWrapper
from zipfile import ZipFile

cols_map = {"Producer": ["producers"],
            "Award": ["award_type"],
            "Film": ["film_id", "film_name", "imdb_rating", "imdb_votes",
                     "movie_time", "year_of_release", "oscar_year", "award_type",
                     "producers"],
            "Person": ["name"],
            "Actor": ["name"],
            "Director": ["name"],
            "Author": ["name"],
            "ActedIn": ["film_id", "name"],
            "Directed": ["film_id", "name"],
            "Wrote": ["film_id", "name"],
            "Produced": ["film_id", "name"],
            "ContentRating": ["content_rating"],
            "Rated": ["film_id", "content_rating"],
            "MovieGenre": ["genre"],
            "GenreOf": ["film_id", "genre"]
            }

# opens file for oscars table.
# CHANGE!

outfile = open("oscars.csv", 'w', encoding="utf-8", newline='')
outwriter = csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_NONE)

# Create output csv files
tables_list = ["Producer", "Award", "Film", "Person", "Actor", "ActedIn", "Author", "Wrote", "Director", "Directed",
               "ContentRating", "Rated", "MovieGenre", "GenreOf"]
out_tables = {table: open(table + ".csv", 'w', encoding="utf-8", newline='') for table in tables_list}

# Create a map between writers to output files and file\table name
writers_map = {table: csv.writer(out_tables[table], delimiter=",", quoting=csv.QUOTE_NONE) for table in out_tables}

# Write column names
for table in writers_map:
    writers_map[table].writerow(cols_map[table])

# Create "inventory" of unique values
films_ids = set()
producers = set()
directors = set()
actors = set()
authors = set()
genres = set()
content_rating = set()
award = set()
persons = set()
acted_in = set()
directed = set()
wrote = set()



# process_file goes over all rows in original csv file, and sends each row to process_row()
# DO NOT CHANGE!!!
def process_file():
    with ZipFile('archive.zip') as zf:
        with zf.open('oscars_df.csv', 'r') as infile:
            reader = csv.reader(TextIOWrapper(infile, 'utf-8'))
            for row in reader:
                # remove some of the columns
                chosen_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 29]
                row = [row[index] for index in chosen_indices]

                # change "," into && in list values
                lists_values_indices = [7, 11, 12, 13]
                for list_value_index in lists_values_indices:
                    row[list_value_index] = row[list_value_index].replace(',', '&&')

                # pre-process : remove all quotation marks from input and turns NA into null value ''.
                row = [v.replace(',', '') for v in row]
                row = [v.replace("'", '') for v in row]
                row = [v.replace('"', '') for v in row]
                row = [v if v != 'NA' else "" for v in row]

                # In the first years of oscars in the database they used "/" for example 1927/28,
                # so we will change these.
                row[2] = row[2].split("/")[0]

                # In 1962 two movies were written as winners, then we change one of them to nominee.
                if row[4] == "Winner" and row[2] == "1962" and row[14] == "8d5317bd-df12-4f24-b34d-e5047ef4665e":
                    row[4] = "Nominee"

                # In 2020 Nomadland won and marked as nominee by mistake.
                if row[2] == "2020" and row[1] == "Nomadland":
                    row[4] = "Winner"

                process_row(row)

    # flush and close the file. close all of your files.
    outfile.close()


# return a list of all the inner values in the given list_value.
# you should use this to handle value in the original table which
# contains an inner list of values.
# DO NOT CHANGE!!!
def split_list_value(list_value):
    return list_value.split("&&")


# process_row should splits row into the different csv table files
# CHANGE!!!
def process_row(row):
    outwriter.writerow(row)
    if row[0] == "":
        return
    # Write to Director
    check_and_write_unique_values(row[11], writers_map["Director"], directors, True)
    # Write to Actor
    check_and_write_unique_values(row[13], writers_map["Actor"], actors, True)
    # Write to Authors
    check_and_write_unique_values(row[12], writers_map["Author"], authors, True)
    # Write to Producer
    check_and_write_unique_values(row[3], writers_map["Producer"], producers, False)
    # Write to MovieGenre
    check_and_write_unique_values(row[7], writers_map["MovieGenre"], genres, False)
    # Write to content rating
    check_and_write_unique_values(row[10], writers_map["ContentRating"], content_rating, False)
    # Write to Award
    check_and_write_unique_values(row[4], writers_map["Award"], award, False)
    # Write to Film
    writers_map["Film"].writerow([row[14], row[1], row[8], row[9], row[6], row[5], row[2], row[4], row[3]])
    # Write to Acted in
    check_and_write_relations(row[14], row[13], acted_in, writers_map["ActedIn"])
    # Write to Directed
    check_and_write_relations(row[14], row[11], directed, writers_map["Directed"])
    # Write to Wrote
    check_and_write_relations(row[14], row[12], wrote, writers_map["Wrote"])
    # Write to GenreOf
    check_and_write_non_unique_values(row[14], row[7], writers_map["GenreOf"])
    # Write to Rated
    check_and_write_non_unique_values(row[14], row[10], writers_map["Rated"])

# return the list of all tables
# CHANGE!!!
def get_names():
    return tables_list


def check_and_write_non_unique_values(film_id, val_to_split, writer):
    if val_to_split != "":
        separated_values = re.split('&& | &&|&&', val_to_split)
        new_rows = [[film_id, val] for val in separated_values]
        writer.writerows(new_rows)


def check_and_write_unique_values(cell, writer, prev_data, is_person):
    separated_values = re.split('&& | &&|&&', cell)
    for val in separated_values:
        if val and val not in prev_data:
            prev_data.add(val)
            writer.writerow([val])
            if is_person and val not in persons:
                persons.add(val)
                writers_map["Person"].writerow([val])

def check_and_write_relations(film_id, values_string, prev_data, writer):
    separated_values = re.split('&& | &&|&&', values_string)
    new_rows = list()

    for val in separated_values:
        if val and (film_id, val) not in prev_data:
            prev_data.add((film_id, val))
            new_rows.append([film_id, val])

    writer.writerows(new_rows)


if __name__ == "__main__":
    process_file()
    for table in out_tables.values():
        table.close()
