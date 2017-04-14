#include <pthread.h>
#include <stdio.h>

#define ITEM_BUFFER_SIZE 32


struct item {
    int value;
    int wait_time;
};


void *producer_function(void *ptr)
{
    struct item *buffer = (struct item *) ptr;
}


void *consumer_function(void *ptr)
{
    struct item *buffer = (struct item *) ptr;
}


int main()
{
    struct item buffer[ITEM_BUFFER_SIZE];
    pthread_t producer;
    pthread_t consumer;

    if (pthread_create(&producer, NULL, producer_function, &buffer))
    {
        printf("Error creating producer thread");
        return 1;
    }

    if (pthread_create(&consumer, NULL, consumer_function, &buffer))
    {
        printf("Error creating consumer thread");
        return 1;
    }

    pthread_join(producer, NULL);
    pthread_join(consumer, NULL);

    return 0;
}
