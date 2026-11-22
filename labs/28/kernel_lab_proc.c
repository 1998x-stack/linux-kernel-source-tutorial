#include <linux/init.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/sched.h>

static struct proc_dir_entry *entry;

static int lab_show(struct seq_file *m, void *v)
{
    seq_printf(m, "name: kernel-field-guide\\n");
    seq_printf(m, "pid: %d\\n", current->pid);
    seq_printf(m, "comm: %s\\n", current->comm);
    return 0;
}

static int lab_open(struct inode *inode, struct file *file)
{
    return single_open(file, lab_show, NULL);
}

static const struct proc_ops lab_ops = {
    .proc_open = lab_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

static int __init lab_init(void)
{
    entry = proc_create("kernel_lab", 0444, NULL, &lab_ops);
    if (!entry)
        return -ENOMEM;
    pr_info("kernel_lab: /proc/kernel_lab created\\n");
    return 0;
}

static void __exit lab_exit(void)
{
    proc_remove(entry);
    pr_info("kernel_lab: removed\\n");
}

module_init(lab_init);
module_exit(lab_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Read-only procfs example for the modern-kernel track");
