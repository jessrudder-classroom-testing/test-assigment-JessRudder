from .hierarchy import Hierarchy
from ..tools import redacc
import random

# NOTE: Phonotactics esp scale & dep build left-to-right. "Progressive" constraints are
# unideally handled either during syllable definition, e.g. in specific syllable types,
# or after syllable build, e.g. through sound changes

# TODO: optional/dependent sonority (see sonority scale list and associated methods below)
# - add_sonority_dependency()
# - e.g. CCV: if s -> {p,t,k,l,w}, then if st -> {r}
class Phonotactics:
    def __init__(self, phonology):
        # check that features exist
        self.phonology = phonology
        
        # feature scale and dependencies
        self.hierarchy = Hierarchy(phonology)
        self.scale = self.hierarchy.scale
        self.dependencies = self.hierarchy.dependencies
        self.recommend = self.hierarchy.recommend

       # configure syllable nucleus
        # TODO: consider defaulting to ['vowel'] if present
        self.nuclei = set()

        # first draw likelihoods
        # TODO: how likely each is to be chosen
        # OR just select from chains/sonority that are at onset/coda length?
        # self.lihelihoods = {
        #     'onset': {},
        #     'coda': {},
        #     'nucleus': {}
        # }

    # Syllable parts - nucleus
    def is_features_list(self, features):
        if not isinstance(features, (list, tuple)):
            return False
        elif False in [self.phonology.phonetics.has_feature(feature) for feature in features]:
            return False
        else:
            return True

    def add_nucleus(self, *features):
        # vet features
        vetted_features = self.phonology.syllables.structure(features)
        # build and check featuresets
        featuresets = []
        for feature in vetted_features:
            featureset = {feature} if isinstance(feature, str) else set(feature)
            if not self.is_features_list(featureset):
                raise ValueError(f"Phonotactics failed to add nucleus with invalid features - {features}")
            featuresets.append(featureset)
        # add featuresets to nuclei
        for featureset in featuresets:
            self.nuclei.add(featureset)
        return self.nuclei

    def get_nuclei(self):
        return self.nuclei

    def remove_nucleus(self, features):
        if features in self.nuclei:
            self.nuclei.remove(features)
            return True
        return False

    def clear_nuclei(self):
        self.nuclei.clear()
        return self.nuclei

    # Split and shape syllable parts phonotactically

    def is_features_list_overlap(self, featureslist_a, featureslist_b, all_a_in_b=True):
        """Compare two lists of featuresets to determine if they are same-length
        overlapping features collections."""
        if len(featureslist_a) != len(featureslist_b):
            return False
        for i in range(len(featureslist_a)):
            feature_overlap = set(featureslist_a[i]) & set(featureslist_b[i])
            if not feature_overlap or (all_a_in_b and len(feature_overlap) != len(featureslist_a)):
                return False
        return True

    def partition_syllable(self, syllable_features):
        """Split syllable liss into onset, nucleus, coda.
        Params:
            syllable_features (list): list of string lists, each string representing a feature
        """
        nucleus_indexes = []
        for i, features in enumerate(syllable_features):
            for nucleus in self.nuclei:
                if self.is_features_list_overlap(features[i:i+len(nucleus)], nucleus):
                    nucleus_indexes += [i, i+len(nucleus)]
                    break
        
        if not nucleus_indexes:
            raise ValueError(f"Phonotactics failed to partition syllable with unknown nucleus - {syllable_features} not in {self.nuclei}")

        syllable_parts = {
            'onset': syllable_features[:nucleus_indexes[0]],
            'coda': syllable_features[nucleus_indexes[0]:nucleus_indexes[1]],
            'nucleus': nucleus_indexes[1]
        }

        return syllable_parts

    # TODO: how to ensure gemination not just found down here in phonotactics?
    #   - also syllable interfaces, since san-nas yields gem
    #   - this brings up another q about restrictions along syllable bounds
    #
    # TODO: for each slot use hierarchy to choose a sound
    #   - no hierarchy -> open choice
    #   - each key is a single string feature or ipa, with ipa checked first
    #   - search for minimum same-length hierarchy element for codas, onsets
    #   - restrictions on the next slot are based on actual sounds chosen
    #
    #   - example: voiced, sibilant then next select sibilant > stop, voiced > voiced
    #   - example: voicing only on certain left-selects (like (voiced, stop) > voiced)
    #
    # TODO: allow doubles (like nmV or nnV)
    #   - beyond just adding say "nasal", "nasal" to sonority
    #
    # TODO: when building C sound slots from dependency chains
    #   - get all dependency chains that are at least as long as cluster
    #   - apply for onset, reverse for coda

    def shape(self, raw_syllable, gaps=True, doubles=True, triples=False):
        """Fill out a syllable with all defined phonotactics including dependencies
        and sonority. Features walk hierarchically down the sonority scale (with gaps)
        until a dependency chain inclusion/exclusion is found, then the dependency
        chain is followed until a sound with no dependency is found, at which point
        vetting switches back to the sonority scale.      
        """
        # vet syllable for valid features
        syllable_features = self.phonology.syllables.structure(raw_syllable)

        # break up and check syllables
        syllable_pieces = self.partition_syllable(syllable_features)
        if not syllable_pieces:
            raise ValueError(f"Phonotactics failed to shape syllable - unknown syllable {syllable_features}")

        # prepare to build syllable features shape from scale and dependencies
        syllable_shape = {piece: [] for piece in syllable_pieces}

        # shape base featureset for each onset sound
        for current_features in syllable_pieces['onset']:
            last_sound = syllable_shape['onset'][-1] if syllable_shape['onset'] else None
            syllable_shape['onset'] += [self.recommend(last_sound, current_features)]

        # shape nucleus
        syllable_shape['nucleus'] = list(random.choice(self.nuclei))

        # shape coda
        for current_features in syllable_pieces['coda']:
            last_sound = syllable_shape['coda'][0] if syllable_shape['coda'] else None
            syllable_shape['coda'] = [self.recommend(last_sound, current_features)] + syllable_shape['coda']

        # NOTE: syllable_shape has turned to a full fill-in of sound symbols
        return syllable_shape['onset'] + syllable_shape['nucleus'] + syllable_shape['coda']
