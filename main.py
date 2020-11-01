# Creates new .txt file with all numbers scaled by X amount
# Works for any ideas
# Works for every policy except "religious_unity", since it's both an ai modifier and a nation modifier.

# To use rename variable fileName to name of .txt you want to change
# Note: My own implementation will use command line arguments
# Change variable SCALE to any number for x times ideas

import sys
import os
from pathlib import Path
import re
from collections import Counter

# If specific potential modifiers need to be discounted, put them here.
EXCLUDED_WORDS = ["vassal", "num_of_cities", "num_of_ports", "province_id", "is_year", "factor",
                  "legitimacy", "tax_income_percentage", "army_size_percentage", "average_effective_unrest",
                  "colonist_placement_chance", "average_autonomy_above_min", "production_income_percentage",
                  "trade_income_percentage", "navy_size", "historical_start_date", "started_in",
                  "set_revolution_target", "date", "value", "duration", "num_free_building_slots",
                  "years", "yearly_decay", "opinion", "nation_designer_cost", "year", "cost", "max_level",
                  "location", "months", "category", "territory", "icon", "stability", "max", "artillery", "infantry",
                  "cavalry", "morale", "min", "province_has_center_of_trade_of_level", "amount", "time",
                  "random_nation_chance", "cooldown_years", "cavalry_cap", "sprite", "claim", "sprite_level",
                  "corruption", "base_price", "imperial_mandate", "manpower_percentage", "land_share", "liberty_desire",
                  "power", "hull_size", "base_cannons," "sail_speed", "fixed_rank", "artillery_weight", "days",
                  "crown_land_share", "cost_modifier", "distance", "num_of_cardinals", "DIP", "total_development",
                  "adm", "mil", "dip_tech", "lose_reforms", "dip", "num_of_rebel_controlled_provinces", "base_manpower",
                  "adm_tech", "default_option", "ADM", "colony", "heir_DIP", "consort_DIP", "absolutism", "owns",
                  "base_tax", "army_size", "MIL", "overextension_percentage", "navy_size_percentage", "base_influence",
                  "home_province", "skill", "heir_ADM", "heir_MIL", "consort_MIL", "grain", "default",
                  "total_own_and_non_tributary_subject_development", "janissary_percentage", "consort_ADM",
                  "num_of_trade_companies", "government_rank", "fish", "animism", "heir_dip", "num_of_rebel_armies",
                  "mil_tech", "start_territory_to_estates", "frame", "variable_initial", "penalty", "personal_union",
                  "fort_level", "treasury", "consort_dip", "fur", "cossacks_percentage", "printing_press",
                  "industrialization", "button_gfx", "army_professionalism", "gift_chance", "gold",
                  "monarch_military_power", "monarch_diplomatic_power", "num_of_missionaries", "num_of_conquistadors",
                  "num_of_explorers", "factions_frame", "flags_with_emblem_percentage", "easy_war_chance_multiplier",
                  "base_liberty_desire", "ship_power_propagation", "legitimacy_equivalent", "consort_adm",
                  "naval_supplies", "shamanism", "level", "average_home_autonomy", "heir_adm", "nationalism",
                  "curia_treasury_contribution", "global_trade", "enlightenment", "isolation_value",
                  "base_conversion_speed", "relative_power_class", "start", "papacy", "sugar", "cocoa", "heir_mil",
                  "num_of_allies", "average_unrest", "feudalism", "manufactories", "cavalry_fraction",
                  "infantry_fraction", "defect_delay", "war_chance_multiplier", "building_budget_multiplier",
                  "devastation", "liberty_desire_development_ratio", "allowed_idea_groups", "num_of_colonies",
                  "consort_mil", "ruler_age", "cotton", "years_of_income", "remove_claim", "trade_company_size",
                  "cooldown_months", "num_of_light_ship", "province", "renaissance", "new_world_i", "innovativeness",
                  "current_institution", "tech_difference", "sailors_percentage", "artillery_fraction",
                  "enemy_strength_multiplier", "different_religion_war_multiplier", "gold_income_percentage",
                  "military_focus", "num_of_continents", "seat_in_parliament", "trade_ideas", "aristocracy_ideas",
                  "ai_peace_desire", "mercantilism", "inuit", "nakota", "cheyenne", "iroquois", "abenaki", "tobacco"
                  "dakota", "shoshone", "salt", "wool", "piman", "navajo", "inca", "copper", "guarani", "noOfFrames",
                  "color", "legitimacy_or_horde_unity", "revolt_percentage", "current_size_of_parliament",
                  "num_of_janissaries", "num_of_free_diplomatic_relations", "num_of_subjects", "is_claim",
                  "max_manpower", "num_of_trading_bonuses", "piety", "num_of_diplomatic_relations",
                  "owns_core_province", "alliance_acceptance", "royal_marriage_acceptance", "heir_age",
                  "army_organiser", "army_reformer", "commandant", "grand_captain", "recruitmaster",
                  "fortification_expert", "quartermaster", "treasurer", "philosopher", "artist", "master_of_mint",
                  "inquisitor", "natural_scientist", "statesman", "diplomat", "naval_reformer", "trader",
                  "colonial_governor", "navigator", "spymaster", "local_autonomy_above_min", "max_government_rank",
                  "pays_overlord", "forcelimit_bonus", "trust_on_start", "liberty_desire_revolution",
                  "owns_or_vassal_of", "university", "num_of_owned_and_controlled_institutions", "administrative_ideas",
                  "economic_ideas", "plutocracy_ideas", "spy_ideas", "diplomatic_ideas", "innovativeness_ideas",
                  "offensive_ideas", "defensive_ideas", "quality_ideas", "quantity_ideas", "religious_ideas",
                  "exploration_ideas", "maritime_ideas", "expansion_ideas", "num_of_coalition_members", "manpower",
                  "aleutian", "cree", "anishinabe", "huron", "mikmaq", "creek", "choctaw", "chickasaw", "cherokee",
                  "shawnee", "powhatan", "delaware", "susquehannock", "pequot", "iron", "chiwere", "pawnee", "osage",
                  "caddo", "pueblo", "aztek", "zapotek", "mayan", "arawak", "carib", "guajiro", "aimara", "patagonian",
                  "chacoan", "tupinamba", "num_symbols", "capital", "add_claim", "silk", "spices", "tea",
                  "num_of_powerful_estates", "num_of_aspects", "discovered_relations_impact", "local_heir_adm",
                  "local_heir_dip", "local_heir_mil", "governing_cost", "num_of_centers_of_trade", "num_of_heavy_ship",
                  "alert_index", "imperial_influence", "church_power", "fervor", "add_next_institution_embracement",
                  "patriarch_authority", "government_reform_progress", "cost_multiplier", "colonysize",
                  "power_cost_base", "ae_base", "reserves_organisation", "remove_religious_reforms", "election_cost",
                  "curia_treasury_cost", "reform_desire", "add_reform_desire_scale", "authority",
                  "num_of_royal_marriages", "other_ai_help_us_multiplier", "other_ai_peace_term_bonus",
                  "other_ai_war_chance_multiplier", "peace_desire", "consort_age", "trade_league_acceptance",
                  "send_warning_desire", "age", "DURATION", "theologian", "current_institution_growth",
                  "development_of_overlord_fraction", "cities_required_for_bonuses"]

