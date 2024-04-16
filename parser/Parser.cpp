#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Parser {
private:
    string res;
    vector<char> inp;

public:
    Parser() {
        res = "";
    }

    bool validateS() {
        res += "S";
        if (inp.empty() || (inp[0] != 'a' && inp[0] != 'b')) {
            return false;
        } else {
            char symbol = inp[0];
            inp.erase(inp.begin());
            if (symbol == 'a') {
                return validateA() && validateB();
            } else { // inace je sigurno b
                return validateB() && validateA();
            }
        }
        
    }

    bool validateA() {
        res += "A";
        if (inp.empty() || (inp[0] != 'a' && inp[0] != 'b')) {
            return false;
        } else {
            char symbol = inp[0];
            inp.erase(inp.begin());
            if (symbol == 'a') {
                return true;
            } else { // inace je opet sigurno b
                return validateC();
            }
        }
    }

    bool validateB() {
        res += "B";
        if (inp.empty() || inp[0] != 'c') { // drugi uvjet je zbog epsilona, on tu moze samo stati 
            return true;
        }
        else if (inp[0] == 'c' && inp[1] == 'c' && inp.size() >= 2) { // gledamo samo prva dva slova
            inp.erase(inp.begin(), inp.begin() + 2);
            if (validateS() && inp.size() >= 2 && inp[0] == 'b' && inp[1] == 'c') { // gledamo drugi dio 
                inp.erase(inp.begin(), inp.begin() + 2);
                return true;
            }
        }
        return false;
    }

    bool validateC() {
        res += "C";
        return validateA() && validateA();
    }

    void parse(string str) {
        for (char &c : str) {
            inp.push_back(c);
        }

        if (validateS() && inp.empty()) { // pokreni sve sa validateS i na kraju vidi je li input ispraznjen
            cout << res << endl;
            cout << "DA" << endl;
        } else {
            cout << res << endl;
            cout << "NE" << endl;
        }
    }
};

int main() {
    string str;
    getline(cin, str);

    Parser p;
    p.parse(str);

    return 0;
}
