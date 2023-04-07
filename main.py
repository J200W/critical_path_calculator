from options import *

"""
This is the main class of the program
"""

for i in range(1, nb_of_files+1):
    execution_trace = open("execution_traces/execution_trace_" + str(i) + ".txt", 'w')  # file to write the execution trace
    execution_trace.close()  # close the file

class Main:
    def __init__(self):

        self.graph = None
        self._name = "Main"  # name of the class
        self.file = "tables/"  # path of the tables
        self.file_table = ""  # file of the table
        self.table = 0  # number of the table
        self.runnable = True  # boolean to run the program

        """
        Parameters of the table of constraints
        """

        self.df_constraints = pd.DataFrame()    # dataframe of the table of constraints
        self.columns_constraints = ['Duration', 'Constraints']  # columns of the table of constraints
        self.rows_tasks = []  # rows of the table of constraints (task numbers and list of strings)
        self.durations = []  # durations of the tasks  (list of integers)
        self.constraints = []  # constraints of the tasks  (list of strings)
        self.entries = []  # list of entries of the table of constraints
        self.exits = []  # list of exits of the table of constraints

        """
        Parameters of the value matrix
        """
        self.df_value_matrix = pd.DataFrame()  # dataframe of the value matrix
        self.columns_value_matrix = []  # columns of the value matrix
        self.rows_value_matrix = []  # rows of the value matrix
        self.rank_table = pd.DataFrame()  # dataframe of the rank of the tasks

        """
        Parameters of the earliest date table
        """
        self.task_and_earliest_date = dict()
        self.df_earliest_date = pd.DataFrame()  # dataframe of the earliest date table
        self.df_earliest_date.columns.name = "Ranks"
        self.columns_earliest_date = []
        self.task_and_duration = []  # list of tasks and their durations

        """
        Parameters of the latest date table
        """
        self.task_and_latest_date = dict()
        self.df_latest_date = pd.DataFrame()  # dataframe of the latest date table
        self.df_latest_date.columns.name = "Ranks"
        self.columns_latest_date = []

        """
        Parameters of the floats table and critical path
        """
        self.df_floats = pd.DataFrame()  # dataframe of the floats table
        self.critical_path = []  # list of the critical path
        self.task_and_earliest_date = dict()
        self.critical_paths = []
        self.all_paths = []

    def print_exe(self, obj):   # print the object in the execution trace file
        if 0 < self.table <= nb_of_files:
            with open("execution_traces/execution_trace_"+str(self.table)+".txt", "a") as f:
                print(obj, file=f)
            return
        return


    ##################################################################

    ########################### HOME SCREEN ##########################


    def menu(self):
        """
        Home Screen
        """
        print(welcome)
        while self.runnable:  # while the user wants to continue
            try:
                self.table = int(input("Enter the number of the table: "))
                self.print_exe("Enter the number of the table: " + str(self.table))
            except ValueError:
                self.table = -1
            while self.table not in range(1, 13):   # while the table number is not valid
                print("\nInvalid table number")
                self.print_exe("\nInvalid table number")
                try:
                    self.table = int(input("\nEnter the number of the table: "))
                    self.print_exe("\nEnter the number of the table: " + str(self.table))
                except ValueError:
                    self.table = -1
            self.file_table = self.file + "table " + str(self.table) + ".txt"   # path of the table
            execution_trace_file = open("execution_traces/execution_trace_" + str(self.table) + ".txt", 'w')  # file to write the execution trace
            execution_trace_file.close()  # close the file
            self.print_exe("\nEnter the number of the table: " + str(self.table))
            self.fill_constraint_table(self.file_table)   # create the table of constraints
            self.create_value_matrix()      # create the value matrix

            """
            Check if the graph contains a cycle or a negative duration
            """

            cycle = self.cycle_check(self.df_value_matrix.copy(), self.rows_value_matrix.copy())
            print("\nThe graph n°"+str(self.table)+" contains a cycle : ", cycle)
            self.print_exe("\nThe graph n°"+str(self.table)+" contains a cycle : " + str(cycle))

            negative = self.negative_check(self.durations.copy())
            print("The graph n°"+str(self.table)+" contains a negative duration : ", negative)
            self.print_exe("The graph n°"+str(self.table)+" contains a negative duration : " + str(negative))

            if not cycle and not negative:  # if the graph doesn't contain a cycle or a negative duration
                print("The graph n°"+str(self.table)+" is a scheduling graph.")
                self.print_exe("The graph n°"+str(self.table)+" is a scheduling graph.")
                print("\nRank table n°"+str(self.table)+": \n")
                self.print_exe("\nRank table n°"+str(self.table)+": \n")
                rank_calculator = self.rank_calculator(self.df_value_matrix.copy(), self.rows_value_matrix.copy())
                print(rank_calculator)
                self.print_exe(rank_calculator)

                self.create_schedule_table()  # create the earliest date table and the latest date table

                # print the earliest date table
                print("\nEarliest date table n°"+str(self.table)+": \n")
                print(self.df_earliest_date)
                self.print_exe("\nEarliest date table n°"+str(self.table)+": \n")
                self.print_exe(self.df_earliest_date)

                # print the latest date table
                print("\nLatest date table n°"+str(self.table)+": \n")
                print(self.df_latest_date)
                self.print_exe("\nLatest date table n°"+str(self.table)+": \n")
                self.print_exe(self.df_latest_date)

                # calculate the floats of the tasks
                self.calculate_floats()
                print("\nFloat table n°"+str(self.table)+": \n")
                print(self.df_floats)
                self.print_exe("\nFloat table n°"+str(self.table)+": \n")
                self.print_exe(self.df_floats)

                self.graph = {}
                for task in self.rows_tasks:  # create the graph@
                    self.graph[task] = self.get_successors_constraint(task, self.rows_tasks)  # get the successors of the task

                self.printAllPaths('a', 'w')
                self.critical_paths_calculator()

                print("\nCritical paths n°"+str(self.table)+": \n")
                self.print_exe("\nCritical paths n°"+str(self.table)+": \n")

                print_path = ""
                for path in self.critical_paths:
                    for p in range(len(path)):
                        if p == len(path) - 1:
                            print(path[p])
                            print_path += path[p]
                        else:
                            print(path[p], end=" -> ")
                            print_path += path[p] + " -> "
                    self.print_exe(print_path)
                    print_path = ""


            else:
                print("The graph n°"+str(self.table)+" is NOT a scheduling graph.")
                self.print_exe("This graph n°"+str(self.table)+" is NOT a scheduling graph.")
                print("\nThere are no ranks because the graph n°"+str(self.table)+" contains a cycle or has a negative duration.")
                self.print_exe("\nThere are no ranks because the graph n°"+str(self.table)+" contains a cycle or has a negative duration.")

            """
            Check if the user wants to continue
            """

            print("\nWould you like to continue? (y/n)")

            answer = input()
            answer = answer.strip()

            while answer not in ['y', 'n', 'Y', 'N']:  # check if the answer is valid
                print("Invalid answer")
                self.print_exe("Invalid answer")

                print("\nWould you like to continue? (y/n)")
                answer = input()
                self.print_exe(answer)
            if answer == 'n' or answer == 'N':   # if the answer is no
                self.runnable = False
                print(new_line)
                self.print_exe(new_line)
                print(goodbye)
                sys.exit()
            else:                               # if the answer is yes
                """
                Clear the data
                """
                self.exits, self.entries = [], []
                self.df_constraints, self.df_floats, self.df_earliest_date, self.df_latest_date, self.df_value_matrix, self.rank_table \
                    = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
                self.rows_tasks, self.durations, self.constraints = [], [], []
                self.rows_value_matrix, self.columns_value_matrix, self.task_and_duration = [], [], []
                self.columns_latest_date, self.columns_earliest_date = [], []
                self.task_and_latest_date, self.task_and_earliest_date = dict(), dict()
                self.critical_paths, self.all_paths = [], []
                self.graph = {}
                print(new_line)
                self.print_exe(new_line)
        return

    ##################################################################

    ###################### CONSTRAINT TABLE ##########################


    def create_constraint_table(self, durations, constraints, rows_tasks):  # create the dataframe of the table of constraints
        df_constraints = pd.DataFrame({'Duration': durations, 'Constraints': constraints}, index=rows_tasks)
        df_constraints.columns.name = 'Tasks'
        return df_constraints


    def count_entries(self, constraints):
        entries = 0   # number of entries
        list_entries = []   # list of the tasks that are entries
        for i in range (len(constraints)):   # for each list constraint
            if len(constraints[i]) == 0:   # if the task has no predecessors
                entries += 1   # add one to the number of entries
                list_entries.append(self.rows_tasks[i])   # add the task to the list of entries
        return entries, list_entries   # return the number of entries and the list of the tasks that are entries


    def count_exits(self, constraints):
        exits = 0  # number of exits
        boolean = False  # boolean to check if the task has a predecessor
        list_exits = []   # list of the tasks that are an exits
        t = 0
        j = 0
        while t < len(self.rows_tasks):  # for each task
            while j < len(constraints) and not boolean:   # for each list constraint and if the task has no predecessors
                if self.rows_tasks[t] in constraints[j]:   # if the task is in the constraint
                    boolean = True    # the task has a predecessor
                j += 1    # go to the next constraint
            if not boolean:    # if the task has no entry
                exits += 1   # the task has an exit
                list_exits.append(self.rows_tasks[t])   # add the task to the list of exits
            boolean = False   # reset the boolean
            t += 1  # go to the next task
            j = 0   # reset the index of the constraints
        return exits, list_exits  # return the number of exits and the list of exits


    def assign_entry(self, entries):  # create a new entry 'a' and add it to the list of tasks
        for e in entries:   # for each task that is an entry
            self.df_constraints.at[e, 'Constraints'].append('a')   # add 0 to the list of constraints of the new entry 'a'
        return


    def assign_exit(self, exits):   # create a new exit 'w' and add it to the list of tasks
        for e in exits:   # for each task that is an exit
            self.df_constraints.at['w', 'Constraints'].append(e)   # add the task to the list of constraints of the new exit 'w'
        return


    def fill_constraint_table(self, name_file):
        file = open(name_file, "r")
        line = file.readline()  # read the first line of the file
        while line != "":
            line = line.strip()  # remove the spaces at the beginning and at the end of the line
            line = line.split(" ")
            self.rows_tasks.append(line[0])  # add the task number to the list of rows
            self.durations.append(int(line[1]))   # add the duration to the list of durations
            self.constraints.append(line[2:])   # add the constraints to the list of constraints
            line = file.readline()  # read the next line of the file

        for constraint in self.constraints:   # for each constraint
            if constraint:
                for i in range(len(constraint)):
                    constraint[i].replace(' ', '')  # remove the spaces in self.constraints

        self.entries = self.count_entries(self.constraints)  # count the number of entries and the list of entries
        self.exits = self.count_exits(self.constraints)   # count the number of exits and the list of exits

        if self.entries[0] > 1 or self.get_duration(self.entries[1][0]) != 0:  # if there is more than one entry or the entry has a duration
            self.rows_tasks.insert(0, 'a')  # add the task number to the list of rows
            self.durations.insert(0, 0)  # add the duration to the list of durations
            self.constraints.insert(0, [])  # add the constraints to the list of constraints

        self.rows_tasks.append('w')  # add the task number to the list of rows
        self.durations.append(0)  # add the duration to the list of durations
        self.constraints.append([])  # add the constraints to the list of constraints

        # create the dataframe of the table of constraints
        self.df_constraints = self.create_constraint_table(self.durations, self.constraints, self.rows_tasks)

        # name of the columns of the table of constraints
        self.df_constraints.columns.name = 'Tasks'

        # if there is more than one entry or the entry has a duration
        if self.entries[0] > 1 or self.get_duration(self.entries[1][0]) != 0:
            print("\nWe add a new entry 'a' to the table of constraints.")
            self.print_exe("\nWe add a new entry 'a' to the table of constraints.")
            # add the entry 'a' to the table of constraints and add it to the list of entries
            self.assign_entry(self.entries[1])

        print("We add a new exit 'w' to the table of constraints.")
        self.print_exe("We add a new exit 'w' to the table of constraints.")
        self.assign_exit(self.exits[1])  # add the exit 'N+1' to the table of constraints and add it to the list of exits

        print("\n\nNumber of old entries: ", self.entries[0], " | List of old entries: ", self.entries[1],
              "\nNumber of old exits: ", self.exits[0], " | List of old exits: ", self.exits[1],
              "\n\nTables of constraints n°", self.table, ":\n")  # print the number of entries and the table of constraints

        self.print_exe("\n\nNumber of old entries: " + str(self.count_entries(self.constraints)[0]) + " | List of old entries: " + str(self.entries[1]) +
              "\nNumber of old exits: " + str(self.count_exits(self.constraints)[0]) + " | List of old exits: " + str(self.exits[1]) +
              "\n\nTables of constraints n°" + str(self.table) + ":\n")

        print(self.df_constraints)
        self.print_exe(self.df_constraints)
        file.close()
        return


    def get_successors_constraint(self, task, rows):   # return the successors of a task from the table of constraints
        successors = []
        for i in range(len(self.constraints)):   # for each constraint
            if task in self.constraints[i]:
                successors.append(rows[i].strip())   # add the successor to the list of successors
        return successors


    def get_duration(self, task):  # return the duration of a task
        for i in range(len(self.rows_tasks)):   # for each task
            if task == self.rows_tasks[i]:
                return self.durations[i]

    ##################################################################

    ###################### Value MATRIX ##########################


    def create_value_matrix(self):   # create the value matrix
        self.columns_value_matrix = self.rows_tasks
        self.rows_value_matrix = self.rows_tasks
        self.df_value_matrix = pd.DataFrame(np.full((len(self.rows_value_matrix), len(self.columns_value_matrix)), '-'),
                                                columns=self.columns_value_matrix, index=self.rows_value_matrix)
        for constraint in self.constraints:
            if constraint:  # if the list of constraints of a task is not empty
                for i in range(len(constraint)):
                    successors = self.get_successors_constraint(constraint[i], self.rows_value_matrix)   # get the successors of the given task
                    duration = self.get_duration(constraint[i])   # get the duration of the given task from the table of constraints

                    for j in range(len(successors)):
                        self.df_value_matrix[constraint[i]][successors[j]] = duration   # add the duration to the value matrix

        self.df_value_matrix =  self.df_value_matrix.transpose()  # transpose the value matrix
        self.df_value_matrix.columns.name = 'Tasks'  # name of the columns of the value matrix
        print("\n\nValue matrix n°", self.table ,":\n")
        self.print_exe("\n\nValue matrix n°" + str(self.table) + ":\n")

        print(self.df_value_matrix)
        self.print_exe(self.df_value_matrix)
        return


    def get_predecessors_value(self, value_matrix, task, rows):   # return the successors of a task from the value matrix
        predecessors = value_matrix.loc[:, task]  # list of predecessors
        tasks_predecessors = []  # list of tasks
        for i in range(len(predecessors)):
            if predecessors[i] != '-':
                tasks_predecessors.append(rows[i].strip())  # add the task to the list of tasks
        return tasks_predecessors


    ##################################################################

    ######################## CHECK PROPERTIES #########################


    def negative_check(self, durations):  # check if there is a negative edge in the graph thanks to the table of constraints
        for i in range(len(durations)):
            if durations[i] < 0:
                return True
        return False

    def cycle_check(self, value_matrix, rows):  # check if there is a cycle in the graph
        cycle = False
        i = 0
        print("\nMethod of eliminating entry points")
        self.print_exe("\nMethod of eliminating entry points")
        list_of_t_null_in_degree = []  # list of tasks with null in degree
        while len(rows) > 0 and not cycle:  # while there are tasks and there is no cycle
            while i < len(rows):  # for each task in the list of tasks
                list_predecessors = self.get_predecessors_value(value_matrix.copy(), rows[i], rows)
                in_degree = len(list_predecessors)
                if in_degree == 0:  # if the task has no predecessors
                    list_of_t_null_in_degree.append(rows[i])  # add the task to the list of tasks with null in degree
                i += 1
            i = 0  # restart the loop
            if len(list_of_t_null_in_degree) == 0:  # if there is no task with null in degree
                cycle = True

            else:
                print("\nEntry point(s) found: ", list_of_t_null_in_degree)
                self.print_exe("\nEntry point(s) found: " + str(list_of_t_null_in_degree))
                print("Removing entry point(s)...")
                self.print_exe("Removing entry point(s)...")

                for j in range(len(list_of_t_null_in_degree)):
                    value_matrix.drop(columns=list_of_t_null_in_degree[j],
                                          inplace=True)  # remove the task from the value matrix
                    value_matrix.drop(index=list_of_t_null_in_degree[j],
                                          inplace=True)  # remove the task from the value matrix
                    rows.remove(list_of_t_null_in_degree[j])  # remove the task from the list of tasks

                list_of_t_null_in_degree = []  # empty the list of tasks with null in degree

        if len(rows) != 0:  # if there is still a task in the graph
            cycle = True
            print("\nNo more entry point found...")
            self.print_exe("\nNo more entry point found...")
        else:
            print("\nNo more task in the graph...")
            self.print_exe("\nNo more task in the graph...")
        return cycle

    ##################################################################

    ######################## RANK TABLE ##############################


    def rank_calculator(self, value_matrix, rows):  # calculate the rank of tasks
        table_of_ranks = pd.DataFrame(np.full((len(rows), 1), ' '), columns=['Rank'], index=rows)
        i = 0
        rank = 0
        list_of_t_null_in_degree = []  # list of tasks with null in degree
        while len(rows) > 0:  # while there are tasks
            while i < len(rows):  # for each task
                list_predecessors = self.get_predecessors_value(value_matrix.copy(), rows[i], rows)
                in_degree = len(list_predecessors)
                if in_degree == 0:  # if the task has no predecessors
                    list_of_t_null_in_degree.append(rows[i])  # add the task to the list of tasks with null in degree
                i += 1

            for j in range(len(list_of_t_null_in_degree)):
                value_matrix.drop(columns=list_of_t_null_in_degree[j], inplace=True)  # remove the task from the value matrix
                value_matrix.drop(index=list_of_t_null_in_degree[j], inplace=True)  # remove the task from the value matrix
                rows.remove(list_of_t_null_in_degree[j])  # remove the task from the list of tasks
                table_of_ranks['Rank'][list_of_t_null_in_degree[j]] = rank  # add the rank to the table of ranks

            list_of_t_null_in_degree = []   # empty the list of tasks with null in degree
            rank += 1  # increment the rank
            i = 0  # restart the loop
        self.rank_table = table_of_ranks
        self.rank_table.columns.name = 'Task'  # name of the columns of the table of ranks
        self.rank_table.sort_values(by=['Rank'], inplace=True)  # sort the table of ranks
        return table_of_ranks


    ##################################################################

    ######################## CALENDAR TABLES #########################


    def create_schedule_table(self):
        self.columns_earliest_date = self.rank_table['Rank'].to_list()  # name of the columns of the earliest date table
        self.df_earliest_date = pd.DataFrame(index=["Task & duration", "Predecessors","Earliest date"],
                                             columns=self.columns_earliest_date)  # name of the columns of the earliest date table

        self.df_latest_date = pd.DataFrame(index=["Task & duration", "Successors","Latest date"],
                                             columns=self.columns_earliest_date)  # name of the columns of the earliest date table

        # name of the columns of the earliest and latest date table
        self.df_earliest_date.columns.name = 'Rank'
        self.df_latest_date.columns.name = 'Rank'

        # add the tasks to the table and their duration
        self.df_earliest_date.loc["Task & duration"] = [i + '(' +str(self.get_duration(i)) + ')' for i in self.rank_table.index]
        self.df_latest_date.loc["Task & duration"] = [i + '(' +str(self.get_duration(i)) + ')' for i in self.rank_table.index]

        # list of tasks from rank 0 to n
        tasks = self.df_earliest_date.loc["Task & duration"].to_list()

        # add the predecessors to the table
        predecessors = [self.get_predecessors_value(self.df_value_matrix.copy(), i, self.rank_table.index) for i in self.rank_table.index]
        successors = [self.get_successors_constraint(i, self.rows_tasks) for i in self.rank_table.index]

        # add the successors and the predecessors to the table
        self.df_earliest_date.loc["Predecessors"] = predecessors
        self.df_latest_date.loc["Successors"] = successors

        # remove the duration from the tasks
        for i in range (len(tasks)):
            tasks[i] = tasks[i].split("(")[0]

        # dictionary of the earliest durations
        self.task_and_duration = dict()
        self.task_and_earliest_date = dict()
        self.task_and_latest_date = dict()

        # add the tasks to the dictionary and initialize the earliest date and the latest date to 0
        for i in range(len(tasks)):
            self.task_and_duration[tasks[i]] = self.get_duration(tasks[i])
            self.task_and_earliest_date[tasks[i]] = 0
            self.task_and_latest_date[tasks[i]] = 0

        # calculate the earliest dates
        self.calculate_earliest_dates(tasks)
        task_and_earliest_date = list(self.task_and_earliest_date.values())  # list of the earliest dates
        self.df_earliest_date.loc["Earliest date"] = task_and_earliest_date  # add the earliest dates to the table

        # calculate the latest dates
        self.calculate_latest_dates(tasks)
        task_and_latest_date = list(self.task_and_latest_date.values())  # list of the latest dates
        self.df_latest_date.loc["Latest date"] = task_and_latest_date  # add the latest dates to the table
        return


    def calculate_earliest_dates(self, tasks):
        for task in tasks:  # for each task
            predecessors = self.get_predecessors_value(self.df_value_matrix.copy(), task, self.rows_tasks)

            if len(predecessors) == 0:
                self.task_and_earliest_date[task] = 0
            else:
                max_earliest_date = 0
                for predecessor in predecessors:  # for each predecessor of the task
                    duration = self.task_and_duration[predecessor]   # duration of the predecessor
                    if self.task_and_earliest_date[predecessor] + duration > max_earliest_date:
                        max_earliest_date = self.task_and_earliest_date[predecessor] + duration
                        self.task_and_earliest_date[task] = max_earliest_date
        return


    def calculate_latest_dates(self, tasks):
        tasks = tasks[::-1]  # reverse the list of tasks
        for task in tasks:
            successors = self.get_successors_constraint(task, self.rows_tasks)  # list of successors of the task
            if len(successors) == 0:
                self.task_and_latest_date[task] = max(self.task_and_earliest_date.values())
            else:
                min_latest_date = max(self.task_and_earliest_date.values())
                for successor in successors:
                    duration = self.task_and_duration[task]
                    if self.task_and_latest_date[successor] - duration <= min_latest_date:
                        min_latest_date = self.task_and_latest_date[successor] - duration
                        self.task_and_latest_date[task] = min_latest_date
        return


    ####################################################################

    ########################## CRITICAL PATHS ##########################


    def calculate_floats(self):
        self.df_floats = pd.DataFrame(index=["Task & duration", "Successors", "Earliest date", "Latest date", "Free float", "Total float"],
                                             columns=self.columns_earliest_date)
        self.df_floats.columns.name = 'Rank'
        self.df_floats.loc["Successors"] = self.df_latest_date.loc["Successors"]  # add the successors to the table
        self.df_floats.loc["Task & duration"] = self.df_latest_date.loc["Task & duration"]  # add the tasks to the table
        self.df_floats.loc["Earliest date"] = self.df_earliest_date.loc["Earliest date"]    # add the earliest dates to the table
        self.df_floats.loc["Latest date"] = self.df_latest_date.loc["Latest date"]          # add the latest dates to the table
        self.df_floats.loc["Free float"] = self.calculator_free_float()
        # add the total float to the table
        self.df_floats.loc["Total float"] = self.df_latest_date.loc["Latest date"] - self.df_earliest_date.loc["Earliest date"]
        return

    def calculator_free_float(self):
        free_floats = dict()
        for i in range(len(self.rank_table.index)):   # initialize the free floats to None
            free_floats[self.rank_table.index[i]] = None
        for i in range(len(self.rank_table.index)):   # for each task
            task = self.rank_table.index[i]
            successors = self.get_successors_constraint(task, self.rows_tasks)  # list of successors of the task
            if len(successors) > 0:
                min_ed = self.task_and_earliest_date[successors[0]]  # min earliest date
                for success in successors:
                    if self.task_and_earliest_date[success] < min_ed:  # if the earliest date of the successor is smaller than the current min earliest date
                        min_ed = self.task_and_earliest_date[success]
                free_floats[task] = min_ed - self.task_and_earliest_date[task] - self.task_and_duration[task]
            else:
                free_floats[task] = 0
        return list(free_floats.values())

    def critical_nodes_calculator(self):  # calculate the critical nodes
        critical_path = []
        for i in range(len(self.df_floats.loc["Total float"].to_list())):  # for each total float
            if self.df_floats.loc["Total float"].to_list()[i] == 0:        # if the total float is 0
                critical_path.append(self.df_floats.loc["Task & duration"].to_list()[i])  # add the task to the critical path

        critical_path = [c.split("(")[0] for c in critical_path]    # remove the duration from the tasks
        return critical_path

    def critical_paths_calculator(self):
        critical_nodes = self.critical_nodes_calculator()  # list of the critical nodes
        for path in self.all_paths:
            if self.check_critical_path(path, critical_nodes):  # check if a path is critical one
                self.critical_paths.append(path)   # add the critical path to the list of the critical paths
        return

    def check_critical_path(self, path, critical_nodes):  # check if a path is critical one
        duration_project = max((list(self.task_and_latest_date.values()))) - min(list(self.task_and_earliest_date.values()))
        set_critical_nodes = set(critical_nodes)
        set_path = set(path)
        if not set_path.issubset(set_critical_nodes):  # if the path is not a subset of the critical nodes
            return False
        total_duration = 0
        for i in range(len(path)):
            total_duration += self.task_and_duration[path[i]]  # calculate the total duration of the path
        # if the total duration is smaller than the max duration of the project
        if total_duration < duration_project:
            return False
        return True

    def printAllPathsUtil(self, start, end, visited_tasks, path):

        # Mark the current node as visited and store in path
        visited_tasks[start] = True
        path.append(start)

        # If current vertex is same as destination, then print
        # current path[]
        if start == end:
            self.all_paths.append(path.copy())
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[start]:
                if not visited_tasks[i]:
                    self.printAllPathsUtil(i, end, visited_tasks, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited_tasks[start] = False

    # Prints all paths from 'start' to 'end'
    def printAllPaths(self, start, end):

        # Mark all the vertices as not visited
        visited_tasks = {v: False for v in self.rows_tasks}

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(start, end, visited_tasks, path)

main = Main()
main.menu()
