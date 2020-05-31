#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#define ALL(X) (X).begin(), (X).end()
using namespace std;

int main(int argc, char *argv[]) {

    if(argc == 1) {
        cout << "Usage: ./VNtranslator <source file> (<output file>)" << endl;
        return 1;
    }
    string outfilename = "a.asm";

    if(argc == 3) {
        outfilename = argv[2];
    }

    ifstream ifs(argv[1], ios::in);
    // ofstream ofs(outfilename, ios::out);

    if(!ifs) {
        cerr << "Error! File can't be opened." << endl;
        return 1;
    }

    string str;

    while(getline(ifs, str, '\n')) { // each line
        stringstream ss(str);
        vector<string> cmd;
        while(!ss.eof()){
            string tmp;
            ss >> tmp;
            if (tmp == "") continue; // 
            cmd.emplace_back(tmp);
        }

        if (cmd.size() == 2){
            if (cmd[0] == "push"){
                if (cmd[1] == "constant"){
                    int num = stoi(cmd[2]); // TODO try catch
                    
                }
            }
        }
    }


}
