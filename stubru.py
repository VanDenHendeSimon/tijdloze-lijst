import json
import re


def json_to_dict():
    json_path = "./data/fast_groepen_opgave2-stubru.json"

    # Init dict to fill with data from json
    d = dict()

    with open(json_path) as json_file:
        # Store json_file's data in dict
        d = json.loads(json_file.read())

    return d


def input_a():
    # Toon huidige tijdloze lijst
    # (Plaats/vorige plaats/verschil/titel/artiest)
    for song in data_dict.get("songs", []):

        # Get data of the curerntly checked song
        position = song.get("position", 0)
        previous = song.get("previous", 0)
        difference = abs(position - previous)
        title = song.get("title", "title not found")
        artist = song.get("name", "artist(s) not found")

        # Print to user
        print(
            "%s van %s staat op de %de plaats." % (
                title, artist, position
            )
        )

        # Print about position
        if previous != 0:
            if previous < position:
                # daling
                print(
                    "Dat is een daling van %d plaatsen "
                    "in vergelijking met vorig jaar" % (
                        difference
                    )
                )
            else:
                # stijging
                print(
                    "Dat is een stijging van %d plaatsen "
                    "in vergelijking met vorig jaar" % (
                        difference
                    )
                )
            # vergelijking
            print(
                "Toen stond dit nummer nog op de %de plaats." % (
                    previous
                )
            )
        else:
            print("Vorige plaats is niet bekend.")

        print("")


def input_b():
    # Toon huidige tijdloze lijst (Aflopend op plaats)
    """
    # minste hoeveelheid code maar werkt enkel
    # omdat de keys van de dict al in de juiste volgorde staan
    nummers = [x["title"] + " van " + x["name"] for x in data_dict["songs"]]
    for index, song in enumerate(reversed(nummers)):
        print(
            "%d. %s" % (
                (len(nummers) - index), song
            )
        )
    """

    # meer robuste manier, maar ook meer code
    nummers = {}

    # Create dict with 'title van artist' as key and
    # position as value for easier sorting
    for song in data_dict.get("songs", []):
        title = song.get("title", "Onbekend")
        artist = song.get("name", "Onbekend")
        position = song.get("position", 0)

        nummers[title + " van " + artist] = position

    # Sorteer de lijst (k) op basis van de positie (v)
    nummers_aflopend = sorted(
        nummers.items(),
        key=lambda kv: kv[1],
        reverse=True
    )

    # Print gesorteerde lijst + positie
    for song in nummers_aflopend:
        print(
            "%d. %s" % (
                song[1], song[0]
            )
        )


def input_c():
    # Toon de songs van de tijdloze lijst van een ander jaartal
    jaartal = input("Van welk jaartal wil je de song(s) zien? ")

    try:
        jaartal = int(jaartal)

        for song in data_dict.get("songs", []):
            release_date = song.get("release_date", None)

            if release_date:
                print(
                    "%s kwam uit op %s" % (
                        song.get("title", "Onbekend"), release_date
                    )
                )
            else:
                print(
                    "release date van %s is onbekend" % (
                        song.get("title", "Onbekend")
                    )
                )

    except ValueError:
        print("Ongeldige waarde\n")
        input_c()


def input_d():
    # Toon enkel de songs die gestegen zijn ten opzichte van vorig jaar.
    for song in data_dict.get("songs", []):
        position = song.get("position", 0)
        previous = song.get("previous", 0)

        if position != 0 and previous != 0:
            if position < previous:
                difference = abs(position - previous)
                print(
                    "%s van %s steeg met %s %s (%d → %d)" % (
                        song.get("title", "Onbekend"),
                        song.get("name", "Onbekend"),
                        difference,
                        "plaatsen" if difference > 1 else "plaats",
                        previous,
                        position
                    )
                )


