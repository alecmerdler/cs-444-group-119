/*
 * LOOK I/O Scheduler
 * CS444 - Spring 2017 - Oregon State University
 * Group 11-09
 *
 * Resources:
 * - http://classes.engr.oregonstate.edu/eecs/fall2011/cs411/proj03.pdf
 * - http://www.makelinux.net/books/lkd2/ch13lev1sec5
 */
#include <linux/blkdev.h>
#include <linux/elevator.h>
#include <linux/bio.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>
#include <linux/list.h>
#include <linux/kernel.h>


struct sstf_data {
	struct list_head queue;
};

/*
 * Identical implementation as noop.
 */
static void sstf_merged_requests(struct request_queue *q, struct request *rq,
				 struct request *next)
{
	list_del_init(&next->queuelist);
}

/*
 * Mostly the same as noop, except for adding request to tail of queue instead of
 * sorting.
 */
static int sstf_dispatch(struct request_queue *q, int force)
{
	struct sstf_data *sd = q->elevator->elevator_data;

	if (!list_empty(&sd->queue)) {
		struct request *rq = list_entry(sd->queue.next, struct request, queuelist);

		printk(KERN_DEBUG "SSTF: dispatching sector: %llu\n",blk_rq_pos(rq));

		list_del_init(&rq->queuelist);

		elv_dispatch_add_tail(q, rq);
		return 1;
	}
	return 0;
}

/*
 * Add a request to the queue using insertion sort.
 */
static void sstf_add_request(struct request_queue *q, struct request *rq)
{
	struct sstf_data *sd = q->elevator->elevator_data;
	struct list_head *curr_pos;
	struct list_head *tmp;
	struct request *curr_node;

	if (list_empty(&sd->queue)) {
		printk(KERN_DEBUG "SSTF: queue list empty adding item to queue. \n");

		// If queue is empty, simply add request to the queue
		list_add(&rq->queuelist, &sd->queue);
	} else {
	    // Use macro to iterate over queue list
		list_for_each_safe(curr_pos, tmp, &sd->queue) {
			curr_node = list_entry(curr_pos, struct request, queuelist);

            // Check if the new request has a higher position
			if (blk_rq_pos(curr_node) < blk_rq_pos(rq)) {
				printk(KERN_DEBUG "SSTF: add_request: inserting  item via insert sort. \n");

                // Add the new request and stop iteration
				list_add(&rq->queuelist, &curr_node->queuelist);
				break;
			}
		}
	}
}

/*
 * Identical implementation as noop.
 */
static struct request *
sstf_former_request(struct request_queue *q, struct request *rq)
{
	struct sstf_data *sd = q->elevator->elevator_data;

	if (rq->queuelist.prev == &sd->queue)
		return NULL;

	return list_entry(rq->queuelist.prev, struct request, queuelist);
}

/*
 * Identical implementation as noop.
 */
static struct request *
sstf_latter_request(struct request_queue *q, struct request *rq)
{
	struct sstf_data *sd = q->elevator->elevator_data;

	if (rq->queuelist.next == &sd->queue)
		return NULL;
	return list_entry(rq->queuelist.next, struct request, queuelist);
}

/*
 * Identical implementation as noop.
 */
static int sstf_init_queue(struct request_queue *q, struct elevator_type *e)
{
	struct sstf_data *sd;
	struct elevator_queue *eq;

	eq = elevator_alloc(q, e);
	if (!eq)
		return -ENOMEM;

	sd = kmalloc_node(sizeof(*sd), GFP_KERNEL, q->node);
	if (!sd) {
		kobject_put(&eq->kobj);
		return -ENOMEM;
	}
	eq->elevator_data = sd;

	INIT_LIST_HEAD(&sd->queue);

	spin_lock_irq(q->queue_lock);
	q->elevator = eq;
	spin_unlock_irq(q->queue_lock);

	printk(KERN_DEBUG "SSTF: INIT queue\n");
	return 0;
}

/*
 * Identical implementation as noop.
 */
static void sstf_exit_queue(struct elevator_queue *e)
{
	struct sstf_data *sd = e->elevator_data;

	BUG_ON(!list_empty(&sd->queue));
	kfree(sd);
}

/*
 * Identical implementation as noop.
 */
static struct elevator_type elevator_sstf = {
	.ops = {
		.elevator_merge_req_fn		= sstf_merged_requests,
		.elevator_dispatch_fn		= sstf_dispatch,
		.elevator_add_req_fn		= sstf_add_request,
		.elevator_former_req_fn		= sstf_former_request,
		.elevator_latter_req_fn		= sstf_latter_request,
		.elevator_init_fn		= sstf_init_queue,
		.elevator_exit_fn		= sstf_exit_queue,
	},
	.elevator_name = "sstf",
	.elevator_owner = THIS_MODULE,
};

/*
 * Identical implementation as noop.
 */
static int __init sstf_init(void)
{
	return elv_register(&elevator_sstf);
}

/*
 * Identical implementation as noop.
 */
static void __exit sstf_exit(void)
{
	elv_unregister(&elevator_sstf);
}

module_init(sstf_init);
module_exit(sstf_exit);

MODULE_AUTHOR("Group 11-09");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("SSTF IO scheduler");