word_list = []

# RegEx setup
'''The Regex explanation, in steps
Begin at the start of the line (^)
Find zero or more tabs (\t*). Combined with above, useful for filtering out comments
Capture the name of the modifier, including the underscore (([a-zA-Z_]+)) (capture group 1)
Find " = ", accounting for whitespace ( *= *)
Capture the value of the modifier (([0-9.-]+)), accounting for decimals and negatives (capture group 2)
Note: Removing the negative will prevent the changing of negative values, while placing it near the beginning will only
allow changing negative values. Doesn't account for if the negative modifier is actually positive or negative.
End at the end of the line ($)
'''
# Compile the regexes (since it's going to be used many times)
# Regex used to find modifier and number
modifier_regex = re.compile('^\t*([a-zA-Z_]+) *= *([0-9.-]+)$', flags=re.MULTILINE)
# Regex used to find number specifically
number_regex = re.compile('([0-9.-]+)', flags=re.MULTILINE)

''' Depreciated function
def name_converter(filename: str, scale: int) -> str:
    # Converts the original file name to a new file name, referencing the scale change
    # Example: file_name.txt -> file_nameScaledx10.txt
    filename2 = filename[:-4]  # Removes the .txt portion and stores the rest
    return filename2 + "Scaled" + "x" + str(scale) + ".txt"  # Add Scaledx(scale), and restores the .txt extension
'''
'''opinion'''


