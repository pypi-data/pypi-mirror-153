import time
from datetime import datetime
from typing import Optional, Union

from qm.QmJob import QmJob
from qm._errors import JobCancelledError
from qm.pb.frontend_pb2 import GetJobExecutionStatusRequest
from qm.pb.inc_qua_pb2 import QuaProgram
from qm.pb.job_manager_pb2_grpc import JobManagerServiceStub
from qm.utils import insert_input_stream_to_job


class QmPendingJob(object):
    """
    A Class describing a job in the execution queue
    """

    def __init__(
        self,
        job_id,
        machine: "qm.QuantumMachine.QuantumMachine",
        qmm: "qm.QuantumMachinesManager.QuantumMachinesManager",
    ):

        self._id = job_id
        self._machine = machine
        self._qmm = qmm
        self._added_user_id = None
        self._time_added = None
        self._set_metadata()
        self._job_manager_client = JobManagerServiceStub(self._qmm._channel)

    def _set_metadata(self):
        response = self._get_execution_status()
        if response.status.HasField("pending"):
            self._added_user_id = response.status.pending.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.pending.timeAdded.seconds
            )
        elif response.status.HasField("running"):
            self._added_user_id = response.status.running.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.running.timeAdded.seconds
            )
        elif response.status.HasField("completed"):
            self._added_user_id = response.status.completed.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.completed.timeAdded.seconds
            )
        elif response.status.HasField("loading"):
            self._added_user_id = response.status.loading.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.loading.timeAdded.seconds
            )

    def id(self) -> str:
        """
        :return: The id of the job

        """
        return self._id

    @property
    def user_added(self):
        return self._added_user_id

    @property
    def time_added(self) -> datetime:
        return self._time_added

    def position_in_queue(self) -> Optional[int]:
        """
        Returns the current position of the job in the queue

        :return: The position in the queue

        Example:

            >>> pending_job.position_in_queue()

        """
        response = self._get_execution_status()
        if response.status.HasField("pending"):
            return response.status.pending.positionInQueue
        return None  # Job left queue

    def _get_execution_status(self):
        request = GetJobExecutionStatusRequest()
        request.quantumMachineId = self._machine.id
        request.jobId = self._id
        response = self._qmm._frontend.GetJobExecutionStatus(request)
        return response

    def wait_for_execution(self, timeout: Optional[float] = None) -> QmJob:
        """
        Waits for the job to be executed (start running) or until the timeout has elapsed

        :param timeout: Timeout (in seconds) for this operation

        :return: The running ``QmJob``

        """
        start = time.time()
        end = start + max(0.0, timeout) if timeout is not None else None

        while end is None or time.time() < end:
            response = self._get_execution_status()
            if response.status.HasField("pending") or response.status.HasField(
                "loading"
            ):
                time.sleep(0.02)
            elif response.status.HasField("running") or response.status.HasField(
                "completed"
            ):
                return QmJob(self._qmm, self._id, None)
            else:
                raise JobCancelledError(f"job {self._id} was cancelled")
        raise TimeoutError(
            f"job {self._id} was not started in time. Check the QMApp "
            f"for errors and try reloading the version. "
            f"Please also inform QM about this issue. "
        )

    def cancel(self) -> bool:
        """
        Removes the job from the queue

        :return: true if the operation was successful

        Example:

            >>> pending_job.cancel()

        """
        return self._machine.queue.remove_by_id(self._id) > 0

    def insert_input_stream(
        self,
        input_stream: Union[
            QuaProgram.ArrayVarRefExpression, QuaProgram.AnyScalarExpression
        ],
        data,
    ):
        """
        Insert data to the input stream declared in the QUA program.
        The data is then ready to be read by the program using the advance
        input stream QUA statement.

        Multiple data entries can be inserted before the data is read by the program.

        See `Input streams <https://qm-docs.qualang.io/guides/features#input-streams>`__ for more information.

        :param input_stream: The input stream the data is to be inserted to.
        :param data: The data to be inserted. The data's size must match the size of the input stream.
        """
        insert_input_stream_to_job(self, data, input_stream)
