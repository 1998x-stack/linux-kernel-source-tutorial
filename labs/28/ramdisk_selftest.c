#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#define TEST_BYTES 1024
#define RAMDISK_BYTES (512 * 1024) /* RAMDISK=512 in 1 KiB blocks */

static int check_region(int fd, long offset,
                        unsigned char *written,
                        unsigned char *readback)
{
    int i;

    if (lseek(fd, offset, 0) < 0 ||
        write(fd, written, TEST_BYTES) != TEST_BYTES ||
        lseek(fd, offset, 0) < 0 ||
        read(fd, readback, TEST_BYTES) != TEST_BYTES)
        return -1;

    for (i = 0; i < TEST_BYTES; i++)
        if (written[i] != readback[i])
            return -1;
    return 0;
}

int main(void)
{
    int fd, i;
    unsigned char written[TEST_BYTES];
    unsigned char readback[TEST_BYTES];

    for (i = 0; i < TEST_BYTES; i++)
        written[i] = (i * 37 + 11) & 0xff;

    fd = open("/dev/ram1", O_RDWR, 0);
    if (fd < 0) {
        printf("open /dev/ram1 failed\n");
        return 1;
    }

    if (check_region(fd, 0L, written, readback) < 0) {
        printf("first-block read/write failed\n");
        close(fd);
        return 2;
    }

    if (check_region(fd, (long)(RAMDISK_BYTES - TEST_BYTES),
                     written, readback) < 0) {
        printf("last-valid-block read/write failed\n");
        close(fd);
        return 3;
    }

    if (lseek(fd, (long)RAMDISK_BYTES, 0) < 0) {
        printf("seek to first out-of-range block failed\n");
        close(fd);
        return 4;
    }
    if (write(fd, written, TEST_BYTES) >= 0) {
        printf("out-of-range write unexpectedly succeeded\n");
        close(fd);
        return 5;
    }

    close(fd);
    printf("ramdisk read/write and boundary PASS\n");
    return 0;
}
