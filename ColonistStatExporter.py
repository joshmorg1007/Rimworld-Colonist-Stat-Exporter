import xml.etree.ElementTree as ET
import getopt
import sys
import csv

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('ColonistStatExporter.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('ColonistStatExporter.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   parse(inputfile, outputfile)

def parse(input_path, output_path):
    stat_titles = ["Colonist Name", "Total Kills", "Human Kills", "Animal Kills", "Mech Kills", "Total Knockouts","Human Knockouts", "Animal Knockouts", "Mech Knockouts", "Shots Fired", "Headshots", "Damage Dealt", "Damage Taken", "Mental Breaks",
     "Times on Fire", "Fires Extinguished", "Operations Recieved", "Operations Performed", "Wound Treatment Recieved", "Wound Treatment Given", "People Captured", "Prison Recruited", "Number of Times Chatted to Prisoners", "Animals Tamed",
     "Animals Slaughtered", "Meals Cooked", "Things Constructed", "Things Installed", "Things Repaired", "Things Crafted", "Things Hauled", "Plants Sown", "Plants Harvested", "Cells Mined", "Messes Cleaned", "Research Points",
      "Corpses Buried", "Nutrition Eaten", "Bodies Stripped", "Things Uninstalled", "Things Deconstructed", "Artifacts Activated", "Containers Opened", "Switches Flicked", "Time as a Colonist", "Time Hosted", "Time as Prisoner",
      "Time in a Bed", "Time in a Medical Bed", "Time Downed", "Time finding Food and Eating", "Time Spend on Entertainment", "Time Under a Roof", "Time Drafted", "Time on Fire", "Time in Mental State", "Time Hauling", "Time Handling Animals",
      "Time Spend Firefighting", "Time Spend Wardening", "Time Spend Hunting", "Time Spend Constructing", "Time Treating and Feeding", "Time Researching", "Time Spent Cleaning", "Time Spend Repairing", "Time Spend Mining", "Time Spend Sowing And Harvesting"]

    colonist_nodes = list()
    colonists_dict = dict();

    tree = ET.parse(input_path)
    root = tree.getroot()

    for entry in root.iter('thing'):
        entry_class = entry.attrib.get('Class')
        if(entry_class == "Pawn"):
            for child in entry.iter('kindDef'):
                if(child.text == "Colonist"):
                    colonist_nodes.append(entry)

    for col in colonist_nodes:
        name = col.findall(".//name/nick")[0].text
        records = col.findall(".//records/records/vals/li")
        colonist_stats = list()
        for record in records:
            colonist_stats.append(record.text)

        colonists_dict[name] = colonist_stats

    export_to_csv(output_path, colonists_dict, stat_titles)


def export_to_csv(output_file, dict, titles):
    with open(output_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(titles)

        for colonist in dict.items():
            row = list()
            row.append(colonist[0])
            for entry in colonist[1]:
                row.append(entry)

            spamwriter.writerow(row)

if __name__ == "__main__":
    main(sys.argv[1:])
