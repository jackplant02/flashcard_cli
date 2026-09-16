from db import add_card, get_all_cards, init_db

def main():

    init_db()

    print("\nWelcome back!\n")
    print("Pick pick a subject to begin:\n")
    # option to create a new deck
    print("1: Create a new deck\n")

    # get all existing subjects
    """
    TODO: create a db of all existing subjects. Add a helper method in db.py 
        that simply returns all of the subject names, then print them out. 
    """ 

    # for loop to print out each of the retrieved subjects
    

    while True:
        entry = input("Please choose one of the following options: (a)dd a card, (s)tudy cards, or (q)uit: ").strip().lower()

        if entry == "q":
            break

        elif entry == "a":
            front = input("\nEnter front text: ").strip()
            back = input("Enter back text: ").strip()

            if front and back:
                add_card(front, back)
                print(f"Saved to database: front='{front}', back='{back}'\n")

        else:
            print("\nOops this program doesn't actually do anything yet lol.")
            print("Bye.\n")
            break

if __name__ == "__main__":
    main()