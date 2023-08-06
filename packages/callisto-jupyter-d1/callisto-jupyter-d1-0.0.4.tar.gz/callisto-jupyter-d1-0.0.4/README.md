# jupyter_d1

Jupiter Discovery One server

## Info

### Install

`pip install git+https://github.com/OakCityLabs/jupyter_d1.git@branch_name#egg=jupyter_d1`

Once installed, install kernel definitions with
`jupyter_d1_install_kernels`

### Start Server

`start_jupyter_d1 --port=8000 --secret_token=user_provided_secret --root_dir=/path/to/working/directory`

### Run tests
(Requires pytest, async-asgi-testclient)
`jupyter_d1_test`

### How Stuff Works

The Jupyter D1 server sits between a REST client and a Jupyter Kernel.
Kernels don't understand notebooks.  They just execute commands they receive.
Jupyter D1 manages the state of the notebook, keeping track of which cell is being
 executed and updating the cells results with the kernel finishes processing.

In the traditional JavaScript Jupyter client, all of this state is held in the web app.
This makes it impossible to share that state with another client.  
In Jupyter D1, this state is held in the D1 server and a client can connect at any time
and ask for the current state.  
A client may also ask that new code is executed.  The D1 server relays that to the active kernel.
Kernel results are used to update the current model of the notebook in the D1 server and broadcast
to clients to update UIs.

Clients should connect to the notebook websocket stream where they will receive a broadcast of all
the updates to the notebook cells.  Clients can send regular REST requests to initiate action, like
executing a cell or changing a cell's source code.  A websocket is also avaible for the raw stream
of kernel messages, but that's not intended for client consumption in the long term.  Kernel messages
are more of a debugging tool.

### See Makefile for convenience commands

    make save_env    save current development environment using conda to environment.yml
    make load_env    create a development environment using conda from environment.yml (deletes current env definition)
    make show_env    list available conda environments
    make lint        run the linter
    make test        run pytest
    make ci_test     run the linter and then run pytest    
    make run_debug   run the 'uvicorn' server in debug mode
    make docs        open the docs in your browser (mac only, requires server running locally)
    make redoc       open the alternate docs in your browser (mac only, requires server running locally)

### Documentation

* Run the server with `make run_debug`
* Open the Swagger UI docs URL with `make docs` [link](http://localhost:8000/docs)
* Open the ReDoc docs URL with `make docs` [link](http://localhost:8000/redoc)

### Stream listeners

Run `./ws_listener.py` to echo out messages from the websocket broadcast channels.  Two options are:

* `./ws_listener.py --feed stream` -- Listen to the stream of kernel messages direct from the Jupyter kernel
* `./ws_listener.py --feed notebook` -- List to the jupyter_d1 stream of updates to notebook cells

### Paw

See the included Paw file `jupyter_d1.paw` for some examples.  A simple test sequence that might represent
what a client would do:

* Open the simple notebook
* Execute a cell by ID -- set x
* Execute a cell by ID -- increment x

This loads a notebook, executes a cell which assigns a value to `x` and then executes another cell that
increments the value of `x`.  It's useful to have the stream listeners active to see the results.

### Testing

* `make test` will pytest and report coverage
* Just running `pytest` from the top level directory will run all the tests
* Can specify a specific test with `pytest tests/test_notebooks_websocket.py::TestNotebookWebSocket::test_notebook`
* VS Code should understand the tests and run them from the editor, but sometimes that seems flakey.
* If VS Code has trouble finding tests, run `pytest --collect-only` at the cli to check for errors.

### WebDAV server

* The FastAPI app instantiates a [WebDAV server](https://wsgidav.readthedocs.io/en/latest/index.html) mounted under `/dav`.
* Currently, this exposes `/tmp` on the local machine.
* Can be mounted via a WebDAV [client](https://en.wikipedia.org/wiki/WebDAV).
* Eventually, this will provide clients file level access to the Jupyter working directory.
* Current username is `user` with password `password`.
* There is a read-only user called `readonly_user` but permission levels aren't implemented, so this user has full access.

### Static typing

* Jupyter_D1 uses static typing for compatibility with FastAPI
* The python runtime ignores type information at the moment.
* In VS Code, you should enable the `mypy` linter to check typing.
* [Mypy Cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

### Authenication with shared secret

* Use the shared secret from the server command line to get an access token
   * curl -H "Authorization: <SHARED_SECRET>" http://127.0.0.1:<port_number>/login/access-token
   * returns {"token":{"access_token":"**ACCESS_TOKEN**","token_type":"bearer"}}
* Use the returned access token for subsequent requests
   * curl -H "Authorization: Bearer <**ACCESS_TOKEN**>" http://127.0.0.1:<port_number>/notebooks

   