def file_search_modify_scale(filename, directory, output_directory, scale_input):
    input_filename: str = filename  # Grab the input filename from the input
    input_file = open(os.path.join(directory, input_filename), 'rt')  # Grab the input file itself and open it
    # Note: Grabs from the directory for source
    # Helpful: https://docs.python.org/3/tutorial/inputoutput.html#tut-files
    output_file = open(os.path.join(output_directory, input_filename), 'wt')
    # Create the output file and write into it
    # Note: Grabs from output_directory for destination

    input_file_lines = input_file.readlines()  # Puts all lines of the input file into a list.
    # Note: includes special characters like \n and EOF
    # output_file.writelines(input_file_lines)  # Test function to see how writing

    # Main loop to run through the file.
    # Using range(len(input_file_lines)), since I need the line number as well
    # Original implementation was for input_line in input_file_lines:
    for i in range(len(input_file_lines)):
        filter_broken = False  # Setup for the filter, uses EXCLUDED_WORDS
        # Test the current line with the RegEx
        input_line_regex_test_result = modifier_regex.match(input_file_lines[i])
        if input_line_regex_test_result is not None:  # If there is a successful match
            for mod_filter in EXCLUDED_WORDS:  # Run through every word in EXCLUDED_WORDS
                if str(mod_filter) == str(input_line_regex_test_result.group(1)):  # If a word in the filter is found
                    filter_broken = True  # A word has been found
                    output_file.write(input_file_lines[i])  # Copy directly from the source file and put it into the new
                    # file
                    break  # Leave the for loop since it's no longer necessary to loop through the rest
            if not filter_broken:  # If a filter word has not been found
                # print(str(i) + ": " + str(input_line_regex_test_result.group(1, 2)))  # Test
                # Here is where the fun begins
                try:
                    modified_line = re.sub(number_regex,
                                           str(float(input_line_regex_test_result.group(2)) * float(scale_input)),
                                           input_file_lines[i])
                except: # Bare excepts are a bad idea, but this is here to know where the program found an error.
                    print(input_filename + "," + str(i) + "," + input_file_lines[i] + "," + str(
                        input_line_regex_test_result.group(2)))
                    raise
                '''Explanation
                re.sub replaces sections of strings that matches a regex.
                Regex used was number_regex, specifically for capturing numbers
                Replacement was the originally detected number, multiplied by the scale
                String receiving the replacement is the current line in the input_file_lines array
                '''
                output_file.write(modified_line)  # Write nothing to the new file except for a new line.
                # Debug for seeing every RegEx match
                # print(str(i) + "\t" + str(input_line_regex_test_result.groups()))
                # print(str(input_line_regex_test_result.group(1)))
                word_list.append(str(input_line_regex_test_result.group(1)))
        else:
            output_file.write(input_file_lines[i])  # Copy directly from the source file and put it into the new file

    # Junk cleanup for good measure
    input_file.close()
    output_file.close()


def search_all_files_from_top(starting_folder_name, scale_input):
    folder_name = 'output_x' + str(scale_input)
    if not os.path.isdir(Path(folder_name)):  # Does the output directory exist?
        os.mkdir(Path(folder_name))  # If it doesn't, create it
    for root, dirs, files in os.walk(Path(starting_folder_name + '/')):  # Loop through the entire input directory
        # Clone the directory tree from the input
        os.makedirs(os.path.join(Path(folder_name + '/'), root), exist_ok=True)
        for file in files:  # Go through each file and apply the modify scale function, storing it in the output
            file_search_modify_scale(str(file), root, os.path.join(Path(folder_name), root), scale_input)


if __name__ == "__main__":
    scale = 10
    try:
        sys.argv[1] == sys.argv[1]
    except IndexError:
        print("Please enter an input folder")
        raise
    try:
        scale = sys.argv[2]
        print("Scale value: " + str(scale))
    except IndexError:
        print("No scale value entered, assuming 10")
    search_all_files_from_top(sys.argv[1], scale)
    print(Counter(word_list))
