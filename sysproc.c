#include "types.h"
#include "x86.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"
#define null 0x00
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

