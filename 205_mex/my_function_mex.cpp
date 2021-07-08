#include <iostream>
#include <fstream>
#include <iomanip>
#include <queue>
#include <list>
#include <cmath>
#include <limits>
#include <set>
// Libigl includes
#include <igl/C_STR.h>
#include <igl/matlab/mexErrMsgTxt.h>
#include <igl/matlab/MexStream.h>
#include <igl/matlab/parse_rhs.h>
#include <igl/matlab/prepare_lhs.h>
#include <igl/matlab/validate_arg.h>
// ADD ANY INCLUDES YOU NEED HERE:
#include "my_function.h"


void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    using namespace igl;
    using namespace igl::matlab;
    using namespace Eigen;
    igl::matlab::MexStream mout;
    std::streambuf *outbuf = std::cout.rdbuf(&mout);
    
    
    // ONLY EVER TOUCH FROM HERE...
    MatrixXd V,U;
    MatrixXi F,G;
    parse_rhs_double(prhs,V); // this reads the first input argument as a matrix of doubles
    parse_rhs_index(prhs+1,F); // this reads the first input argument as a matrix of indeces (it                               // already shifts from 1-indexing to 0-indexing).
    
    // Now, we call our completely-normal cpp function
    my_function(V,F,U,G);
    

    
    switch(nlhs)
    {
        case 2:
            prepare_lhs_double(G,plhs+1); // this prepares the output G as a matlab vector of doubles 
        case 1:
            prepare_lhs_index(U,plhs+0); // this prepares the output G as a matlab index vector 
        default:break;
    }
    // ... TO HERE
    
    // Do not delete this line:
    std::cout.rdbuf(outbuf);
}
