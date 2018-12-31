from syllable import Syllable
from phoneme import Phoneme
from affixes import Affixes

# TODO handle feature checks in language instead of shared Features dependency
#   - check before passing non C xor V to syll
#   - check before adding consonant or vowel to inventory
#   - check before adding features to phone

# TODO set up default letters and symbols

# TODO language handles checking inventory, environment, rules
#   - e.g. avoid ['smiles', '_', 'sauce'] allow ['vowel', '_', 'vowel']
#   - '0', '#' when applying rules

class Language:
    def __init__(self, name="", display_name="", features=None, inventory=None, rules=None):
        self.name = name
        self.display_name = display_name
        self.features = features
        self.inventory = inventory
        self.rules = rules
        self.affixes = Affixes()
        self.environments = {}  # instantiated environments
        self.syllables = {}     # set of syllables - inventory?
        self.phonemes = {}      # dict of created phonemes - inventory?

    def set_inventory(self, inventory):
        """Set the inventory object for this language"""
        self.inventory = inventory

    def set_features(self, features):
        """Set the features object for this language"""
        self.features = features

    # TODO compare with Rules.add checks already in place
    def add_rule(self, source, target, environment):
        if not (self.features.has_ipa(source) and self.features.has_ipa(target)):
            print("Language add_rule failed - invalid source or target symbols")
            return
        e = Environment(structure=environment)
        if not e.get():
            print("Language add_rule failed - invalid environment given")
            return
        self.rules.add(source, target, e)

    def add_syllable(self, syllable_structure):
        # build valid symbol or features list
        syllable_characters = ['_', '#', ' ', 'C', 'V']
        new_syllable = []
        for syllable_item in syllable_structure:
            if type(syllable_item) is str:
                if syllable_item not in syllable_characters or not self.features.has_feature(syllable_item):
                    print("Language add_syllable failed - invalid syllable item {0}".format(syllable_item))
                    return
                elif syllable_item == 'C':
                    new_syllable_structure.append(["consonant"])
                elif syllable_item == 'V':
                    new_syllable_structure.append(["vowel"])
                else:
                    new_syllable_structure.append([syllable_item])
            elif type(syllable_item) is list:
                for feature in syllable_item:
                    if not self.features.has_feature(syllable_item):
                        print("Language add_syllable failed - invalid syllable feature {0}".format(feature))
                        return
                new_syllable_structure.append(syllable_item)
        syllable = Syllable(new_syllable_structure)
        self.inventory.add_syllable(syllable)
        return

    def add_affix(self, category, grammar, affix):
        """Add a grammatical category and value affix in phonetic transcription"""
        for symbol in affix:
            if symbol != '-' or not self.inventory.has_ipa(symbol):
                print("Language add_affix failed - invalid affix {0}".format(affix))
                return
        self.affixes.add(category, grammar, affix)
        return self.affixes.get(affix)

    # TODO add weights for letter choice? for rules?
    #   - current weight intended for distributing phon commonness/freq of occ
    def add_sound(self, ipa, letters=[], weight=0):
        """Add one phonetic symbol, associated letters and optional weight to the language's inventory"""
        if not self.features.has_ipa(ipa) or not all(isinstance(l, str) for l in letters):
            print("Language add_sound failed - invalid phonetic symbol or letters")
            return {}
        sound = Phoneme(ipa, letters=letters, weight=weight)
        if ipa not in self.phonemes:
            self.phonemes[ipa] = {sound}
        else:
            self.phonemes[ipa].add(sound)
        # TODO decide if adding sounds to language (above) or managing through inventory (below)
        features = self.features.get_features(ipa)
        for letter in letters:
            self.inventory.add_letter(letter=letter, features=features)
        return {ipa: self.phonemes[ipa]}

    def add_sounds(self, ipa_letters_map):
        """Add multiple sounds to the language's inventory"""
        if type(ipa_letters_map) is not dict:
            print("Language add_sounds failed - expected dict not {0}".format(type(ipa_letters_map)))
            return
        sounds = {}
        for ipa, letters in ipa_letters_map.items():
            print(ipa)
            added_sound = self.add_sound(ipa, letters=letters)
            sounds.update(added_sound)
        return sounds

    def build_word(self, length=1):
        """Form a word following the defined inventory and syllable structure"""
        if not self.inventory and self.inventory.get_syllables():
            print("Language build_word failed - unrecognized inventory or inventory  syllables")
            return
        word = ""
        for i in range(length):
            syllable = random.choice(self.inventory.get_syllables())
            syllable_structure = syllable.get()
            print(syllable_structure)
            for syllable_letter_feature in syllable_structure:
                letters = self.inventory.get_letter(syllable_letter_feature)
                # TODO choose letters by weighted freq/uncommonness
                if letters:
                    word += random.choice(letters)
        print(word)
        return word