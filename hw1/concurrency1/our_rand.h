/* generates a random number between min and max, inclusive
 * uses rdrand if available, Mersenne Twister (mt19937) if not
 */
int our_rand(int min, int max);
