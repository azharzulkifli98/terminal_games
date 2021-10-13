/*
goal is to test probability of getting repeat values
versus probability of getting exact values in random sampling
*/

using System;
using System.Collections.Generic;
using System.Linq;


namespace Birthday
{
    public class Tester
    {
        private static Random random = new Random();

        public static int birthday_paradox(int max_range) {
            int pick;
            List<int> found = new List<int>();

            for (;;) {
                pick = random.Next(max_range);
                if (found.Contains(pick)) {
                    string total = string.Join(" ", found);
                    Console.WriteLine(total);
                    return found.Count;
                }
                else {
                    found.Add(pick);
                }
            }
        }


        public static int one_in_a_million(int max_range, int chosen) {
            int pick;
            int tries = 0;

            for (;;) {
                pick = random.Next(max_range);
                tries++;

                if (pick == chosen) {
                    return tries;
                }
            }
        }


        public static int deck_of_cards(int max_range, int chosen) {
            int pick;
            int index;
            int tries = 0;
            List<int> unused = new List<int>();
            for (int i = 0; i < max_range + 1; i++) {
                unused.Add(i);
            }

            for (;;) {
                index = random.Next(unused.Count - 1);
                pick = unused[index];
                tries++;

                if (pick == chosen) {
                    return tries;
                }
                else {
                    unused.RemoveAt(index);
                }
            }
        }


        public static void Main(string[] args) {
            Console.WriteLine("prob of repeat vs prob of deck of cards vs prob of blind guesses");
            
            Console.WriteLine(birthday_paradox(365));
            Console.WriteLine(one_in_a_million(365, 100));
            Console.WriteLine(deck_of_cards(365, 100));
        }
    }
}