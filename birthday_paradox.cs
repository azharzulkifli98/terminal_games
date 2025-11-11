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
                    return found.Count;
                }
                else {
                    found.Add(pick);
                }
            }
        }

        public static int one_in_a_million(int max_range) {
            int pick;
            int tries = 0;
            int first = random.Next(max_range);

            for (;;) {
                pick = random.Next(max_range);
                tries++;

                if (pick == first) {
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
            Console.WriteLine("Test the probability of getting any repeating number vs getting a specific repeat number");

            int x = -1;
            while (x < 1 || x > 1000)
            {
                Console.Write("Enter a positive integer between 1 and 1000: ");

                string userInput = Console.ReadLine();

                if (int.TryParse(userInput, out x))
                {
                    if (x > 1000 || x < 1)
                    {
                        Console.WriteLine("Integer out of bounds, try again.");
                    }
                }
                else
                {
                    Console.WriteLine("Not an integer, try again.");   
                }
            }
            
            Console.WriteLine("Any repeat: {0}", birthday_paradox(x));
            Console.WriteLine("Specific repeat: {0}", one_in_a_million(x));
            Console.WriteLine("Specific value with no repeats: {0}", deck_of_cards(x, 1));
        }
    }
}