/*--***************************************************************************

Execute multiple commands (serial tasks) parallely on multiple cores. This is
useful to parallize your serial tasks on HPC cluster.

Usage: A text file containing the commands that you want to execute should be 
       provided as the input to the program in such a syntax:
           $ mpirun -np N multi_tasks -in commands.txt
       The first N line of the input file will be read and executed 
       independently by each of the N cores you invoked.

Notes: 1) Compile using MPI and C++11 standard:
           $ mpic++ -std=c++0x multi_tasks.cpp -o multi_tasks
       2) Be careful about the independency of the outputs by each line of 
       command. Make sure they don't conflict to each other.

Created: 16/Mar/2016

***************************************************************************--*/

#include "fstream"
#include "mpi.h"
#include "string.h"
#include "vector"

using namespace std;

vector<string> GetInput(char *filename);
int RunTask(int id, string *p_command);

int main(int argc, char *argv[])
{
    int id;
    int n_procs;
    int run_status;
    char *input_file_name;
    vector<string> commands;
    MPI::Status status;

    if (argc == 3 && strcmp(argv[1], "-in") == 0){
        input_file_name = argv[2];
    }else{
        cout << "Syntax: ... -in commands.txt" << endl;
        return 0;
    }

    commands = GetInput(input_file_name);

    MPI::Init();
    id = MPI::COMM_WORLD.Get_rank();
    n_procs = MPI::COMM_WORLD.Get_size();
    
    if (id == 0){         
        cout << "\n" << n_procs << " tasks are created..." << endl; 
        cout << commands.size() << " commands read ";
        cout << "from \'" << input_file_name << "\'." << endl;

        if (n_procs != commands.size()){
            cout << "Warning: NOT MACTHING!" << endl << endl;
        }
    }
    run_status = RunTask(id, &commands[id]);

    MPI::Finalize();
    return 0;
}

vector<string> GetInput(char *filename)
{  
    ifstream input_file(filename);
    string buffer; 
    vector<string> commands;
 
    while (getline(input_file, buffer)){ 
       commands.push_back(buffer);
    }

    return commands;
}

int RunTask(int id, string *p_command)
{
    int status = 0;
    string command_str; 
    string stdout_str = " 1> proc." + to_string(id) + ".o";
    string stderr_str = " 2> proc." + to_string(id) + ".e";  

    cout << "On Proc " << id << ":" << endl;
    cout << "  " << *p_command << endl;
    command_str = *p_command + stdout_str + stderr_str;

    const char *command = command_str.c_str();
    status = system(command);

    return status;
}
