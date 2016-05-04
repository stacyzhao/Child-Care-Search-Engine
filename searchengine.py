import psycopg2
import csv

conn = psycopg2.connect("dbname=childcare user=stacy host=/tmp/")
cur = conn.cursor()

# create_table = ("CREATE TABLE childcare(id serial PRIMARY KEY NOT NULL, "
#                 "LOC_ID INT, "
#                 "LOC_NAME TEXT, "
#                 "STR_NO INT, "
#                 "STREET TEXT, "
#                 "PCODE TEXT, "
#                 "WARDNUMBER TEXT, "
#                 "PHONE TEXT, "
#                 "IGSPACE INT, "
#                 "TGSPACE INT, "
#                 "PGSPACE INT, "
#                 "KGSPACE INT, "
#                 "SGSPACE INT, "
#                 "TOTSPACE INT, "
#                 "SUBSIDY TEXT);")
#
# cur.execute(create_table)

with open('childcare.csv') as childcare:
    data = csv.reader(childcare)
    next(data)
    for row in data:
        r = [row[0], row[1], row[3], row[4], row[6], row[7], row[8], row[11],
             row[12], row[13], row[14], row[15], row[16], row[17]]
        cur.execute("INSERT INTO childcare (" +
                    "LOC_ID, LOC_NAME, STR_NO, STREET, PCODE,"
                    "WARDNUMBER, PHONE, IGSPACE, TGSPACE, PGSPACE,"
                    "KGSPACE, SGSPACE, TOTSPACE, SUBSIDY)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, \
                    %s, %s, %s, %s, %s, %s)", r)


# cur.execute("SELECT LOC_NAME, PHONE FROM childcare WHERE STR_NO = '600' \
#             ORDER BY LOC_ID;")


def user_menu():
    print("What would you like to find out?")
    user_choice = int(input("\n \
        (1) Search for spots by age \n \
        (2) Search by postal code \n \
        (3) Search if day care subsidy is available \n \
        (4) Update a location \n "))

    if user_choice == 1:
        spot_by_age()
    elif user_choice == 2:
        postal_code()
    elif user_choice == 3:
        subsidy()
    elif user_choice == 4:
        update()
    else:
        print("theres no more options!")


def spot_by_age():
    user_child_age = int(input("How old is your child?"))

    if user_child_age <= 1:
        cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE, IGSPACE \
            FROM childcare WHERE IGSPACE > 0 ORDER BY IGSPACE;")

    elif user_child_age > 1 and user_child_age <= 3:
        cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE, TGSPACE \
            FROM childcare WHERE TGSPACE > 0 ORDER BY TGSPACE;")

    elif user_child_age > 3 and user_child_age <= 4:
        cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE, PGSPACE \
            FROM childcare WHERE PGSPACE > 0 ORDER BY PGSPACE;")

    elif user_child_age > 5 and user_child_age <= 6:
        cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE, KGSPACE \
                FROM childcare WHERE KGSPACE > 0 ORDER BY KGSPACE;")

    elif user_child_age > 6:
        cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE, SGSPACE \
                FROM childcare WHERE SGSPACE > 0 ORDER BY SGSPACE;")
    return print_result(cur.fetchall())


def print_result(results):
    for result in results:
        print("Location: ", result[0])
        print("Address: ", result[1], result[2])
        print("Phone Number: ", result[3])
        print("\n\n")
        # if result[4] is not None:
        #     print("Spots Available: ", result[4])
        #     print("\n\n")


def postal_code():
    postal = input("What is your postal code? \n").upper()
    cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE \
        FROM childcare WHERE PCODE = '{}';".format(postal))
    return print_result(cur.fetchall())


def subsidy():
    sub = input("(Y)es or (N)o for subsidy daycare? \n").upper()
    cur.execute("SELECT LOC_NAME, STR_NO, STREET, PHONE \
            FROM childcare WHERE SUBSIDY = '{}';".format(sub))
    return print_result(cur.fetchall())


def update():
    loc_id = input("What is the location ID?")
    print("What woud you like to update?")
    location = input("Location Name: \n").title()
    number = input("Number: \n")
    postal = input("Postal Code: \n").upper()

    cur.execute("UPDATE childcare SET LOC_NAME = '{}', PHONE = '{}', \
        PCODE = '{}' WHERE LOC_ID = '{}';".format(location, number, postal, loc_id))



user_menu()


# conn.commit()

cur.close()

conn.close()




# print(cur.fetchall())
# cur.execute("SELECT * FROM childcare WHERE street LIKE '%Ave%'")


# cur.execute("COPY childcare(LOC_ID, LOC_NAME, AUSPICE, STR_NO, STREET, " +
#            "UNIT, PCODE, WARDNUMBER, PHONE, BLDG_TYPE) FROM " +
#            "'/Users/stacy/dev/Child-Care-Search-Engine/childcare.csv' " +
#            "DELIMITER',' CSV")
