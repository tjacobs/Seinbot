#!/bin/bash
 
source activate tom

face_recognition known_people/ unknown_people/

jupyter notebook Seinbot.ipynb 
