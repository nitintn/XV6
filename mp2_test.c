#include"types.h"
#include"user.h"

#define STACKSIZE 1024

extern int sys_write(void);
struct 
bufferstruct 
{
  int items;
  int arrayspaces;
  int bufferArray[10];
};
struct bufferstruct bufferstruct;

int mutex;

void 
prodRandSleep(void)
{
  sleep(5);
}

void 
consRandSleep(void)
{
  sleep(4);
}

void 
producer (void*arg)
{
  int i, j;  
  j = 0;
  
  //loopto create items i
  for(i = 0; i < 10; i++)
  {
	bufferstruct.arrayspaces = 10;
    
	mtx_lock(mutex);
	if(bufferstruct.arrayspaces == 0)
	{
		mtx_unlock(mutex);
		prodRandSleep();
    } 
	else 
	{
        if(bufferstruct.bufferArray[j] == 0)
		{
          //found = 1;
          printf(1,"producer produced item %d\n", i);
          
          bufferstruct.bufferArray[j] = i;
          bufferstruct.items ++;
          bufferstruct.arrayspaces --;
        }
        j++;
      mtx_unlock(mutex);
    }//end else	
  }
//printf(1,"j is: %d mutex: %d\n",j, mutex);
  exit();
}

void 
consumer (void*arg)
{
 
  int i,k;
  int count;
  count =0; 
  for(k=0; k < sizeof(bufferstruct.bufferArray); k++)
  {
	if(bufferstruct.bufferArray[k]!=0)
	{
		count =  count +1;
	}		
  }
  //loopto create items i    
  for(i = 0; i < 10; i++)
  {
    mtx_lock(mutex);
    if(bufferstruct.items == 0)
	{
      mtx_unlock(mutex);
      consRandSleep();
    } 
	else 
	{
      
        if(count>=0)
		{
          printf(1,"consumer consumed item %d\n", bufferstruct.bufferArray[count]);
          
          bufferstruct.bufferArray[count] = 0;
          bufferstruct.items --;
          bufferstruct.arrayspaces ++;
        }
        count--;
      mtx_unlock(mutex);
    }//end else
  }//end for
  exit();
}

int 
main(int argc, char**argv)
{
  mutex = mtx_create(0);
  uint* stack = malloc(STACKSIZE);

  //Creating one producer
  thread_create(*producer,stack,(void*)0);
  thread_join((void*)0);
  // Creating one consumer
  thread_create(*consumer,stack,(void*)0);
  thread_join((void*)1);
	
  exit();
  return 0;
}
