#include "types.h"

#include "user.h"

#include "syscall.h"



#define NUM_ELEMENTS 100

int mutex;

//unsigned short



void pro(void *arg){

    int *buffer=(int*)arg;

    int p;

    for(p=0;p<NUM_ELEMENTS;p++){

        mtx_lock(mutex);

        buffer[p]=p*5;

        printf(1,"Producer put %d\n",buffer[p]);

        mtx_unlock(mutex);

        if(p==(NUM_ELEMENTS/2)){

            sleep(100);

        }

    }

    exit();

}

void con(void *arg){

    int *buffer=(int*)arg;

    int c;

    mtx_lock(mutex);

    printf(1,"Consumer has:[");

    for(c=0;c<NUM_ELEMENTS;c++){

        if(buffer[c]!=-1){

            printf(1,"%d,",buffer[c]);

            buffer[c]=-1;

        }

    }

    printf(1,"]\n");

    mtx_unlock(mutex);

    exit();

}

int main(int argc,char *argv[]){

    mutex=mtx_create(0);

    void(*consumerPtr)(void *)=&con;

    void(*producerPtr)(void *)=&pro;

    int *main_buffer=(int*)malloc(NUM_ELEMENTS*sizeof(int));

    memset(main_buffer,-1,NUM_ELEMENTS*sizeof(int*));

    uint *stack=(uint *)malloc(1024);

    void *return_stack;

    thread_create(producerPtr,(void *)stack,(void *)main_buffer);

    thread_join((void**)&return_stack);

    thread_create(consumerPtr,(void *)stack,(void *)main_buffer);

    thread_join((void**)&return_stack);

    free(return_stack);

    exit();

    

}