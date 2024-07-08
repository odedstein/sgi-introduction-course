# Parameterization Exercises

To access the Python notebook, you will need [jupyter notebook](https://jupyter.org/install) installed. You can install it by calling
```bash
pip install notebook
```
or if you have conda
```bash
conda install notebook -c conda-forge
```
Once installed, make sure you are in the same directory as this README in the terminal, and launch the notebook server using
```bash
jupyter notebook
```

Exercise 102 consists of the Python notebook [102_parameterization_exercises.ipynb](102_parameterization_exercises.ipynb), in which you will reproduce the analyses done in exercise 101 with more complex meshes, as well as try your hand at more advanced parameterization methods.

You can spot-check your calculations by referring to the saved .npy files containing the correct parameterization values for the Tutte, mean value, LSCM, and ARAP parameterizations for the two meshes (./solution/x_tutte.npy, ./solution/x_meanvalue.npy, ./solution/x_lscm.npy, ./solution/x_arap.npy respectively.)

Below are screenshots of the parameterizations, which can also use to visually debug your calculations.

#### halfbunny.obj

*Tutte*
![halfbunny_lscm](./solution/halfbunny_tutte.png)

*Mean Value*
![halfbunny_meanvalue](./solution/halfbunny_meanvalue.png)

*LSCM*
![halfbunny_lscm](./solution/halfbunny_lscm.png)

*ARAP*
![ogre_arap](./solution/halfbunny_arap.png)

#### ogre.obj
*Tutte*
![ogre_lscm](./solution/ogre_tutte.png)

*Mean Value*
![ogre_meanvalue](./solution/ogre_meanvalue.png)

*LSCM*
![ogre_lscm](./solution/ogre_lscm.png)

*ARAP*
![ogre_arap](./solution/ogre_arap.png)
