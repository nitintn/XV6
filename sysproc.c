#include "types.h"
#include "x86.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"
#define null 0x00
#define INVALID_ARGS -1


int
sys_fork(void)
{
  return fork();
}

int
sys_exit(void)
{
  exit();
  return 0;  // not reached
}

int
sys_wait(void)
{
  return wait();
}

int
sys_kill(void)
{
  int pid;

  if(argint(0, &pid) < 0)
    return -1;
  return kill(pid);
}

int
sys_getpid(void)
{
  return proc->pid;
}

int
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;
  addr = proc->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

int
sys_sleep(void)
{
  int n;
  uint ticks0;
  
  if(argint(0, &n) < 0)
    return -1;
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(proc->killed){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

// return how many clock tick interrupts have occurred
// since start.
int
sys_uptime(void)
{
  uint xticks;
  
  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}
/*The fucntions sys_start_burst and sys_end_burst 
	are called after and before the syscall to get 
	the CPU Ticks*/
int
sys_start_burst(void)
{
  int start = sys_uptime();
  return start;
}

int
sys_end_burst(void)
{
  int end = sys_uptime();
  return end;

}

/* It keeps the track of the proceses
	running in the CPU*/
int
sys_print_bursts(void)
{
  int i;
  for( i=0; i<75;i++){
	  if(proc->cpu_bursts[i]!=null){					
		  cprintf ("%d,", proc->cpu_bursts[i]);					// printing the CPU bursts
		}
  }	
	  cprintf ("Turnaround Time:%d", sys_end_burst() - proc->ticktocktick); // calculating turnaround time
	  cprintf("\n");
	  return 0;
}

//machine problem 2- kernel threading

/*
	check whether valid thread arguments are passed
*/

// thread syscall 
int sys_thread_create(void)
{
	char *tmain, *stack, *arg;
	
	if (argptr(0,&tmain,1) < 0 || argptr(1, &stack,0) < 0 || argptr(2,&arg,0) < 0)
		return INVALID_ARGS;
	return thread_create((void*)tmain,(void*)stack, (void*)arg);

}

int sys_thread_join(void)
{
	char* stack;
	
	if(argptr(0,&stack,1) < 0)
		return INVALID_ARGS;
	return thread_join((void**)stack);
}

//mutex syscall
int sys_mtx_create(void)
{
	int locked;
	
	if(argint(0,&locked) < 0)
		return INVALID_ARGS;
	return mtx_create(locked);
}

int sys_mtx_lock(void)
{
	int lock_id;
	
	if(argint(0,&lock_id) < 0)
		return INVALID_ARGS;
	return mtx_lock(lock_id);
}

int sys_mtx_unlock(void)
{
	int lock_id;
	
	if(argint(0,&lock_id) < 0)
		return INVALID_ARGS;
	return mtx_unlock(lock_id);
}