def input_e():
    # Geef een lijst vansong(s) van een bepaalde artiest
    artiest = input("Van welke artiest wil je de song(s) zien? ")
    matches = False

    for song in data_dict.get("songs", []):
        if artiest.lower() == song.get("name", "onbekend").lower():
            matches = True
            print(
                "%s is van %s en staat op de %de plaats" % (
                    song.get("title", "Onbekend"),
                    artiest,
                    song.get("position", 0)
                )
            )

    if not matches:
        print("Geen enkel nummer van %s staat in de lijst" % artiest)


def input_f():
    # Geef een lijst van song(s) waar volgend woord in de lyric staat
    lyric = input("Welk(e) woord(en) wil je in de song(s) zien? ")
    matches = False

    for song in data_dict.get("songs", []):
        # Get lyrics
        lyrics = song.get("lyrics", None)

        # Check if we have valid lyrics to check against
        if lyrics:
            # Check for each given word
            list_of_words = lyric.split(" ")
            # Init counter to make sure every input word is in the lyrics
            amount_of_matches = 0

            for word in list_of_words:
                # Prevent 'test' to be found if 'sweetest' is in the song
                # - Johnny Cash, Hurt
                # Also check that the full string is in the lyrics
                # to prevent parts being scattered
                if (
                    re.search(r"\b(%s)\b" % word.lower(), lyrics.lower()) and
                    lyric.lower() in lyrics
                ):
                    matches = True
                    amount_of_matches += 1

            if amount_of_matches == len(list_of_words):
                print(
                    "%s van %s bevat %s" % (
                        song.get("title", "Onbekend"),
                        song.get("name", "Onbekend"),
                        " ".join(list_of_words)
                    )
                )

    if not matches:
        print("Geen enkel nummer bevat %s" % lyric)


def input_g():
    # Toon de top 10 artiesten die het meest in de lijst voorkomen.
    artiesten_dict = {}

    # Create dict with artists (k)
    # and amount of songs in the list (v) for easy sorting
    for song in data_dict.get("songs", []):
        artiest = song.get("name", "")

        if artiest in artiesten_dict.keys():
            # if the artist is already a key, add a song to its name
            artiesten_dict[artiest] += 1
        else:
            # if the artist is not in the dict yet, set song count to 1
            artiesten_dict[artiest] = 1

    # Sort dict
    artiesten = sorted(
        artiesten_dict.items(),
        key=lambda kv: kv[1],
        reverse=True
    )

    # Get the least amount of songs in the top 10
    minst_nummers_in_top_10 = artiesten[9][1]
    ex_aequo_artiesten = []

    # Add all the artist that have that amount of songs to this list
    for artiest in artiesten:
        if artiest[1] == minst_nummers_in_top_10:
            ex_aequo_artiesten.append(artiest[0])

    for i in range(10):
        # verwijder artiesten die op de laatste plaats staan
        # maar toch in de top 10 getoond worden
        if artiesten[i][0] in ex_aequo_artiesten:
            ex_aequo_artiesten.remove(artiesten[i][0])

        print(
            "%s met %s nummers %s" % (
                artiesten[i][0],
                artiesten[i][1],
                ""
                if i < 9 else
                "(Gedeelde laatste plaats met %s)" %
                ", ".join(ex_aequo_artiesten)
            )
        )


def input_h():
    # Toon de huidige (en de vorige) posities van één bepaalde song.
    nummer = input(
        "Van welk nummer wil je graag de huidige en de vorigie positie? "
    )
    # No matches found by default
    matches = False

    # Check for each song
    for song in data_dict.get("songs", []):
        # If the input song is the same
        # as the title of the currently check songtitle
        if nummer.lower() == song.get("title", "").lower():
            # we have a match
            matches = True

            # Print what we know
            print(
                "De huidige positie van dit nummer is %s" % (
                    "onbekend"
                    if song.get("position", 0) == 0 else
                    song["position"]
                    )
            )
            print(
                "De vorige positie van dit nummer was %s" % (
                    "onbekend"
                    if song.get("previous", 0) == 0 else
                    song["previous"]
                    )
            )

    # If the input song doesn't match any of the songtitles in the list
    if not matches:
        print("%s staat niet in de lijst.\nCheck de spelling" % nummer)


