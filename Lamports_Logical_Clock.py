"""
Author: André Martins (ID:0230991223)

Python script implementing the Lamport's logical clock algorithm. All the information related to the logic of the implementation can be found
on the available README.md file.
"""

#Constants
CLOCK_CALCULATION_LIMIT = 15

# Task Class

class Task:
    """
    Class representing one task, will be used together with "Processes".
    """
    def __init__(self, clock_value, depends_on, inv_depends_on, identifier):
        """
            Class constructor:

            Parameters:
            ------------------------------
            :param clock_value: (int) value of the logical clock, if unknown please set it as "None"
            :param depends_on: (Task) Dependent task of the current task (This task depends on the depends_on task)
            :param inv_depends_on: (Task) Inverse dependent task of the current task (The inv_depends_on depends on the newly defined task)
            :param identifier: (string) Identifier that will be used for beauty printing
            """
        self.clock_value = clock_value
        self.depends_on = depends_on
        self.inv_depends_on = inv_depends_on
        self.identifier = identifier

class Process:
    """
    Class representing one Process, will be used together with "Processes" and with LogicalClockSystem.
    """
    def __init__(self, is_clock_defined, identifier):
        """
        Class constructor:

        Parameters:
        --------------------------
        :param is_clock_defined: (boolean) attribute defining the allowing to quickly identifying if all the clock values have been defined
        :param identifier: (string) Identifier that will be used for beauty printing
        """
        self.tasks = []
        self.is_clock_defined = is_clock_defined
        self.identifier = identifier

    # General getters and setters
    def add_task(self, task):
        self.tasks.append(task)
        return self.tasks

    def set_tasks(self, tasks):
        self.tasks = tasks
        return self.tasks

    def get_tasks(self):
        return self.tasks

    def get_task(self, index):
        return self.tasks[index]

    # Clock related methods
    def define_clock(self):
        """
        This method will go through all of it's defined Tasks and define the correct clock value to it.
        If there are any dependency issues (dependent nodes/tasks) it will not stop the execution

        This method also changes the value is_clock_defined to the according state.
        :return: (boolean) value representing the execution result
        """
        counter = 1
        for task in self.tasks:
            # Checking dependency
            if task.depends_on is None: # does not have any dependencies
                task.clock_value = counter
                counter += 1
            else: # is dependent of another task [this_task<--another_task]
                if task.depends_on.clock_value is None: # case where dependency has not been defined yet
                    self.is_clock_defined = False
                    return False
                else:
                    if task.depends_on.clock_value > counter:
                        counter = task.depends_on.clock_value + 1
                        task.clock_value = counter
                        counter += 1
                    else:
                        task.clock_value = counter
                        counter += 1
        self.is_clock_defined = True
        return True

    def get_clock_of_task(self, index):
        """Method allowing to directly get the clock of a specific task."""
        if not self.is_clock_defined:
            print("Clock has not been defined yet")
            return None
        if index < 0 or index >= len(self.tasks):
            print("Invalid index at get_clock_of_task")
            return None
        return self.tasks[index].clock_value

class LogicalClockSystem:
    """Top layer class for this script allowing to represent Logical Clock containing different processes."""
    def __init__(self, all_processes):
        """
        Class constructor:
        The attribute is_complete is always set to False in order to force the user to use the implemented methods of ordering

        Parameters:
        ----------------------
        :param all_processes: (list of Process) list of current tests represented in their internal ordering
        """
        self.all_processes = all_processes
        self.is_complete = False

    # getters and setters
    def add_process(self, process):
        self.all_processes.append(process)

    def get_processes(self):
        return self.all_processes

    def get_process(self, index):
        return self.all_processes[index]

    # Clock related methods
    def define_clock_for_all_processes(self):
        """
        This method loops through the list of processes and tries to execute each process define_clock() method until all the processes have the respective
        task's clock values defined.

        Currently, the method stops after looping through all the processes for CLOCK_CALCULATION_LIMIT times to avoid a possible infinite loop.

        The method also changes the is_finished attribute accordingly.
        :return: (boolean) value representing the execution result
        """
        limiter = CLOCK_CALCULATION_LIMIT
        is_finished = False
        while not is_finished and limiter > 0:
            is_finished = True
            for process in self.all_processes:
                is_finished =  process.define_clock() and is_finished
            limiter -= 1
        self.is_complete = is_finished
        return is_finished

    def define_execution_order(self):
        """
        This method defines teh main execution order using both conditions defined in the Lamport's logical clock algorithm.

        It uses the previously task clock number as a first argument of order and uses the process order defined in the list as a second argument.
        :return: ([Task], [string]) Return the final execution order both as a list of object references for each task as well as an array of the representative
        strings.
        """
        if not self.is_complete:
            print("Clock has not been defined yet for all processes")
            return None

        result = []
        result_beauty_print = []
        maximum_clock_value = 0
        # Getting the biggest clock value such that we do know how where to stop
        for process in self.all_processes:
            for task in process.tasks:
                if task.clock_value > maximum_clock_value:
                    maximum_clock_value = task.clock_value
        # Defining main order
        current_clock_value = 1
        while current_clock_value <= maximum_clock_value:
            for process in self.all_processes:
                for task in process.tasks:
                    if task.clock_value == current_clock_value:
                        result.append(task)
                        result_beauty_print.append("P" + str(process.identifier) + "(" + str(task.identifier) + ") [Clock= " + str(current_clock_value) + "]")

            current_clock_value += 1

        return result, result_beauty_print


#Helper functions
def beauty_array_print(array):
    for i in range(len(array)):
        print("\t-pos:" + str(i+1) + "=>" +array[i])

if __name__ == '__main__':
    print("Stating Lamport's logical clock...")
    # Creating all processes and tasks
    process_p = Process(is_clock_defined=False, identifier="p")
    p1 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="1")
    p2 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="2")
    p3 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="3")
    p4 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="4")
    process_q = Process(is_clock_defined=False, identifier="q")
    q1 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="1")
    q2 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="2")
    q3 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="3")
    q4 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="4")
    q5 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="5")
    q6 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="6")
    q7 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="7")
    process_r = Process(is_clock_defined=False, identifier="r")
    r1 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="1")
    r2 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="2")
    r3 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="3")
    r4 = Task(clock_value=None, depends_on=None, inv_depends_on=None, identifier="4")
    # Adding all dependencies
    p2.depends_on = q1
    q1.inv_depends_on = q2

    p4.depends_on = q5
    q5.inv_depends_on = p4

    q2.depends_on = p1
    p1.inv_depends_on = q2

    q7.depends_on = r2
    r2.inv_depends_on = q7

    r3.depends_on = q4
    q4.inv_depends_on = r3

    r4.depends_on = q1
    q1.inv_depends_on = r4

    # Putting everything together
    process_p.add_task(p1)
    process_p.add_task(p2)
    process_p.add_task(p3)
    process_p.add_task(p4)
    process_q.add_task(q1)
    process_q.add_task(q2)
    process_q.add_task(q3)
    process_q.add_task(q4)
    process_q.add_task(q5)
    process_q.add_task(q6)
    process_q.add_task(q7)
    process_r.add_task(r1)
    process_r.add_task(r2)
    process_r.add_task(r3)
    process_r.add_task(r4)

    mainSystem = LogicalClockSystem(all_processes=[process_p, process_q, process_r])

    print("Determining clock values for each task and ordering them")
    mainSystem.define_clock_for_all_processes()
    objects, beauty_list = mainSystem.define_execution_order()

    print("Final execution order:-----")
    beauty_array_print(beauty_list)
    print("---------------------------")

