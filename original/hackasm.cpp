#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;
#define SIN(x, S) (S.count(x) != 0)
// 16-bit Hack assembly

string IntToBinstr(int x, int n) {
    vector<char> s(n);
    int tmp = 1;
    for(size_t i = 0; i < n; i++) {
        if(x % 2 == 0)
            s[i] = '0';
        else
            s[i] = '1';
        x = x / 2;
    }

    string ret = "";
    for(size_t i = 0; i < n; i++) {
        ret = s[i] + ret;
    }
    return ret;
}

string comptrans(string compstr) {
    // a = 0
    if(compstr == "0")
        return "0101010";
    if(compstr == "1")
        return "0111111";
    if(compstr == "-1")
        return "0111010";
    if(compstr == "D")
        return "0001100";
    if(compstr == "A")
        return "0110000";
    if(compstr == "!D")
        return "0001101";
    if(compstr == "!A")
        return "0110001";
    if(compstr == "-D")
        return "0001111";
    if(compstr == "-A")
        return "0110011";
    if(compstr == "D+1")
        return "0011111";
    if(compstr == "A+1")
        return "0110111";
    if(compstr == "D-1")
        return "0001110";
    if(compstr == "A-1")
        return "0110010";
    if(compstr == "D+A")
        return "0000010";
    if(compstr == "D-A")
        return "0010011";
    if(compstr == "A-D")
        return "0000111";
    if(compstr == "D&A")
        return "0000000";
    if(compstr == "D|A")
        return "0010101";

    // a = 1
    if(compstr == "M")
        return "1110000";
    if(compstr == "!M")
        return "1110001";
    if(compstr == "-M")
        return "1110011";
    if(compstr == "M+1")
        return "1110111";
    if(compstr == "M-1")
        return "1110010";
    if(compstr == "D+M")
        return "1000010";
    if(compstr == "D-M")
        return "1010011";
    if(compstr == "M-D")
        return "1000111";
    if(compstr == "D&M")
        return "1000000";
    if(compstr == "D|M")
        return "1010101";

    // for convenience
    if(compstr == "A+D")
        return comptrans("D+A");
    return "-1";
}

string desttrans(string deststr) {
    if(deststr == "")
        return "000";
    if(deststr == "M")
        return "001";
    if(deststr == "D")
        return "010";
    if(deststr == "MD")
        return "011";
    if(deststr == "A")
        return "100";
    if(deststr == "AM")
        return "101";
    if(deststr == "AD")
        return "110";
    if(deststr == "AMD")
        return "111";
    return "-1";
}

string jumptrans(string jumpstr) {
    if(jumpstr == "")
        return "000";
    if(jumpstr == "JGT")
        return "001";
    if(jumpstr == "JEQ")
        return "010";
    if(jumpstr == "JGE")
        return "011";
    if(jumpstr == "JLT")
        return "100";
    if(jumpstr == "JNE")
        return "101";
    if(jumpstr == "JLE")
        return "110";
    if(jumpstr == "JMP")
        return "111";

    return "-1";
}

string Aproc(string str, map<string, int> &variable, set<string> &variable_set, int &valuecount) {
    // retrun A code binary
    // Error .. return ""
    const int BIN15_MAX = 32767;
    int len = str.length();
    string output = "";
    string s = str.substr(1); // _************
    if(len == 1) {
        return "";
    }

    int A;

    if(('0' <= str[1]) and (str[1] <= '9')) {
        // 0,1,2..9
        try {
            A = stoi(s);
        } catch(invalid_argument e) {
            return "";
        }
    } else {
        if(SIN(s,variable_set)){
            A = variable[s];
        } else {
            // new variable
            A = variable[s] = valuecount;
            variable_set.insert(s);
            valuecount++;
        }
    }

    if(A > BIN15_MAX)
        return "";
    return "0" + IntToBinstr(A, 15);
}

int CstrParse(string str, string &dest, string &comp, string &jump) {
    // Error -> 1/
    // overwrite dest,comp,jump from str.
    int len = str.length();
    bool eq = false;
    bool semicolon = false;
    comp = str; // 0;JMP pattern

    for(int i = 0; i < len; i++) {
        char c = str[i];
        if(c == '=') {
            if(eq) {
                return 1;
            }

            eq = true;
            dest = str.substr(0, i);
            comp = str.substr(i + 1);
        }
    }

    int complen = comp.length();
    for(int i = 0; i < complen; i++) {
        char c = comp[i];
        if(c == ';') {
            if(semicolon) {
                return 1;
            }

            semicolon = true;
            string temp = comp;
            comp = temp.substr(0, i);
            jump = temp.substr(i + 1);
        }
    }

    return 0;
}

