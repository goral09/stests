import random

import dramatiq

from stests.core import cache
from stests.core.utils import factory
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionStatus
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.core.utils.exceptions import IgnoreableAssertionError
from stests.workflows.orchestration.model import Workflow
from stests.workflows.orchestration.model import WorkflowStep
from stests.workflows.orchestration import predicates



# Queue to which messages will be dispatched.
_QUEUE = "workflows.orchestration"


@dramatiq.actor(queue_name=_QUEUE)
def do_step(ctx: ExecutionContext):
    """Runs a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Escape if unexecutable.
    if not _can_start(ctx):
        return

    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index + 1)    

    # Update ctx.
    ctx.step_index += 1
    ctx.step_label = step.label

    # Set info/state.
    step_info = factory.create_execution_info(ExecutionAspect.STEP, ctx)

    # Update cache.
    cache.orchestration.set_context(ctx)
    cache.orchestration.set_info(step_info)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> starts")

    # Execute.
    step.execute()

    # Process errors.
    if step.error:
        on_step_error.send(ctx, str(step.error))

    # Exception if step result != None | tuple.
    elif step.result is not None and not isinstance(step.result, tuple):
        raise TypeError("Expecting either None or a tuple from a step function.")

    # Process result for async ops.
    elif step.is_async:
        on_step_execute_async(ctx, step)

    # Process result for sync ops.
    else:
        on_step_execute_sync(ctx, step)


def on_step_execute_async(ctx: ExecutionContext, step: WorkflowStep):
    """Performs asynchronous step execution.
    
    :param ctx: Execution context information.
    :param step: Step related execution information.
    
    """
    # Enqueue message.
    if isinstance(step.result, tuple) and len(step.result) == 2:
        _enqueue_message(ctx, step)

    # Enqueue message batch.
    elif isinstance(step.result, tuple) and len(step.result) == 3:
        _enqueue_message_batch(ctx, step)
    
    else:
        raise TypeError("Async steps must return either a single message or a batch of messages")


def on_step_execute_sync(ctx: ExecutionContext, step: WorkflowStep):
    """Performs step execution.
    
    :param ctx: Execution context information.
    :param step: Step related execution information.
    
    """
    # If unit of work is complete then signal step end.
    if step.result is None:
        do_step_verification.send(ctx)

    # Enqueue message batch (with completion callback).
    elif isinstance(step.result, tuple) and len(step.result) == 3:
        _enqueue_message_batch(ctx, step)

    else:
        raise TypeError("Sync steps must return None or a batch of messages")


@dramatiq.actor(queue_name=_QUEUE)
def do_step_verification(ctx):
    """Verifies a workflow step prior to signalling end.
    
    :param ctx: Execution context information.
    
    """
    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)
    if step is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> invalid step")

    # Verify step.
    if not step.has_verifer:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> step verifier undefined")
    else:
        try:
            step.verify()
        except AssertionError as err:
            if (err.args and isinstance(err.args[0], IgnoreableAssertionError)):
                return
            logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> step verification failed")
            return

    # Step verification succeeded therefore signal step end.
    on_step_end.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_step_end(ctx: ExecutionContext):
    """Ends a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)

    # Update cache.
    cache.orchestration.set_info_update(ctx, ExecutionAspect.STEP, ExecutionStatus.COMPLETE)

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> end")

    # Enqueue either end of phase or next step. 
    if step.is_last:
        # JIT import to avoid circularity.
        from stests.workflows.orchestration.actors.phase import on_phase_end
        on_phase_end.send(ctx)
    else:
        do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_step_error(ctx: ExecutionContext, err: str):
    """Ends a workflow step in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # Update cache.
    cache.orchestration.set_info_update(ctx, ExecutionAspect.STEP, ExecutionStatus.ERROR)

    # Inform.
    logger.log_error(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {ctx.step_label} -> unhandled error: {err}")


@dramatiq.actor(queue_name=_QUEUE)
def on_step_deploy_finalized(ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):   
    """Processes a finalized deploy within the context of a step.
    
    :param ctx: Execution context information.
    :param node_id: Identifier of node that emitted block finalization event.
    :param block_hash: Hash of a finalized block.
    :param deploy_hash: Hash of a finalized deploy.

    """
    # Increment deploy counts.
    cache.orchestration.increment_deploy_counts(ctx)

    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)
    if step is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> invalid step")

    # Verify deploy.
    if not step.has_verifer_for_deploy:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> deploy verifier undefined")
        return       
    else:
        try:
            step.verify_deploy(node_id, block_hash, deploy_hash)
        except AssertionError as err:
            logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> deploy verification failed: {err} :: {deploy_hash}")
            return

    # Verify step.
    if not step.has_verifer:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> step verifier undefined")
    else:
        try:
            step.verify()
        except AssertionError as err:
            if (err.args and isinstance(err.args[0], IgnoreableAssertionError)):
                return
            logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} -> step verification failed")
            return

    # Step verification succeeded therefore signal step end.
    on_step_end.send(ctx)


def _can_start(ctx: ExecutionContext) -> bool:
    """Returns flag indicating whether a step increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a step increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = predicates.is_valid_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if current phase not found.
    phase = wflow.get_phase(ctx.phase_index)
    if phase is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> invalid phase index")
        return False
    
    # False if next step not found.
    step = phase.get_step(ctx.next_step_index)
    if step is None:
        logger.log_warning(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.next_step_index_label} -> invalid step index")
        return False

    # False if next step locked - can happen when processing groups of messages.
    if not predicates.was_lock_acquired(ExecutionAspect.STEP, ctx):
        return False
    
    # All tests passed, therefore return true.    
    return True


def _enqueue_message(ctx, step):
    """Enqueues a single message.
    
    """
    actor, args = step.result
    actor.send_with_options(args=args)


def _enqueue_message_batch(ctx, step):
    """Enqueues a message batch.
    
    """
    # Unpack step result.
    actor, count, args_factory = step.result

    # Set window of dispatch.
    dispatch_window = 0 if step.is_sync else ctx.get_dispatch_window_ms(count)

    # Yield args of messages to be enqueued.
    def message_factory():
        for args in args_factory():
            yield actor.message_with_options(
                args=args,
                delay=0 if step.is_sync else random.randint(0, dispatch_window)
                )

    # Instantiate a dramatiq group to batch message set.
    group = dramatiq.group(message_factory())

    # When in sync mode can signal end of step in a completion callback. 
    if step.is_sync:
        group.add_completion_callback(do_step_verification.message(ctx))

    # Enqueue message batch.
    group.run()

