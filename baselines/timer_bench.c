#include <stdio.h>

#if defined(__i386__)
    static __inline__ unsigned long long rdtsc(void)
    {
        unsigned long long int x;,
        __asm__ volatile (".byte 0x0f, 0x31" : "=A" (x));
        return x;
    }

#elif defined(__x86_64__)
    static __inline__ unsigned long long rdtsc(void)
    {
        unsigned hi, lo;
        __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
        return ( (unsigned long long)lo)|( ((unsigned long long)hi)<<32 );
    }
#endif

int main(void)
{
    unsigned long long start = 0;
    unsigned long long end = 0;

    FILE *fp; 
    fp = fopen("overhead.txt", "w");
    if (fp == NULL) {return 1;}
    int count = 0;
    for(int i = 0; i < 100000000; i++)
    {
        start = rdtsc();
        end = rdtsc();
        
        if(count % 100000 == 0)
        {
            printf("%d\n", count);
            fflush(stdout);
        }
        count++;
        fprintf(fp, "%llu\n", end - start);
        fflush(fp);
    }

    return 0;
}