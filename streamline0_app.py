import streamlit as st
import pandas as pd
import numpy as np
import re

#####################################
# 1) Reference Data for Kidney
#####################################

# Kidney main data (number, tumor mass dimensions, RENAL score, and histology)
kidney_main_data = [
    {"number": 1, "size_mass": "1,9 x 2,1 x 2,8", "RENAL_score": "7P", "histology": "Clear Cell"},
    {"number": 2, "size_mass": "1 x 1,7 x 1,3", "RENAL_score": "6x", "histology": "Clear Cell"},
    {"number": 3, "size_mass": "2,1 x 2,5 x 2,8", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 4, "size_mass": "2 x 2,8 x 2,8", "RENAL_score": "4x", "histology": "Clear Cell"},
    {"number": 5, "size_mass": "1,6 x 1,2 x 1,8", "RENAL_score": "7p", "histology": "Clear Cell"},
    {"number": 6, "size_mass": "2,9 x 2,6 x 2,8", "RENAL_score": "5a", "histology": "Clear Cell"},
    {"number": 7, "size_mass": "2,9 x 2,6 x 3 (1,9 x 2,2 x 3)", "RENAL_score": "6x", "histology": "Clear Cell"},
    {"number": 8, "size_mass": "3,5 x 3,4 x 3,9", "RENAL_score": "4x", "histology": "Clear Cell"},
    {"number": 9, "size_mass": "2,1 x 1,9 x 1,9", "RENAL_score": "5a", "histology": "Clear Cell"},
    {"number": 10, "size_mass": "2,3 x 2 x 2,1", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 11, "size_mass": "2,9 x 3,3 x 3,1", "RENAL_score": "5x", "histology": "Clear Cell"},
    {"number": 12, "size_mass": "3,6 x 3,5 x 3,7", "RENAL_score": "5x", "histology": "Clear Cell"},
    {"number": 13, "size_mass": "3,6 x 3,8 x 2,8", "RENAL_score": "7ph", "histology": "Clear Cell"},
    {"number": 14, "size_mass": "3,2 x 3,4 x 3,1", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 15, "size_mass": "3 x 2,8 x 2,7", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 16, "size_mass": "2,8 x 2,4 x 2", "RENAL_score": "6x", "histology": "Clear Cell"},
    {"number": 17, "size_mass": "1,7 x 1,6 x 1,8", "RENAL_score": "5a", "histology": "Clear Cell"},
    {"number": 18, "size_mass": "2,6 x 2,5 x 2,6", "RENAL_score": "7xh", "histology": "Clear Cell"},
    {"number": 19, "size_mass": "5,8 x 4,3 x 6,2", "RENAL_score": "5x", "histology": "Clear Cell"},
    {"number": 20, "size_mass": "2,9 x 3,2 x 2,6", "RENAL_score": "6x", "histology": "Clear Cell"},
    {"number": 21, "size_mass": "1,4 x 1,4 x 1,5", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 22, "size_mass": "2,6 x 2,3 x 2,1", "RENAL_score": "7ph", "histology": "Clear Cell"},
    {"number": 23, "size_mass": "2 x 1,8 x 1,9", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 24, "size_mass": "3,2 x 2,9 x 3,2", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 25, "size_mass": "3,1 x 2,9 x 2,8", "RENAL_score": "6a", "histology": "Clear Cell"},
    {"number": 26, "size_mass": "1,9 x 1,6 x 1,6", "RENAL_score": "6x", "histology": "Clear Cell"},
    {"number": 27, "size_mass": "2 x 2,5 x 2,3", "RENAL_score": "7p", "histology": "Clear Cell"},
    {"number": 28, "size_mass": "2,4 x 2,6 x 2", "RENAL_score": "6a", "histology": "Clear Cell"},
    {"number": 29, "size_mass": "3,6 x 3,7 x 4,3", "RENAL_score": "10a", "histology": "Clear Cell"},
    {"number": 30, "size_mass": "1,8 x 2 x 2,1", "RENAL_score": "4x", "histology": "Clear Cell"},
    {"number": 31, "size_mass": "2,2 x 2,5 x 2,4", "RENAL_score": "4x", "histology": "Clear Cell"},
    {"number": 32, "size_mass": "2,5 x 2,1 x 2,2", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 33, "size_mass": "19 x 19 x 2,1", "RENAL_score": "4x", "histology": "Clear Cell"},
    {"number": 34, "size_mass": "2,6 x 2,5 x 2,1", "RENAL_score": "4a", "histology": "Clear Cell"},
    {"number": 35, "size_mass": "4,6 x 3,8 x 4,8", "RENAL_score": "8x", "histology": "Clear Cell"},
    {"number": 36, "size_mass": "2,6 x 1,9 x 2,2", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 37, "size_mass": "4,2 x 3,6 x 4,6", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 38, "size_mass": "3,1 x 2,5 x 4,8", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 39, "size_mass": "3,1 x 3,9 x 3,4", "RENAL_score": "4x", "histology": "Clear Cell"},
    {"number": 40, "size_mass": "2,5 x 2,7 x 2,8", "RENAL_score": "5x", "histology": "Clear Cell"},
    {"number": 41, "size_mass": "3,4 x 3,5 x 2,9", "RENAL_score": "6p", "histology": "Clear Cell"},
    {"number": 42, "size_mass": "3,7 x 3,5 x 3,4", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 43, "size_mass": "1,7 x 1,9 x 2", "RENAL_score": "5a", "histology": "Clear Cell"},
    {"number": 44, "size_mass": "3,7 x 3,5 x 4", "RENAL_score": "4a", "histology": "Clear Cell"},
    {"number": 45, "size_mass": "2,4 x 2,0 x 2,6", "RENAL_score": "4p", "histology": "Clear Cell"},
    {"number": 46, "size_mass": "2,6 x 2,3 x 2,1", "RENAL_score": "7ah", "histology": "Clear Cell"},
    {"number": 47, "size_mass": "2,9 x 2,7 x 2,7", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 48, "size_mass": "3,2 x 2,5 x 3,7", "RENAL_score": "4ah", "histology": "Clear Cell"},
    {"number": 49, "size_mass": "2,9 x 2,8 x 2,9", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 50, "size_mass": "3,7 x 3,2 x 3,5", "RENAL_score": "5a", "histology": "Clear Cell"},
    {"number": 51, "size_mass": "2 x 2,2 x 1,9", "RENAL_score": "4a", "histology": "Clear Cell"},
    {"number": 52, "size_mass": "2,8 x 2,7 x 2", "RENAL_score": "5p", "histology": "Clear Cell"},
    {"number": 53, "size_mass": "2 x 1 x 2", "RENAL_score": "5p", "histology": "Clear Cell"}
]
df_main_kidney = pd.DataFrame(kidney_main_data)

