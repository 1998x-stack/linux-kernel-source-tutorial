#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#define TEST_BYTES 1024

int main(void)
{
    int fd, i;
    unsigned char written[TEST_BYTES];
    unsigned char readback[TEST_BYTES];

    for (i = 0; i < TEST_BYTES; i++)
        written[i] = (i * 37 + 11) & 0xff;

    fd = open("/dev/ram1", O_RDWR, 0);
    if (fd < 0) {
        printf("open /dev/ram1 failed\\n");
        return 1;
    }
    if (lseek(fd, 0L, 0) < 0 ||
        write(fd, written, TEST_BYTES) != TEST_BYTES ||
        lseek(fd, 0L, 0) < 0 ||
        read(fd, readback, TEST_BYTES) != TEST_BYTES) {
        printf("ramdisk I/O failed\\n");
        close(fd);
        return 2;
    }
    for (i = 0; i < TEST_BYTES; i++) {
        if (written[i] != readback[i]) {
            printf("mismatch at %d\\n", i);
            close(fd);
            return 3;
        }
    }
    close(fd);
    printf("ramdisk read/write PASS\\n");
    return 0;
}
