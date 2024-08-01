import streamlit as st
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
from jinja2 import Template #pour le rendu des variables dans le fichier HTML.
import os