void variable_init(map<string, int> &variable, set<string> &variable_set){
    variable["SCREEN"] = 16384;
    variable["KBD"] = 24576;
    variable_set.insert("SCREEN");
    variable_set.insert("KBD");
    for (size_t i = 0; i < 16; i++)
    {
        string v = "R" + to_string(i);
        variable[v] = i;
        variable_set.insert(v);
    }
    
    variable["SP"] = 0;
    variable["LCL"] = 1;
    variable["ARG"] = 2;
    variable["THIS"] = 3;
    variable["THAT"] = 4;
    variable_set.insert("SP");
    variable_set.insert("LCL");
    variable_set.insert("ARG");
    variable_set.insert("THIS");
    variable_set.insert("THAT");
}

string Cproc(string deststr, string compstr, string jumpstr) {
    string output = "111";
    string compbin = comptrans(compstr);
    string destbin = desttrans(deststr);
    string jumpbin = jumptrans(jumpstr);

    if(compbin == "-1")
        return "";
    if(destbin == "-1")
        return "";
    if(jumpbin == "-1")
        return "";

    output += compbin;
    output += destbin;
    output += jumpbin;

    return output;
}


int main(int argc, char *argv[]) {
    if (argc == 1){
        cout << "Usage: ./hackasm <source file> (<output file>)" << endl;
        return 1;
    }

    int valuecount = 16;
    string outfilename = "a.hack";

    if (argc == 3){
        outfilename = argv[2];
    }


    map<string, int> variable; // (address)
    set<string> variable_set;

    variable_init(variable,variable_set);

    ifstream ifs(argv[1], ios::in);
    ofstream ofs(outfilename, ios::out);

    if(!ifs) {
        cerr << "Error! File can't be opened." << endl;
        return 1;
    }

    if(!ofs) {
        cerr << "Error! File can't be saved." << endl;
        return 1;
    }

    string str;
    vector<string> input;
    vector<string> output;
    int linecnt = 0;

    while(getline(ifs, str)) {
        int len = str.length();
        for(int i = 0; i < len - 1; i++) {
            if((str[i] == '/') and (str[i + 1] == '/')) {
                str = str.substr(0, i);
                break;
            }
        }

        str.erase(remove(str.begin(), str.end(), ' '), str.end());
        str.erase(remove(str.begin(), str.end(), '\r'), str.end());
        str.erase(remove(str.begin(), str.end(), '\n'), str.end());
        len = str.length();
        if(len == 0)
            continue; // empty line

        if (str[0] == '('){
            if (str[len - 1] != ')'){
                cout << "syntax error (label)" << endl;
                return 0;
            }

            string newlabel = str.substr(1,len - 2);
            if (SIN(newlabel,variable_set)){
                cout << "duplicate label error" << endl;
                return 0;
            }else{
                variable[newlabel] = linecnt;
                variable_set.insert(newlabel);
            }
        }else{
            // not label
            linecnt++;
            input.push_back(str);
        }
    }




    for(const auto & str : input){
        string outputline = "";
        // comment

        if(str[0] == '@') { // A
            outputline = Aproc(str, variable, variable_set, valuecount);
            if(outputline == "") { // Error
                cout << "str = " << str << endl;
                cout << "syntax error(A code)" << endl;
                return 0;
            }
        } else { // C .. dest = comp;jump
            string deststr = "";
            string compstr = "";
            string jumpstr = "";
            if(CstrParse(str, deststr, compstr, jumpstr) != 0) {
                cout << "syntax error (C parse)" << endl;
                return 0;
            }
           
            outputline = Cproc(deststr, compstr, jumpstr);
            if(outputline == "") {
                cout << "syntax error(C proc)" << endl;
                return 0;
            }
            // cout << output << "\n";
        }

        output.push_back(outputline);
    }

    for(const auto str : output){
        ofs << str << "\n";
    }

    ifs.close();
    ofs.close();

    cout << "OK" << "\n";
    cout << "Saved as " + outfilename << endl;
}