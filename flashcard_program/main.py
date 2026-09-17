from db import init_db, get_all_subjects, add_subject

def main():

    init_db()

    print("\nWelcome back!\n")
    print("Pick pick a subject to begin:\n")
    # option to create a new deck
    print("(1) Create New Deck")

    # get all existing subjects
    subjects = get_all_subjects()

    for i, subject in enumerate(subjects):
        print(f"({i+2}) {subject}")

    selection = input("\nPlease enter your selection: ").strip()

    if selection == "1":
        add_subject(input().strip())

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