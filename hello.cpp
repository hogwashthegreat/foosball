#include <iostream>
#include <string>
#include <vector>
#include <math.h>
using std::vector;

vector<double> getInput(){
    vector<double> points(4,0);
    std::cout << "x1: ";
    std::cin >> points[0];
    std::cout << "y1: ";
    std::cin >> points[1];
    std::cout << "x2: ";
    std::cin >> points[2];
    std::cout << "y2: ";
    std::cin >> points[3];
    return points;
}



int main(){
    vector<double> points = getInput();
    for (double x : points){
        std::cout << x << ", ";
    }
    double amp = ((double)points[1]-points[3])/2;
    std::cout << "\nsin or cos: ";
    std::string choice;
    std::cin >> choice;
    if(choice.compare("cos") == 0){
        std::cout << amp << "cos(" << "(pi/" << (points[2]-points[0]) << ")(" << "x-" << points[0] << ")) + " << points[1]-amp;
    }
    
    else{
        double pointy = ((double)points[1]+points[3])/2;
        double pointx = ((double)points[0]+points[2])/2;
        std::cout << pointy << "\n";
        std::cout << points[3] - pointy<< "sin(" << "(pi/" << 2*(points[2]-pointx) << ")(" << "x-" << pointx << ")) + " << pointy;
    }
}
