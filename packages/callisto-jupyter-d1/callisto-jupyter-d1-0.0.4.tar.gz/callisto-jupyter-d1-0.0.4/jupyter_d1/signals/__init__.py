# Standard names for Blinker signals shared between modules

# Signals that are fired when new data comes in on respective channels.
# The signal will be emitted with these kwargs:
#    * msg - contents of the message
#    * kernel_id - uuid of the kernel emitting the message
#    * channel - name of the channel, eg iopub, shell, etc
IOPUB_CHANNEL = "iopub_channel"
SHELL_CHANNEL = "shell_channel"
STDIN_CHANNEL = "stdin_channel"
HB_CHANNEL = "hb_channel"
CONTROL_CHANNEL = "control_channel"

# Signal fired when a cell in a document changes
# The signal will be emitted with these kwargs:
#    * cell - The nbformat.notebooknode.NotebookNode object that is the cell
#    * notebook_id - The uuid of the notebook that the cell belongs to
CELL_UPDATE = "cell_update"
CELL_ADDED = "cell_added"
CELL_DELETED = "cell_deleted"

# Signal fired when a cell produces stream output
# The signal will be emitted with these kwargs:
#    * output - The nbformat-style cell output
#    * notebook_id - The uuid of the notebook that the cell belongs to
#    * cell_id - The uuid of the cell
CELL_STREAM = "cell_stream"

# Signal fired when a cell execution_count gets updated
# The signal will be emitted with these kwargs:
#    * execution_count - the int execution count for the cell
#    * notebook_id - The uuid of the notebook that the cell belongs to
#    * cell_id - The uuid of the cell
#    * parent_id - The message_id of the original execution request
CELL_EXECUTION_REPLY = "cell_execution_reply"

# Signal fired when the kernel starts to execute a piece of code
# The signal will be emitted with these kwargs:
#    * content - the content dictionary from the original message including
#       * code - the code being executed
#       * execution_count - the int execution count for the cell
#    * notebook_id - The uuid of the notebook that the cell belongs to
#    * parent_id - The message_id of the original execution request
CELL_EXECUTION_INPUT = "cell_execution_input"

# Signal fired when the kernel starts to execute a piece of code
# The signal will be emitted with these kwargs:
#    * notebook_id - The uuid of the notebook that the cell belongs to
#    * cell_id - The uuid of the cell
#    * message_id - The message_id of the  execution request
CELL_EXECUTION_REQUEST = "cell_execution_request"

# Signal fired when a scratch command updates. This may happen multiple times
# for a single scratch command with different outputs.
# The signal will be emitted with these kwargs:
#    * msg_id - The msg_id of the scratch command execution
#    * notebook_id - The uuid of the notebook that the scratch command was
#                    run in
#    * output - Output of the scratch command
#    * execution_state - The state of the scratch command
SCRATCH_UPDATE = "scratch_update"

# Signal fired when a kernels vars are updated
# The signal will be emitted with these kwargs:
#    * notebook_id - The uuid of the notebook
#    * vars - List of KernelVariable objects
VARS_UPDATE = "vars_update"

# Signal fired when a details response for a variable comes back
# The signal will be emitted with these kwargs:
#    * notebook_id - The uuid of the notebook
#    * single_var - Optional KernelVariable object
VAR_DETAILS = "var_details"

# Signal fired when the kernel emits a page payload (like help command
# output).
# The signal will be emitted with these kwargs:
#    * msg_id - The msg_id of the command that prompted this payload
#    * notebook_id - The uuid of the notebook that the command was
#                    run in
#    * data - The mimebundle of data, includes at least text/plain
#    * start - Line offset to start from
PAYLOAD_PAGE = "payload_page"

# Signal fired when code complete results come back
# The signal will be emitted with these kwargs:
#    * msg_id - The msg_id of the completion request
#    * notebook_id - The uuid of the notebook
#    * matches - List of possible completions
#    * cursor_start - Start of text that would be replaced
#    * cursor_end - End of text that would be replaced
COMPLETE_REPLY = "complete_reply"

HISTORY_REPLY = "history_reply"
METADATA_UPDATE = "metadata_update"
KERNEL_RESTARTED = "kernel_restarted"
KERNEL_INTERRUPTED = "kernel_interrupted"

# Signals fired when notebook is added to or removed from notebook manager
# The signal will be emitted with these kwargs:
#    * notebooks - The dict of notebook uuid to notebook nodes from the
#                  notebook manager
NOTEBOOKS_UPDATED = "notebook_updated"

# FastAPI lifecycle events
APP_STARTUP = "app_startup"
APP_SHUTDOWN = "app_shutdown"

RCLONE_UPDATE = "rclone_update"
WATCHDOG_FILE_SYSTEM_EVENT = "watchdog_event"
SERVER_STATS_UPDATE = "server_stats_update"
APP_LOG = "app_log"
