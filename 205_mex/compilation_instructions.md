# Compilation Instructions for `gptoolbox/mex`

This is a work-in-progress! Bugs get fixed, instructions get expanded, new bugs appear. Please take these instructions the spirit of Heraclitus of Ephesus: πάντα ῥεῖ. Please [email us](mailto:sgsellan@cs.toronto.edu) if you attempt to follow these instructions and run into any problem, or submit a pull request yourself if you know how to fix it! We will be happy to acknowledge you :)

## MacOS

1. Install Homebrew by running in the Mac terminal:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install `boost` by running
```
brew install boost
```
3. Inside `gptoolbox/mex`, run
```
mkdir build
cd build
cmake ..
make
```

A known issue is that sometimes `cmake` has a hard time finding Matlab. You may have to change the `cmake ..` line to give the path to Matlab explicitly:
```
cmake ../ -DMatlab_ROOT_DIR=/path/to/matlab-version/
```

## Linux

To-do

## Windows

*Special thanks to Dr. Rahul Arora for providing these instructions* 

1. Download Visual Studio 2019. In the installer, ensure that you choose the "Desktop development with C++" workload. See https://docs.microsoft.com/en-us/cpp/build/vscpp-step-0-installation?view=msvc-160
This will take a while. You can perform steps 2 to 4 while VS2019 is being downloaded and installed.
2. Download boost from https://www.boost.org/users/download/ and extract it. I'm assuming you're downloading boost 1.74 and extracting to C:/dev/. Please edit the variables below based on the version and location you choose.
Then, set the environment variable `BOOST_ROOT` to `C:\dev\boost_1_74_0`. See this guide to understand how to set environment variables on Windows: https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/. I recommend creating a user variable, instead of a system variable.
3. Download `cmake` from https://cmake.org/download/ and add it to path. That is, add `;C:\Program Files\CMake\bin` to the Path environment variable. If there is no user variable called `Path`, create one and set it to `C:\Program Files\CMake\bin`.
4. Download `git` from https://git-scm.com/downloads and add it to the path. That is, append `;C:\Program Files\Git\cmd` to the `Path` environment variable.
5. Download Intel oneMKL from https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onemkl.html. This requires creating an Intel software development account.
In the installer, choose "Custom Installation" and only select the Math Kernel Library.
Create a new environment variable MKLROOT and set it to `C:\Program Files (x86)\Intel\oneAPI\mkl\latest`
Create a new environment variable MKL_LIB_DIR and set it to `C:\Program Files (x86)\Intel\oneAPI\mkl\latest\lib\intel64`
6. Open up Powershell (`Win+X -> Windows Powershell`). Go to any folder you like using the cd command:
```
cd C:/dev
```
7. Clone gptoolbox:
```
git clone https://github.com/alecjacobson/gptoolbox/
```

8. Configure the gptoolbox mex projects.
```
cd gptoolbox/mex
mkdir build
cd build
cmake ..
```
9. This may result in an error. If yes, delete `FindMATLAB` and try again:
```
rm C:\dev\gptoolbox\mex\external\libigl\external\cgal\Installation\cmake\modules\FindMATLAB.cmake
cmake ..
```
10. Now, build the mex code:
```
cmake --build . --config Release
```
The above step will take a while (up to 30 minutes on a standard laptop). 
11. Copy all executable files to the base folder
```
cd ..
cp ./build/Release/*.mexw64 .
```
12. Also copy the required dependencies:
```
cp C:\dev\gptoolbox\mex\external\libigl\external\gmp\lib\libgmp-10.dll .
cp C:\dev\gptoolbox\mex\external\libigl\external\mpfr\lib\libmpfr-4.dll .
```
13. Open MATLAB and set up mex. Note that the following commands should be typed in MATLAB, not on Powershell.
```
mex -setup
mex -setup C++
```
14. Now, try running a simple program. If MATLAB doesn't crash, you're good to go. Note that the following should be typed in MATLAB, not on Powershell.
```
cd /dev/gptoolbox/mex
[VT, FT] = wire_mesh([0 0 0; 1 1 1], [1 2], 'PolySize', 6, 'Thickness', 2e-3, 'Solid', false);
```
