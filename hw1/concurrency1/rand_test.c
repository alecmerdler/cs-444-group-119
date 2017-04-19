/* simple test of the our_rand function */

#include <stdio.h>
#include "our_rand.h"

int main(void)
{
	printf("%d\n", our_rand(1, 1000));
	return 0;
}
