import csv
from fuzzywuzzy import fuzz

refined_sightings = []

def isAlias(id, name):
    result = False
    for alias in animal_aliases:
        #print id + " " + name
        if alias["id"] == id:
            if fuzz.ratio(alias["alias"].lower(), name.lower()) >= 90:
                result = True
                break
    return result

def processBatch(raw_sightings):
    for raw_sighting in raw_sightings:
        #print raw_sighting["Record ID"]

        for animal in animals:
            #print animal["id"]

            if (isAlias(animal["id"], raw_sighting["Scientific Name"]) or
                isAlias(animal["id"], raw_sighting["Matched Scientific Name"]) or
                isAlias(animal["id"], raw_sighting["Vernacular Name - matched"]) or
                isAlias(animal["id"], raw_sighting["Vernacular Name"]) or
                isAlias(animal["id"], raw_sighting["Species - matched"]) and
                raw_sighting["Latitude - processed"] != "" and
                raw_sighting["Longitude - processed"] != ""):

                temp = {'id':animal["id"],'latitude':raw_sighting["Latitude - processed"],'longitude':raw_sighting["Longitude - processed"]}
                print "Found " + str(animal["display_name"]) + " " + str(temp)
                refined_sightings.append(temp)


with open('animal_aliases.csv') as f:
    animal_aliases = list(csv.DictReader(f))

with open('animals.csv') as f:
    animals = list(csv.DictReader(f.read().splitlines()))



with open('bio_blitz_melb_data.csv') as f:
    melb_sightings = list(csv.DictReader(f.read().splitlines()))

processBatch(melb_sightings)



with open('atlas_of_living_aus_data.csv') as f:
    ala_sightings = list(csv.DictReader(f.read().splitlines()))

processBatch(ala_sightings)


keys = refined_sightings[0].keys()
with open('processed_sightings_combined.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(refined_sightings)