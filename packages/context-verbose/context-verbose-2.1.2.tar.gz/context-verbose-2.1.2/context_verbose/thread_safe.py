#!/usr/bin/env python3

"""
** Avoid display conflicts between threads. **
----------------------------------------------

This allows to replace the 'print' method native to python. All formatting must be done before.
"""

import threading

from context_verbose.memory import get_id
from context_verbose.tree import Tree, get_terminal_size, cut


EXPERIMENTAL = False


def print_safe(text, *, end='\n'):
    """
    ** Replacement of 'print'. **

    Constrained to display in a particular area to avoid mixing between threads.

    Parameters
    ----------
    text : str
        The string to display
    end : str, optional
        Transfer directly to the native ``print`` function.
    """
    assert isinstance(text, str)

    if EXPERIMENTAL:
        Pipe().add_message(text+end)

    else:
        columns, _ = get_terminal_size()
        if len(text) <= columns or columns <= 5:
            print(text, end=end)
        else:
            print('\n'.join(cut(text, columns)), end=end)


def _reset_memory():
    """
    ** Removes all traces of memory. **
    """
    for name in list(globals()).copy():
        if name.startswith('_pipe_'):
            del globals()[name]


class Pipe(threading.Thread):
    """
    ** Allows you to communicate with other execution threads. **

    * If this object is instantiated from the main thread of the main process:
        * It just keeps the display tree up to date and prints the new changes.
    * If it is instantiated in a thread of the main process:
        * It transmits messages to the main process.
        * He responds to callers who ask him if he is alive.
    * If it is instantiated in the main thread of a secondary process:
        * Failed : not implemented
    * If it is instantiated in a secondary thread of a secondary process:
        * Failed : not implemented
    """

    def __new__(cls):
        """
        ** Guarantees the uniqueness of an instance of this class. **

        Examples
        --------
        >>> import threading
        >>> from context_verbose.thread_safe import Pipe
        >>> def compare(pointer):
        ...     pointer[0] = Pipe()
        ...     pointer[1] = Pipe()
        ...
        >>> pointer1 = [None, None]
        >>> compare(pointer1)
        >>> p1, p2 = pointer1
        >>> p1 is p2
        True
        >>> pointer2 = [None, None]
        >>> t = threading.Thread(target=compare, args=(pointer2,))
        >>> t.start()
        >>> t.join()
        >>> p3, p4 = pointer2
        >>> p1 is p3
        False
        >>> p3 is p4
        True
        >>>
        """
        self_id = get_id()
        proc_name = self_id['proc_name']
        thread_name = self_id['thread_name']
        father_proc = self_id['father_proc']
        self_name = f'_pipe_{proc_name}_{thread_name}'
        if self_name not in globals():
            self = super(Pipe, cls).__new__(cls)
            self._init(proc_name, thread_name, father_proc)
            if proc_name == 'MainProcess' and thread_name == 'MainThread':
                self.start()
            globals()[self_name] = self
        return globals()[self_name]

    def _init(self, proc_name, thread_name, father_proc):
        """
        ** Unique initialisator. **
        """
        threading.Thread.__init__(self)
        self.daemon = True

        self.proc_name = proc_name
        self.thread_name = thread_name
        self.father_proc = father_proc

        self.tree = None
        if proc_name == 'MainProcess' and thread_name == 'MainThread':
            self.tree = Tree()

    def add_message(self, message):
        """
        ** Add to the queue, the future message to display. **

        If this object is defined in the main process, it instantly starts the whole display chain.
        Thus, this method returns only when the final 'printt' has taken place.
        If this object is defined in a secondary process, the message is only added to the queue
        to be processed asynchronously in the main process.
        Thus, this method will return before the actual display has taken place.

        Parameters
        ----------
        message : str
            The new lines to display in this thread.
        """
        assert isinstance(message, str)

        # transmission of the message to the main thread of the current process
        if self.thread_name != 'MainThread':
            try:
                father = globals()[f'_pipe_{self.proc_name}_MainThread']
            except KeyError as err:
                raise ImportError(
                    "you have to import 'context_verbose' in the main thread "
                    "before importing it in the secondary threads"
                ) from err
            else:
                father._get_local_message(message, thread_name=self.thread_name)

        # transmission to the father process
        elif self.proc_name != 'MainProcess':
            self._get_local_message(message, thread_name='MainThread')

        # transmission of the message to itself (main thread of the main process)
        else:
            self._get_local_message(message, thread_name='MainThread')

    def _get_local_message(self, message, *, thread_name):
        """
        ** Recover the messages of the different threads of this process. **

        Parameters
        ----------
        message : str
            The new lines to display in this thread.
        thread_name : str
            The name of the child thread.

        Examples
        --------
        >>> from context_verbose.thread_safe import Pipe, _reset_memory
        >>> _reset_memory()
        >>> p = Pipe()
        >>> print(p.tree)
        Tree with 0 nodes and 0 edges
        >>> p._get_local_message('message', thread_name='MainThread')
        message
        >>> print(p.tree)
        Tree with 1 nodes and 0 edges
        >>>
        """
        if self.thread_name != 'MainThread':
            raise RuntimeError('only main threads can collect data from other threads')

        if self.proc_name == 'MainProcess':
            self.tree.add_message(message, proc_name='MainProcess', thread_name=thread_name)
            self.tree.display()
        else:
            raise NotImplementedError(
                'the transfer of information to the process above is not coded'
            )

    def run(self):
        """
        ** Transmits or collects the display tree. **

        Examples
        --------
        >>> import threading
        >>> from context_verbose.thread_safe import Pipe, _reset_memory
        >>> _reset_memory()
        >>> Pipe()
        <Pipe(MainProcess, MainThread)>
        >>>
        >>> def test():
        ...     Pipe().add_line('sentence in the main thread')
        ...     threading.Thread(target=(lambda: Pipe().add_line('text in a subthread'))).start()
        ...     threading.Thread(target=(lambda: Pipe().add_line('text in a subthread'))).start()
        ...
        >>> test() # doctest: +SKIP
        sentence in the main thread
        sentence in the main thread
        ********** ('MainProcess', 'Thread-20') **********
        text in a subthread
        **************************************************
        sentence in the main thread
        ********** ('MainProcess', 'Thread-20') **********
        text in a subthread
        **************************************************
        ********** ('MainProcess', 'Thread-23') **********
        text in a subthread
        **************************************************
        >>>
        """
        if self.thread_name != 'MainThread':
            raise RuntimeError('secondary threads do not need to have an assynchronous behavior')
        if self.proc_name != 'MainProcess':
            raise RuntimeError(
                'only the main thread of the main process must have an asynchronous behavior'
            )

        raise NotImplementedError("we are not able to listen to the children's process")


    def __del__(self):
        """
        ** Disappears and tries to remove the traces. **
        """
        self_name = f'_pipe_{self.proc_name}_{self.thread_name}'
        if self_name in globals():
            del globals()[self_name]

    def __repr__(self):
        """
        ** Offers a better representation. **
        """
        return f'<Pipe({self.proc_name}, {self.thread_name})>'


if EXPERIMENTAL:
    Pipe()
