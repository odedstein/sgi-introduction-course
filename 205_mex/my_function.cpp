#include "my_function.h"
#include <iostream>
#include <Eigen/Core>
using namespace std;

void my_function(Eigen::MatrixXd & V,Eigen::MatrixXi & F, Eigen::MatrixXd & U, Eigen::MatrixXi & G){
    
    // This is where your real functionality should be, if you're being principled
    U = V;
    G = F;
    
}

