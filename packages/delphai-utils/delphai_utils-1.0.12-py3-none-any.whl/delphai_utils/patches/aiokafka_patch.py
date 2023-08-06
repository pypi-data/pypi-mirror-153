from aiokafka.consumer.group_coordinator import GroupCoordinator
import asyncio


async def ensure_active_group(self, subscription, prev_assignment):
    # due to a race condition between the initial metadata
    # fetch and the initial rebalance, we need to ensure that
    # the metadata is fresh before joining initially. This
    # ensures that we have matched the pattern against the
    # cluster's topics at least once before joining.
    # Also the rebalance can be issued by another node, that
    # discovered a new topic, which is still unknown to this
    # one.
    if self._subscription.subscribed_pattern:
        await self._client.force_metadata_update()
        if not subscription.active:
            return None

    if not self._performed_join_prepare:
        # NOTE: We pass the previously used assignment here.
        await self._on_join_prepare(prev_assignment)
        self._performed_join_prepare = True

    # NOTE: we did not stop heartbeat task before to keep the
    # member alive during the callback, as it can commit offsets.
    # See the ``RebalanceInProgressError`` case in heartbeat
    # handling.
    await self._stop_heartbeat_task()

    # We will not attempt rejoin if there is no activity on consumer
    idle_time = self._subscription.fetcher_idle_time
    if prev_assignment is not None and idle_time >= self._max_poll_interval:
        await asyncio.sleep(self._retry_backoff_ms / 1000)
        # This if condition always triggered and resulted in the agent not being able to
        # reconnect because it kept waiting and returned None
        # return None
    # We will only try to perform the rejoin once. If it fails,
    # we will spin this loop another time, checking for coordinator
    # and subscription changes.
    # NOTE: We do re-join in sync. The group rebalance will fail on
    # subscription change and coordinator failure by itself and
    # this way we don't need to worry about racing or cancellation
    # issues that could occur if re-join were to be a task.
    success = await self._do_rejoin_group(subscription)
    if success:
        self._performed_join_prepare = False
        self._start_heartbeat_task()
        return subscription.assignment
    return None


GroupCoordinator.ensure_active_group = ensure_active_group