def input_i():
    # Toon de top 15 songs die het langs in de lijst hebben gestaan.
    songs = {}

    # Create dict with titles (k) and amount of ranks (v) for easy sorting
    for song in data_dict.get("songs", []):
        songs[song.get("title", "")] = len(song.get("rank", []))

    # Sorteer de songs op basis van de hoeveelheid ranks
    sorted_songs = sorted(
        songs.items(),
        key=lambda kv: kv[1],
        reverse=True
    )

    # Get the least amount of ranks in the top 15
    minst_jaren = sorted_songs[14][1]
    songs_minst_jaren = []

    # Store every song that has the same amount of ranks
    for song in sorted_songs:
        if song[1] == minst_jaren:
            songs_minst_jaren.append(song[0])

    # Display top 15
    for i in range(15):
        # If there are multiple songs with the lowest years
        # that already displayed we dont want to display them again
        # So take them out of the list we will display at the end
        if sorted_songs[i][0] in songs_minst_jaren:
            songs_minst_jaren.remove(sorted_songs[i][0])

        if i < 14:
            # Print eerste 14 normaal
            print(
                "%s stond %d jaar in de lijst" % (
                    sorted_songs[i][0],
                    sorted_songs[i][1]
                )
            )
        else:
            if len(songs_minst_jaren) > 0:
                # Indien er meerder songs zijn met
                # dezelfde hoeveeltijd jaren als de laatste,
                # vermeld deze dan ook
                print(
                    "%s stond %d jaar in de lijst %s" % (
                        sorted_songs[i][0],
                        sorted_songs[i][1],
                        "(Gedeeld met %s)" % ", ".join(songs_minst_jaren)
                    )
                )
            else:
                # Indien er geen gedeelde laatste plaats is,
                # print normaal
                print(
                    "%s stond %d jaar in de lijst" % (
                        sorted_songs[i][0],
                        sorted_songs[i][1]
                    )
                )


def request():
    # Get name
    if data_dict.get("data", None):
        name = data_dict["data"].get("name", "ons")
    else:
        name = "ons"

    # Print welkom
    print("\nWelkom bij %s, wat wil je doen?" % name)
    print("-"*80)

    # Display choices
    print(
        "A) Toon huidige tijdloze lijst "
        "(Plaats/vorige plaats/verschil/titel/artiest)")
    print("B) Toon huidige tijdloze lijst (Aflopend op plaats)")
    print("C) Toon de songs van de tijdloze lijst van een bepaald jaartal")
    print(
        "D) Toon enkel de songs die gestegen zijn "
        "ten opzichte van vorig jaar.")
    print("E) Geef een lijst van song(s) van een bepaalde artiest")
    print("F) Geef een lijst van song(s) waar volgend woord in de lyric staat")
    print("G) Toon de top 10 artiesten die het meest in de lijst voorkomen.")
    print("H) Toon de huidige (en de vorige) posities van éénbepaalde song.")
    print("I) Toon de top 15 songs die het langs in de lijst hebben gestaan.")
    print("S) Stop")

    keuze = input("Wat wil je doen: ")

    # Execute code based on the user input
    if keuze.lower() == "a":
        input_a()
    elif keuze.lower() == "b":
        input_b()
    elif keuze.lower() == "c":
        input_c()
    elif keuze.lower() == "d":
        input_d()
    elif keuze.lower() == "e":
        input_e()
    elif keuze.lower() == "f":
        input_f()
    elif keuze.lower() == "g":
        input_g()
    elif keuze.lower() == "h":
        input_h()
    elif keuze.lower() == "i":
        input_i()
    elif keuze.lower() == "s":
        exit()
    else:
        print("Commando werd niet herkend\n")
        request()

# Fill dict with data from json
data_dict = json_to_dict()
# Ask user what to do next
request()
