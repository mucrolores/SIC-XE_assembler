#include <iostream>
#include <fstream>
using namespace std;
int main()
{
	ofstream out;
	out.open("instruc.txt");
	string mnemonicCode;
	string OPCode;
	
	for(int i=0;mnemonicCode!="exit" || OPCode != "exit";i++)
	{
		cin >> mnemonicCode;
		cin >> OPCode;
		out << "\"" << mnemonicCode << "\"";
		out << ":";
		out << "\"" << OPCode << "\"";
		out << ",";
		if((i+1)%5==0)
		{
			out << "\n";
		}
	}
	out.close();
	system("PAUSE");
} 
