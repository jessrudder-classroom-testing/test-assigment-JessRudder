using System;
using System.Collections.Generic;

class Main {
	
	// model sound structure
	public class Inventory {
		string nasals = "";
		string plosivesVoiced = "";
		string plosivesVoiceless = "";
		string fricativesVoiced = "";
		string fricativesVoiceless = "";
		string approximants = "";
		string vowels = "";

		public Inventory () {
		}
		public void AddNasals (string nasals) {
			this.nasals = String.Format("{0}{1}", this.nasals, nasals);
		}
		public void AddPlosives (string plosives) {
			this.plosivesVoiced = String.Format("{0}{1}", this.plosivesVoiced, plosives);
		}
		public void AddPlosivesVoiceless (string plosives) {
			this.plosivesVoiceless = String.Format("{0}{1}", this.plosivesVoiceless, plosives);
		}
		public void AddFricativesVoiced (string fricatives) {
			this.fricativesVoiced = String.Format("{0}{1}", this.fricativesVoiced, fricatives);
		}
		public void AddFricativesVoiceless (string fricatives) {
			this.fricativesVoiceless = String.Format("{0}{1}", this.fricativesVoiceless, fricatives);
		}
		public void AddApproximants (string approximants) {
			this.approximants = String.Format("{0}{1}", this.approximants, approximants);
		}
		public void AddVowels (string vowels) {
			this.vowels = String.Format("{0}{1}", this.vowels, vowels);
		}
	}


	// model syllable structure as onset, nucleus, coda
	public class Syllable {
		List<string> nuclei = new List<string>();
		List<string> onsets = new List<string>();
		List<string> codas = new List<string>();

		public Syllable () {
		}
		public void AddOnset (string onsets) {
			this.onsets.Add(onset);
		}
		public void AddNucleus (string nucleus) {
			this.nuclei.Add(nucleus);
		}
		public void AddCoda (string coda) {
			this.codas.Add(coda);
		}
	}


	// build and store a syllable (modeled as process -ation rather than entity -ator)
	public class NameGeneration {
		Syllable syllable;
		Inventory inventory;
		Dictionary<string,string> affixes = new Dictionary<string,string>();
		// sound change kvs of structure 'feature, feature' -> 'feature, feature'
		Dictionary<string,string> soundChanges = new Dictionary<string,string>();

		public NameGeneration () {
			this.syllable = new Syllable();
			this.inventory = new Inventory();
		}
		public void BuildSyllable () {
			// recipe
			// ?- internal rules
			// - build by features
			// - roll for each part
			// - choose parts
			//
			// - attach syllables->word
			//
			// - word affixes
			// - word-internal changes
			// - word-edge changes
		}
	}

	public static void Main(string[] args) {

		Console.WriteLine ("test print");

	}
}