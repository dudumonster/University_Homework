/*人工智能基础 8数码实验代码下发版2023*/
#include<iostream>
#include<cmath>
#include "stdlib.h" 
#include "time.h" 
#include<stack>
#include<queue>
using namespace std;
#define num 9
struct Node {
	int state[9];
	struct Node* parent;
	int value;
	int depth;
	friend bool operator < (Node A, Node B){ 
		if (A.value == B.value) return A.depth > B.depth;
		return A.value > B.value;
	}
};

priority_queue<Node> openTable;     //open表
queue<Node> closeTable;     //close表
stack<Node> Path;     //生成路径
int count1 = 0, count2 = 0;

bool read(Node& S, Node& G) {
	//初始化
	S.parent = NULL;	S.depth = 0;	S.value = 0;
	G.parent = NULL;	G.depth = 0;	G.value = 0;

	cout << "请输入初始状态\n";
	for (int i = 0; i < num; i++)
		cin >> S.state[i];
	cout << "请输入目标状态?\n";
	for (int i = 0; i < num; i++)
		cin >> G.state[i];

	for (int i = 0; i <= num - 2; i++)
		for (int j = i + 1; j < num; j++)
			if (S.state[i] > S.state[j] && S.state[i] * S.state[j] != 0)
				count1++;

	for (int i = 0; i <= num - 2; i++)
		for (int j = i + 1; j < num; j++)
			if (G.state[i] > G.state[j] && G.state[i] * G.state[j] != 0)
				count2++;


	if (count1 % 2 != count2 % 2){
		cout << "始末状态逆序数奇偶性不同!" << endl;
		return false;
	}
	return true;
}

int value1(Node A, Node G) { //利用不在位数计算value
	int count = 8;
	for (int i = 0; i < num; i++)
		if (A.state[i] == G.state[i] && G.state[i] != 0)
			count--;
	return count + A.depth;

}

int value2(Node A, Node G) {  //利用哈密顿距离计算value，请补充完整
	int count = 0;
	//int begin[3][3], end[3][3];           
	return count + A.depth;
}


//用于判断两结点是否相同
bool judge(Node S, Node G){
	for (int i = 0; i <= 8; i++)
	{
		if (S.state[i] != G.state[i])
		{
			return false;
		}
	}
	return true;
}

//产生新节点，加入OPEN表
void creatNode(Node& S, Node G){
	int blank;
	for (blank = 0; blank < 9 && S.state[blank] != 0; blank++);
	int x = blank / 3, y = blank % 3; 
	for (int d = 0; d < 4; d++){ 
		int newX = x, newY = y;
		Node tempNode;
		//分别朝四个方向移动空格
		if (d == 0)  newX = x - 1;
		if (d == 1)	 newY = y - 1;
		if (d == 2)  newX = x + 1;
		if (d == 3)	 newY = y + 1;

		int newBlank = newX * 3 + newY; 

		if (newX >= 0 && newX < 3 && newY >= 0 && newY < 3){ 
			tempNode = S;
			tempNode.state[blank] = S.state[newBlank];
			tempNode.state[newBlank] = 0;

			if (S.parent != NULL && (*S.parent).state[newBlank] == 0) {
				continue;
			}
			tempNode.parent = &S;
			tempNode.value = value1(tempNode, G);
			tempNode.depth = S.depth + 1;
			openTable.push(tempNode);
		}
	}
}

int main() {
	Node A, B;
	if (!read(A, B)){
		cout << "两点之间不可达！";
		system("pause");
		return 0;
	}
	clock_t start, finish;
	start = clock();
	openTable.push(A);
	int max = 50000;
	while (max)
	{
		closeTable.push(openTable.top()); 
		openTable.pop(); 
		if (!judge(closeTable.back(), B)) { 
			creatNode(closeTable.back(), B);
		}
		else{
			break;
		}
	}

	Node tempNode;  
	tempNode = closeTable.back();
	while (tempNode.parent != NULL)
	{
		Path.push(tempNode);
		tempNode = *(tempNode.parent);
	}
	Path.push(tempNode);
	cout << "至少要移动" << Path.size() - 1 << "步" << endl;

	while (Path.size() != 0){
		for (int i = 0; i <= 8; i++){
			cout << Path.top().state[i] << " ";
			if ((i + 1) % 3 == 0)
				cout << endl;
		}
		cout <<"当前深度为："<<Path.top().depth << endl;
		cout << "估价值为：" << Path.top().value << endl;
		Path.pop();
		cout << endl;
	}
	finish = clock();
	cout << (finish - start) << "毫秒";
	system("pause");
	return 0;
}

/*尝试编写代码计算扩展节点数、生成节点数*/