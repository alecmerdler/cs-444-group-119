#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "our_rand.h"


#define ITEM_BUFFER_SIZE 32


struct item {
    int value;
    int wait_time;
};

struct item buffer[ITEM_BUFFER_SIZE];
volatile int b_index = 0;
pthread_mutex_t lock;

void *producer_function(void *ptr)
{
	int wait = our_rand(3, 7);
	int done = 0;
	sleep(wait);
	struct item tmp;
	tmp.value = our_rand(0, 100);
	tmp.wait_time = our_rand(2, 9);
	while(!done) {
		/* block on trying to access the buffer */
		pthread_mutex_lock(&lock);
		/* If buffer full, release lock and try again */
		if(b_index >= ITEM_BUFFER_SIZE) {
			pthread_mutex_unlock(&lock);
			continue;
		}
		buffer[b_index] = tmp;
		b_index++;
		pthread_mutex_unlock(&lock);
		done = 1;
		printf("Produced %d\n", tmp.value);
	}


}


void *consumer_function(void *ptr)
{
	int done = 0;
	struct item tmp;
	while(!done) {
		/* block on trying to access the buffer */
		pthread_mutex_lock(&lock);
		/* If buffer full, release lock and try again */
		if(b_index == 0) {
			pthread_mutex_unlock(&lock);
			continue;
		}
		b_index--;
		done = 1;
		sleep(buffer[b_index].wait_time);
		printf("Consumed %d\n", buffer[b_index].value);
		pthread_mutex_unlock(&lock);
	}
}


int main(int argc, char **argv)
{

	if (argc < 1) {
		printf("Usage: %s [number of threads]\n" , argv[0]);
		return 1;
	}
	int num_threads = atoi(argv[1]);
	int i;

	printf("Number of threads: %d\n", num_threads);

	pthread_t threads[num_threads * 2];

	for (i = 0; i < num_threads; i++) {
		if(pthread_create(&threads[i], NULL, producer_function, NULL)) {
			printf("Error creating producer thread");
			return 1;
		}
	}

	for (i = num_threads; i < (num_threads * 2); i++) {
		if(pthread_create(&threads[i], NULL, consumer_function, &buffer)){
			printf("Error creating consumer thread");
			return 1;
		}
	}

	for (i = 0; i < (num_threads * 2); i++) {
		pthread_join(threads[i], NULL);
	}

	return 0;
}