# Kidney cryoablation results table for kidney (numbered 1 to 54; we use only rows 1-53)
cryo_data_kidney = [
    {"number": 1, "cryoprobes": "3 rod", "types_of_probes": "ROD", "size_Ice_ball": "2,7x1,9x3,2", "protection": "NO", "complications": "NONE"},
    {"number": 2, "cryoprobes": "1", "types_of_probes": "", "size_Ice_ball": "1,4 x 2,6 x 2,8 or 1,7", "protection": "YES/COLON SPLEEN", "complications": "NONE"},
    {"number": 3, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "2,8 x 2,7 x 3,5", "protection": "NONE", "complications": "NONE"},
    {"number": 4, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "3 x 3,6 x 2", "protection": "NONE", "complications": "PNEUMOTH"},
    {"number": 5, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "2,7 x 2,4 x 2,8", "protection": "NONE", "complications": "NONE"},
    {"number": 6, "cryoprobes": "2", "types_of_probes": "", "size_Ice_ball": "2,9 x 3 x 4,2", "protection": "YES/SPLEEN", "complications": ""},
    {"number": 7, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3 x 3,8 x 3,4", "protection": "NO", "complications": "MILD HEMORRHAGE?"},
    {"number": 8, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,8 x 5,2 x 4,9", "protection": "YES/PSOAS", "complications": "none"},
    {"number": 9, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,2 x 3,4 x 3", "protection": "NO", "complications": "NONE"},
    {"number": 10, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,7 x 2,4 x 3,2", "protection": "NO", "complications": "NONE"},
    {"number": 11, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "4,2 x 3,6 x 4,1", "protection": "NO", "complications": "NONE"},
    {"number": 12, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,8 x 4,2 x 4,9", "protection": "YES/COLON", "complications": "MILD HEMORRHAGE?"},
    {"number": 13, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 3,6 x 3,3", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 14, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 3,2 x 3,6", "protection": "YES/COLON", "complications": "MILD HEMORRHAGE?"},
    {"number": 15, "cryoprobes": "3", "types_of_probes": "2ROD+1SPHERE", "size_Ice_ball": "3,6 x 2,9 x 3,4", "protection": "NO", "complications": "NONE?"},
    {"number": 16, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "2,7 x 3,7 x 3,5", "protection": "YES/COLON", "complications": ""},
    {"number": 17, "cryoprobes": "1", "types_of_probes": "SPHERE", "size_Ice_ball": "1,2 x 1,8 x 2", "protection": "YES/PSOAS", "complications": ""},
    {"number": 18, "cryoprobes": "3", "types_of_probes": "4SPHERE", "size_Ice_ball": "3,5 x 3,3 x 3,8", "protection": "COLON/SPLEEN", "complications": "none"},
    {"number": 19, "cryoprobes": "5", "types_of_probes": "4FORCE+1ROD", "size_Ice_ball": "5,5 x 5,7 x 6,5", "protection": "YES/COLON/SPLEEN", "complications": "none"},
    {"number": 20, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 4,8 x 4", "protection": "HYDRO/COLON", "complications": "none"},
    {"number": 21, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,1 x 2,9 x 2,7", "protection": "NO", "complications": "MILD HEMORRHAGE"},
    {"number": 22, "cryoprobes": "3", "types_of_probes": "2ROD+1SPHERE", "size_Ice_ball": "2,6 x 4,4 x 3,5", "protection": "YES/LIVER/COLON", "complications": "NONE"},
    {"number": 23, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,1 x 2,5 x 3", "protection": "NO", "complications": "NONE"},
    {"number": 24, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 4,7 x 5", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 25, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,2 x 4 x 4", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 26, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3 x 2,5 x 2,8", "protection": "NO", "complications": "NONE"},
    {"number": 27, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,4 x 3,3 x 3", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 28, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "4 x 2,4 x 3,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 29, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "5,2 x 4 x 4,8", "protection": "YES/SPLEEN", "complications": "MILD HEMORRHAGE"},
    {"number": 30, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,7 x 3,3 x 2,8", "protection": "NO", "complications": "NONE"},
    {"number": 31, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "2,9 x 3,3 x 2,9", "protection": "YES/PSOAS,RENAL VEIN", "complications": "NONE"},
    {"number": 32, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,7 x 3,4 x 2,7", "protection": "YES/SPLEEN", "complications": "NONE"},
    {"number": 33, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3 x 3,6 x 3,8", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 34, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,1 x 2,7 x 2,4", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 35, "cryoprobes": "4", "types_of_probes": "FORCE", "size_Ice_ball": "5,2 x 4,1 x 4,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 36, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "2,6 x 2,2 x 2,1", "protection": "YES/PSOAS", "complications": "NONE"},
    {"number": 37, "cryoprobes": "3", "types_of_probes": "FORCE", "size_Ice_ball": "5,2 x 4,2 x 4,8", "protection": "YES/PSOAS", "complications": "HEMORRHAGE- νοσηλεία"},
    {"number": 38, "cryoprobes": "3", "types_of_probes": "FORCE", "size_Ice_ball": "", "protection": "", "complications": ""},
    {"number": 39, "cryoprobes": "4", "types_of_probes": "FORCE", "size_Ice_ball": "5,0 x 3,5 x 5,3", "protection": "YES/COLON, PSOAS", "complications": "NONE"},
    {"number": 40, "cryoprobes": "2", "types_of_probes": "FORCE", "size_Ice_ball": "3,5 x 4,1 x 4,3", "protection": "YES/ COLON", "complications": "MILD HEMORRHAGE"},
    {"number": 41, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "3 x 4,1 x 2,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 42, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "5,5 x 5,5 x 4,6", "protection": "NO", "complications": "MILD HEMORRHAGE"},
    {"number": 43, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "4,2 x 3,9 x 5,4", "protection": "YES/ COLON, PSOAS", "complications": "NONE"},
    {"number": 44, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,4 x 2,6 x 3,1", "protection": "YES/COLON", "complications": "HEMORRHAGE ΜΕΓΑΛΗ"},
    {"number": 45, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,8 x 5,3 x 6,5", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 46, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "3,2 x 3,7 x 3,6", "protection": "YES/PSOAS", "complications": "MILD HEMORRHAGE"},
    {"number": 47, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,8 x 2,8 x 2,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 48, "cryoprobes": "4", "types_of_probes": "SPHERE", "size_Ice_ball": "4,6 x 3,6 x 3,6", "protection": "YES/LIVER,COLON", "complications": "NONE"},
    {"number": 49, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "4,2 x 3,1 x 3,6", "protection": "YES/LIVER,COLON", "complications": "NONE"},
    {"number": 50, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "3,6 x 3 x 3,5", "protection": "YES/SPLEEN,COLON", "complications": "NONE"},
    {"number": 51, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "4,1 x 4 x 5,2", "protection": "YES/COLON", "complications": "SUBCUTANEUS HEMATOMA / MILD HEMORRHAGE"},
    {"number": 52, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "2,7 x 2,9 x 2,6", "protection": "YES/ COLON", "complications": "NONE"},
    {"number": 53, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "4,7 x 3,6 x 3,5", "protection": "YES/ COLON", "complications": "NONE"}
]
df_cryo_kidney = pd.DataFrame(cryo_data_kidney)

# Only use rows 1-53 (drop extra if any)
df_cryo_kidney = df_cryo_kidney[df_cryo_kidney["number"] <= 53]

# Merge kidney data on "number"
df_main_kidney.set_index("number", inplace=True)
df_cryo_kidney.set_index("number", inplace=True)
df_kidney_merged = pd.merge(df_main_kidney, df_cryo_kidney, left_index=True, right_index=True)

#####################################
# 2) Reference Data for Lung
#####################################

lung_main_data = [
    {"index_l": 1, "type_lesion": "NSCLC", "age": 82, "side": "R", "size_lung": "1,3x2,1x2,3"},
    {"index_l": 2, "type_lesion": "NSCLC", "age": 87, "side": "R", "size_lung": "1,5x1,4x2,1"},
    {"index_l": 3, "type_lesion": "NSCLC", "age": 83, "side": "R", "size_lung": "3,5x3,4x2,1"},
    {"index_l": 4, "type_lesion": "NSCLC", "age": 69, "side": "R", "size_lung": "2x1,7x2"},
    {"index_l": 5, "type_lesion": "NSCLC", "age": 83, "side": "L", "size_lung": "1,9x1,8x2,2"},
    {"index_l": 6, "type_lesion": "META-COLORECTAL", "age": 65, "side": "R", "size_lung": "1,5x1,3x1,1"},
    {"index_l": 7, "type_lesion": "META-COLORECTAL", "age": 63, "side": "L", "size_lung": "3,7x3,3x2,8"},
    {"index_l": 8, "type_lesion": "NSCLC", "age": 80, "side": "R", "size_lung": "2,3x1,9x1,9"},
    {"index_l": 9, "type_lesion": "META-COLORECTAL", "age": 58, "side": "R", "size_lung": "1,1x1x0,9"},
    {"index_l": 10, "type_lesion": "NSCLC", "age": 69, "side": "L", "size_lung": "1,2x1,6x1"},
    {"index_l": 11, "type_lesion": "NSCLC", "age": 72, "side": "L", "size_lung": "1,1x0,8x0,6"},
    {"index_l": 12, "type_lesion": "NSCLC", "age": 71, "side": "L", "size_lung": "1,6x1,1x1,6"},
    {"index_l": 13, "type_lesion": "NSCLC", "age": 79, "side": "L", "size_lung": "4,6x3,2x3,9"},
    {"index_l": 14, "type_lesion": "META-COLORECTAL", "age": 64, "side": "R", "size_lung": "2,1x2x1x5"},
    {"index_l": 15, "type_lesion": "META-COLORECTAL", "age": 64, "side": "L", "size_lung": "1,4x1,3x1,3"},
    {"index_l": 16, "type_lesion": "META-COLORECTAL", "age": 64, "side": None, "size_lung": "2,5x2,1x1,5"},
    {"index_l": 17, "type_lesion": "NSCLC", "age": 69, "side": "L", "size_lung": "3,1x1,8x3"},
    {"index_l": 18, "type_lesion": "NSCLC", "age": 76, "side": "R", "size_lung": "2,2x2,6x1,8"},
    {"index_l": 19, "type_lesion": "NSCLC", "age": 75, "side": "R", "size_lung": "2,7x1,6x2,9"},
    {"index_l": 20, "type_lesion": "NSCLC", "age": 77, "side": "L", "size_lung": "2,2x1,8x1,6"},
    {"index_l": 21, "type_lesion": "META-COLORECTAL", "age": 74, "side": "R", "size_lung": "4,2x4x3,6"},
    {"index_l": 22, "type_lesion": "NSCLC", "age": 82, "side": "L", "size_lung": "1,9x1,3x1,5"},
    {"index_l": 23, "type_lesion": "NSCLC", "age": 82, "side": "R", "size_lung": "1,6x1,9x2,2"},
    {"index_l": 24, "type_lesion": "META-COLORECTAL", "age": 74, "side": "R", "size_lung": "1x0,9x0,8"},
    {"index_l": 25, "type_lesion": "NSCLC", "age": 71, "side": "R", "size_lung": "1,4x1,1x1,1"},
    {"index_l": 26, "type_lesion": "NSCLC", "age": 78, "side": "L", "size_lung": "1,3x1,1x1,2"},
    {"index_l": 27, "type_lesion": "META-COLORECTAL", "age": 63, "side": "L", "size_lung": "4,5"},
    {"index_l": 28, "type_lesion": "NSCLC", "age": 51, "side": "L", "size_lung": "1,2x0,8x1"},
    {"index_l": 29, "type_lesion": "META-COLORECTAL", "age": 63, "side": "R", "size_lung": "4,5"},
    {"index_l": 30, "type_lesion": "NSCLC", "age": 68, "side": "R", "size_lung": "1,1x1,2x1"},
    {"index_l": 31, "type_lesion": "NSCLC", "age": 81, "side": "R", "size_lung": "2χ1,2x1,3"},
    {"index_l": 32, "type_lesion": "NSCLC", "age": 70, "side": "R", "size_lung": "2,1x2x1,7"},
    {"index_l": 33, "type_lesion": "META-COLORECTAL", "age": None, "side": "R", "size_lung": "1,3x1,3x1,2"},
    {"index_l": 34, "type_lesion": "META-COLORECTAL", "age": 70, "side": "R", "size_lung": "2,4"},
    {"index_l": 35, "type_lesion": "META-COLORECTAL", "age": 48, "side": "L", "size_lung": "1,2x1,1x0,9"},
    {"index_l": 36, "type_lesion": "NSCLC", "age": 78, "side": "R", "size_lung": "1,7x1,7x1,8"},
    {"index_l": 37, "type_lesion": "NSCLC", "age": 64, "side": "L", "size_lung": "1,5x1x0,8"},
    {"index_l": 38, "type_lesion": "MESOTHELIOMA", "age": 65, "side": "R", "size_lung": "2x1,4x1,7"},
    {"index_l": 39, "type_lesion": "NSCLC", "age": 71, "side": "L", "size_lung": "0,8x1x0,8"},
    {"index_l": 40, "type_lesion": "NSCLC", "age": 83, "side": "R", "size_lung": "1,4x1,8x1,5"},
    {"index_l": 41, "type_lesion": "NSCLC", "age": 83, "side": "R", "size_lung": "2,2x2,8x2,8"},
    {"index_l": 42, "type_lesion": "NSCLC", "age": 76, "side": "L", "size_lung": "1,4x0,9x1,3"},
    {"index_l": 43, "type_lesion": "META-COLORECTAL", "age": 71, "side": "R", "size_lung": "3,7x2,7x2,9"},
    {"index_l": 44, "type_lesion": "META-COLORECTAL", "age": 73, "side": "R", "size_lung": "2,1x0,8x0,8"},
    {"index_l": 45, "type_lesion": "NSCLC", "age": 70, "side": "L", "size_lung": "1,3x1,1x1,2"},
    {"index_l": 46, "type_lesion": "NSCLC", "age": 84, "side": "L", "size_lung": "2,5x1,8x3"},
    {"index_l": 47, "type_lesion": "NSCLC", "age": 78, "side": "R", "size_lung": "3,2x2,1x2,8"},
    {"index_l": 48, "type_lesion": "NSCLC", "age": 82, "side": "L", "size_lung": "3,2x2,5x3"},
    {"index_l": 49, "type_lesion": "META-COLORECTAL", "age": 73, "side": "R", "size_lung": "1,5x1,2x1"},
    {"index_l": 50, "type_lesion": "META-COLORECTAL", "age": 73, "side": "L", "size_lung": "1,5x1,9x1,8"},
    {"index_l": 51, "type_lesion": "NSCLC", "age": 73, "side": "L", "size_lung": "1,2x0,8x1,3"},
    {"index_l": 52, "type_lesion": "NSCLC", "age": 73, "side": "R", "size_lung": "1,3x1,2x1,4"},
    {"index_l": 53, "type_lesion": "META-COLORECTAL", "age": 73, "side": "R", "size_lung": "0,9x0,9x1 + 0,7x0,7x0,6"},
    {"index_l": 54, "type_lesion": "NSCLC", "age": 78, "side": "R", "size_lung": "1x0,8x0,6"},
    {"index_l": 55, "type_lesion": "?", "age": 73, "side": "M", "size_lung": "1,9x1,4x1,8"},
    {"index_l": 56, "type_lesion": "NSCLC", "age": 73, "side": "R", "size_lung": "1,2x1,5x1"},
    {"index_l": 57, "type_lesion": "NSCLC", "age": 79, "side": "L", "size_lung": "2,4x1,7x2,1"},
    {"index_l": 58, "type_lesion": "NSCLC", "age": 69, "side": "R", "size_lung": "2x2x1,8"},
    {"index_l": 59, "type_lesion": "NSCLC", "age": 81, "side": "R", "size_lung": "3,1x4x3,3"},
    {"index_l": 60, "type_lesion": "META-COLORECTAL", "age": 73, "side": "R", "size_lung": "3,4X21X16"},
    {"index_l": 61, "type_lesion": "NSCLC", "age": 72, "side": "L", "size_lung": "1,2Χ1Χ1"},
    {"index_l": 62, "type_lesion": "NSCLC", "age": 60, "side": "L", "size_lung": "1,1X1,1X1,3"},
    {"index_l": 63, "type_lesion": "NSCLC", "age": 80, "side": "L", "size_lung": "2x1,3x2,2"},
    {"index_l": 64, "type_lesion": "META-COLORECTAL", "age": 70, "side": "L", "size_lung": "1,1Χ1,2Χ1,3"},
    {"index_l": 65, "type_lesion": "NSCLC", "age": 61, "side": "L", "size_lung": "1,7x1x1,7"},
    {"index_l": 66, "type_lesion": "NSCLC+RCC", "age": 76, "side": "R", "size_lung": "2,4x1,8x1,9"},
    {"index_l": 67, "type_lesion": "META-RCC", "age": 73, "side": "L", "size_lung": "2,3x2x1,9"},
    {"index_l": 68, "type_lesion": "NSCLC", "age": 65, "side": "L", "size_lung": "1,1x0,8x0,9"},
    {"index_l": 69, "type_lesion": "META-COLORECTAL", "age": 82, "side": "R", "size_lung": "3,9x2,4x3,8"},
    {"index_l": 70, "type_lesion": "META-COLORECTAL", "age": 67, "side": "L", "size_lung": "2x2x2,2"},
    {"index_l": 71, "type_lesion": "NSCLC", "age": 77, "side": "R", "size_lung": "2x1,8x1,8"},
    {"index_l": 72, "type_lesion": "NSCLC", "age": 67, "side": "R", "size_lung": "3,1x3,6x2,5"},
    {"index_l": 73, "type_lesion": "NSCLC", "age": 74, "side": "R", "size_lung": "2,5x1,8x1,4"},
    {"index_l": 74, "type_lesion": "?", "age": None, "side": None, "size_lung": "1,3x1,1x0,9"},
    {"index_l": 75, "type_lesion": "NSCLC", "age": 66, "side": "L", "size_lung": "1,9x1,5x1,7"}
]
df_main_lung = pd.DataFrame(lung_main_data)

# Lung cryo data (numbered 1 to 55; use only rows with complete data, here we use a sample)
lung_cryo_data = [
    {
        "index_l": 1,
        "types_of_probes": "ROD",
        "size_Ice_ball": "3,3x4,8x4,4",
        "freeze_time": 30,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 2,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,6x2x3x2",
        "freeze_time": 30,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 3,
        "types_of_probes": "ROD",
        "size_Ice_ball": "3,2x4,2x4",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 4,
        "types_of_probes": "SPHERE",  
        "size_Ice_ball": "3,7x3x3,2",
        "freeze_time": 27,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 5,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,2x3,6x2,8",
        "freeze_time": 24,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 6,
        "types_of_probes": "SPEHRE",
        "size_Ice_ball": "3,2x3x2,4",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 7,
        "types_of_probes": "ROD",
        "size_Ice_ball": "4,3x4,1x3,7",
        "freeze_time": 20,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 8,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "4,2x3,3x2,6",
        "freeze_time": 23,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 9,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3x2,5x1,9",
        "freeze_time": 20,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 10,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "1,9x2,9x2,3",
        "freeze_time": 15,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 11,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,1x3,1x2,3",
        "freeze_time": 15,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 12,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "1,7x1,5x1,6",
        "freeze_time": 15,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 13,
        "types_of_probes": "ROD",
        "size_Ice_ball": "3,7x4,9x3,7",
        "freeze_time": 15,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 14,
        "types_of_probes": "ROD",
        "size_Ice_ball": "4,1x3,3x2,8",
        "freeze_time": 14,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 15,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,9x2,7x2x6",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 16,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,7x3,6x3,3",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 17,
        "types_of_probes": "ROD",
        "size_Ice_ball": "2,7x5x3,7",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 18,
        "types_of_probes": "ROD",
        "size_Ice_ball": "2,8x2,6x2,5",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 19,
        "types_of_probes": "ROD",
        "size_Ice_ball": "4,2x2,8x3,2",
        "freeze_time": 14,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 20,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "4,2x2,3x2,6",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 21,
        "types_of_probes": "2 SPHERE+2 ROD",
        "size_Ice_ball": "4,4x4,3x3x8",
        "freeze_time": 8,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 22,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,6x2,1x1,8",
        "freeze_time": 7,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 23,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,8x2,1x2,6",
        "freeze_time": None,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 24,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,5x1,6x1,4",
        "freeze_time": 2,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 25,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "1,7x1,8x2",
        "freeze_time": 3,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 26,
        "types_of_probes": "ROD",
        "size_Ice_ball": "4,5x3,3x3,3",
        "freeze_time": 6,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 27,
        "types_of_probes": "ROD",
        "size_Ice_ball": None,
        "freeze_time": 5,
        "protection": "not",
        "notes": None
    },
    {
        "index_l": 28,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,6x3,9x1,9",
        "freeze_time": 2,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 29,
        "types_of_probes": "ROD",
        "size_Ice_ball": None,
        "freeze_time": None,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 30,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,4x3,1x2,8",
        "freeze_time": 12,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 31,
        "types_of_probes": "ROD",
        "size_Ice_ball": "2.4χ3.5x1,3",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 32,
        "types_of_probes": "ROD",
        "size_Ice_ball": "2,5x4,1x2,1",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 33,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,3x3,4x1,8",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 34,
        "types_of_probes": "2 ROD+1 SPHERE",
        "size_Ice_ball": None,
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 35,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,4x2,8x2x6",
        "freeze_time": None,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 36,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,2x1,9x2,2",
        "freeze_time": None,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 37,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "1,7x2,8x2",
        "freeze_time": 15,
        "protection": "NOT",
        "notes": None
    },
    {
        "index_l": 38,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,9χ2,2χ2,3",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 39,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,2x3x2",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 40,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,2x2,2x2",
        "freeze_time": None,
        "protection": None,
        "notes": "ΝΑ ΜΗ ΣΥΜΠΕΡΙΛΗΦΘΕΙ"
    },
    {
        "index_l": 41,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,6x2,7x2x9",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 42,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,4x1,7x1,8",
        "freeze_time": None,
        "protection": None,
        "notes": "impax 3m"
    },
    {
        "index_l": 43,
        "types_of_probes": "3 SPHERE+2 ROD",
        "size_Ice_ball": "5x5,8x3,6",
        "freeze_time": None,
        "protection": None,
        "notes": "DISSECTION PARASPINAL."
    },
    {
        "index_l": 2,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,9x2,5x2,6",
        "freeze_time": None,
        "protection": None,
        "notes": "1m κεντρική εμπλουτιζόμενη περιοχή - τοπική υποτροπή."
    },
    {
        "index_l": 44,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,1x1,6x1,9",
        "freeze_time": None,
        "protection": None,
        "notes": "3m χωρίς υποτροπή???"
    },
    {
        "index_l": 45,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,5x3,5x3,6",
        "freeze_time": None,
        "protection": None,
        "notes": "3m χωρίς υποτροπή. Όχι άλλο έλεγχο impax"
    },
    {
        "index_l": 46,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "4,8x2,2x2,2",
        "freeze_time": None,
        "protection": None,
        "notes": "1m χωρίς υποτροπή. Όχι άλλο έλεγχο impax"
    },
    {
        "index_l": 47,
        "types_of_probes": "2 SPHERE+2 ROD",
        "size_Ice_ball": "3,4x2,9x3,3",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρις follow up impax"
    },
    {
        "index_l": 48,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,5x2,5x1,4",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 49,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,8x1,7x2,4",
        "freeze_time": None,
        "protection": None,
        "notes": "6m χωρίς υποτροπή??"
    },
    {
        "index_l": 50,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3x2,2x1,9",
        "freeze_time": None,
        "protection": None,
        "notes": "7m χωρίς υποτροπή."
    },
    {
        "index_l": 51,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,6x3,5x1,9",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρις follow up impax"
    },
    {
        "index_l": 52,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,8x2x1,3 και 1,8x3,3xx1,9",
        "freeze_time": None,
        "protection": None,
        "notes": "1m όλα υποτροπή???"
    },
    {
        "index_l": 53,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "1,7x1,8x1,5",
        "freeze_time": None,
        "protection": None,
        "notes": "3m χωρίς υποτροπή. Όχι άλλο έλεγχο impax"
    },
    {
        "index_l": 54,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,1x1,9x2,2",
        "freeze_time": None,
        "protection": None,
        "notes": "4m χωρίς υποτροπή. Όχι άλλο έλεγχο"
    },
    {
        "index_l": 55,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,7x3,2x1,9",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρις follow up impax"
    },
    {
        "index_l": 56,
        "types_of_probes": "ROD",
        "size_Ice_ball": "2,8x2x1,9",
        "freeze_time": None,
        "protection": None,
        "notes": "1m χωρίς υποτροπή"
    },
    {
        "index_l": 57,
        "types_of_probes": "3 SPHERE+1 ROD",
        "size_Ice_ball": "3x5,3x3,4",
        "freeze_time": None,
        "protection": None,
        "notes": "υπολειπόμενη νόσος περιφερικός όζος. Χωρίς follow up"
    },
    {
        "index_l": 58,
        "types_of_probes": "3 SPHERE+2 ROD",
        "size_Ice_ball": "5,1x2,8x4",
        "freeze_time": None,
        "protection": None,
        "notes": "πρόοδος νόσου στους 4m"
    },
    {
        "index_l": 59,
        "types_of_probes": "ROD",
        "size_Ice_ball": "4X2,4X2,4",
        "freeze_time": None,
        "protection": "not",
        "notes": "6m χωρίς υποτροπή"
    },
    {
        "index_l": 60,
        "types_of_probes": "ROD",
        "size_Ice_ball": "1,9Χ1,8Χ2",
        "freeze_time": None,
        "protection": "not",
        "notes": "4m χωρίς τοπική υποτροπή, Νέα μάζα στην ΑΡ πύλη. Συστηματική θεραπεία"
    },
    {
        "index_l": 61,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "1,5X1,9X1,8",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρίς επανέλεγχο"
    },
    {
        "index_l": 62,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,3x3,2x2,6",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρίς επανέλεγχο"
    },
    {
        "index_l": 63,
        "types_of_probes": "2 SPHERE",
        "size_Ice_ball": "2,4Χ2,6Χ2,3",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρίς επανέλεγχο"
    },
    {
        "index_l": 64,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,6x2,4x2,2",
        "freeze_time": None,
        "protection": None,
        "notes": "6m χωρίς υποτροπή"
    },
    {
        "index_l": 65,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,5x3,3x2,5",
        "freeze_time": None,
        "protection": None,
        "notes": "1m χωρίς υποτροπή"
    },
    {
        "index_l": 66,
        "types_of_probes": "ROD",
        "size_Ice_ball": "4,2x2,8x2,2",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρίς επανέλεγχο"
    },
    {
        "index_l": 67,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2x2,8x1,6",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρίς επανέλεγχο"
    },
    {
        "index_l": 68,
        "types_of_probes": "4ROD+1SPHERE",
        "size_Ice_ball": "5x4,5x4,1",
        "freeze_time": None,
        "protection": None,
        "notes": "χωρίς επανέλεγχο impax"
    },
    {
        "index_l": 69,
        "types_of_probes": "ROD",
        "size_Ice_ball": "3,7x4,4x2,6",
        "freeze_time": None,
        "protection": None,
        "notes": "1m χωρίς υποτροπή"
    },
    {
        "index_l": 70,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,7x2,9x3,3",
        "freeze_time": None,
        "protection": None,
        "notes": "1m χωρίς υποτροπή"
    },
    {
        "index_l": 71,
        "types_of_probes": "3ROD",
        "size_Ice_ball": "4,7x3,9x3,7",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 72,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,8x3,6x3,5",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 73,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "2,3x2,3x1,9",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 74,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,6x2,9x2",
        "freeze_time": None,
        "protection": None,
        "notes": None
    },
    {
        "index_l": 75,
        "types_of_probes": "SPHERE",
        "size_Ice_ball": "3,6x2,9x2",
        "freeze_time": None,
        "protection": None,
        "notes": None
    }
]
df_cryo_lung = pd.DataFrame(lung_cryo_data)

# Derive number of cryoprobes from the description when explicit counts are not
# available. Many rows in the lung dataset include phrases like '2 SPHERE+2 ROD'
# describing the used probes. This helper extracts all numbers from that string
# and returns their sum so the app can display a numeric recommendation.
def parse_cryoprobes(probe_str: str):
    """Infer how many probes were used from a textual description."""
    if not probe_str or not isinstance(probe_str, str):
        return None

    nums = re.findall(r"\d+", probe_str)
    if nums:
        return sum(int(n) for n in nums)

    # If no explicit number is present but probe type exists, assume one probe
    if re.search(r"(sphere|rod)", probe_str.lower()):
        return 1
    return None

df_cryo_lung["cryoprobes"] = df_cryo_lung["types_of_probes"].apply(parse_cryoprobes)

df_main_lung.set_index("index_l", inplace=True)
df_cryo_lung.set_index("index_l", inplace=True)
df_lung_merged = pd.merge(df_main_lung, df_cryo_lung, left_index=True, right_index=True, how="inner")

#####################################
# 3) Utility Functions
#####################################

def parse_size(s: str):
    """
    Convert a string like '4,2 x 3,6 x 4,8' to a list of floats [4.2, 3.6, 4.8].
    """
    if not s:
        return None
    try:
        cleaned = s.replace("χ", "x").replace("Χ", "x").replace(",", ".")
        cleaned = re.sub(r"[^0-9.x]", " ", cleaned.lower())
        parts = cleaned.replace("x", " ").split()
        floats = [float(p) for p in parts if p]
        if len(floats) >= 3:
            return floats[:3]
    except Exception:
        return None

def parse_renal_score(rs: str):
    """
    Extract numeric portion from a RENAL score string (e.g., '5p' -> 5).
    """
    """Extract the numeric portion from a RENAL score string (e.g., '5p')."""
    match = re.search(r'(\d+)', rs)
    if match:
        return int(match.group(1))
    return None

def size_difference(user_dims, ref_dims, weight=5.0):
    """
    Calculate weighted difference in tumor size.
    """
    """Calculate weighted difference in tumor size."""
    user_sorted = np.sort(user_dims)
    ref_sorted = np.sort(ref_dims)
    diff = np.sum(np.abs(user_sorted - ref_sorted))
    return weight * diff

def renal_score_difference(user_score, ref_score, weight=2.0):
    """
    Weighted difference for RENAL score.
    """
    """Weighted difference for RENAL score."""
    if user_score is None or ref_score is None:
        return 0.0
    return weight * abs(user_score - ref_score)

def histology_difference(user_hist, ref_hist, weight=1.0):
    """
    Weighted difference for histology type.
    """
    """Weighted difference for histology type."""
    if not user_hist or not ref_hist:
        return weight
    return 0.0 if user_hist.lower() == ref_hist.lower() else weight

def type_lesion_diff(user_type, ref_type, weight=3.0):
    """
    Weighted difference for lung lesion type.
    """
    """Weighted difference for lung lesion type."""
    if not user_type or not ref_type:
        return weight
    return 0.0 if user_type.lower() == ref_type.lower() else weight

def age_difference(user_age, ref_age, weight=1.0):
    """Weighted age difference for lung cases."""
    if user_age is None or ref_age is None:
        return weight
    return weight * abs(user_age - ref_age) / 10.0

def side_diff(user_side, ref_side, weight=0.0):
    """
    Side difference (no penalty).
    """
    """Side difference (no penalty)."""
    return 0.0

#####################################
# 4) Streamlit App Interface
#####################################

st.title("Cryoablation Probe Calculator")

# First, select organ type: Kidney or Lung
organ_choice = st.sidebar.radio("Select Organ", ["Kidney", "Lung"])

if organ_choice == "Kidney":
    st.sidebar.header("Kidney Input")
    st.sidebar.write("Enter tumor dimensions (cm):")
    k_length = st.sidebar.number_input("Tumor Length", 0.5, 10.0, 4.2)
    k_width  = st.sidebar.number_input("Tumor Width", 0.5, 10.0, 3.6)
    k_height = st.sidebar.number_input("Tumor Height", 0.5, 10.0, 4.6)
    user_renal_score = st.sidebar.text_input("RENAL Score (e.g. '5p')", value="5p")
    user_renal_numeric = parse_renal_score(user_renal_score)
    user_histology = st.sidebar.selectbox("Histology", ["Clear Cell", "Papillary", "Chromophobe", "Other"])
    
    if st.sidebar.button("Generate Kidney Plan"):
        user_dims = [k_length, k_width, k_height]
        best_idx = None
        best_total = float("inf")
@@ -948,50 +967,54 @@ if organ_choice == "Kidney":
            st.write(f"**Estimated Ice Ball Size:** {match['size_Ice_ball']} cm")
            st.write(f"**Protection:** {match['protection']}")
            st.write(f"**Complications:** {match['complications']}")
            st.info(f"Difference Score: {best_total:.2f}")

elif organ_choice == "Lung":
    st.sidebar.header("Lung Input")
    user_type_lesion = st.sidebar.selectbox("Type of Lesion", ["NSCLC", "META-COLORECTAL", "Other"])
    user_age = st.sidebar.number_input("Age (years)", 18, 120, 70)
    user_side = st.sidebar.selectbox("Side", ["R", "L"])
    st.sidebar.write("Enter lesion dimensions (cm):")
    l_length = st.sidebar.number_input("Lesion Length", 0.5, 10.0, 2.5)
    l_width  = st.sidebar.number_input("Lesion Width", 0.5, 10.0, 2.0)
    l_height = st.sidebar.number_input("Lesion Height", 0.5, 10.0, 2.1)
    
    if st.sidebar.button("Generate Lung Plan"):
        user_dims = [l_length, l_width, l_height]
        best_idx = None
        best_total = float("inf")
        for idx, row in df_lung_merged.iterrows():
            ref_dims = parse_size(row["size_lung"])
            if not ref_dims:
                continue
            ref_type = row["type_lesion"]
            ref_side = row["side"]
            ref_age = row["age"]
            diff_size = size_difference(user_dims, ref_dims, weight=5.0)
            diff_type = type_lesion_diff(user_type_lesion, ref_type, weight=3.0)
            diff_side = side_diff(user_side, ref_side, weight=0.0)
            total_diff = diff_size + diff_type + diff_side
            diff_age = age_difference(user_age, ref_age, weight=1.0)
            total_diff = diff_size + diff_type + diff_side + diff_age
            if total_diff < best_total:
                best_total = total_diff
                best_idx = idx
        if best_idx is None:
            st.error("No matching lung reference data found.")
        else:
            match = df_lung_merged.loc[best_idx]
            st.subheader("Lung Cryoablation Plan")
            st.write(f"**Reference Lesion Type:** {match['type_lesion']}")
            st.write(f"**Reference Lesion Size:** {match['size_lung']} cm")
            st.write(f"**Reference Side:** {match['side']}")
            st.write("---")
            st.subheader("Cryoablation Parameters")
            st.write(f"**Recommended Cryoprobes:** {match.get('cryoprobes', 'N/A')}")
            cryo_val = match.get('cryoprobes')
            cryo_display = "N/A" if cryo_val is None or pd.isna(cryo_val) else int(cryo_val)
            st.write(f"**Recommended Cryoprobes:** {cryo_display}")
            st.write(f"**Types of Probes:** {match.get('types_of_probes', 'N/A')}")
            st.write(f"**Estimated Ice Ball Size:** {match.get('size_Ice_ball', 'N/A')} cm")
            st.write(f"**Notes/Additional Info:** {match.get('notes', 'N/A')}")
            st.info(f"Difference Score: {best_total:.2f}")

st.markdown("---")
st.write("Created by Michailidis A. for free use (demo).")
