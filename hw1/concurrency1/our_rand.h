/* CS444 Project 1: Concurrency 1
 * Group 11-09
 * Members: Leon Leighton, Alec Merdler, Arthur Shing
 */


/* generates a random number between min and max, inclusive
 * uses rdrand if available, Mersenne Twister (mt19937) if not
 */
int our_rand(int min, int max);
