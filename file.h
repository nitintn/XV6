struct file {
  enum { FD_NONE, FD_PIPE, FD_INODE } type;
  int ref; // reference count
  char readable;
  char writable;
  struct pipe *pipe;
  struct inode *ip;
  uint off;
};
#define BSIZE 512  // block size
#define NDIRECT 10
#define INDIRECT_SINGLE 2
#define INDIRECT_DOUBLE 1

#define NINDIRECT (BSIZE / sizeof(uint))	//No. of pointers
 
#define MAXFILE (NDIRECT + INDIRECT_SINGLE*NINDIRECT + (INDIRECT_DOUBLE*NINDIRECT*NINDIRECT))

// in-memory copy of an inode
struct inode {
  uint dev;           // Device number
  uint inum;          // Inode number
  int ref;            // Reference count
  int flags;          // I_BUSY, I_VALID

  short type;         // copy of disk inode
  short major;
  short minor;
  short nlink;
  uint size;
  //uint addrs[NDIRECT+1];
  uint addrs[NDIRECT+INDIRECT_SINGLE+INDIRECT_DOUBLE];
};
#define I_BUSY 0x1
#define I_VALID 0x2

// table mapping major device number to
// device functions
struct devsw {
  int (*read)(struct inode*, char*, int);
  int (*write)(struct inode*, char*, int);
};

extern struct devsw devsw[];

#define CONSOLE 1
