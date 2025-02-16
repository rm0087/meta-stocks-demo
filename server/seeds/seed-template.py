#!/usr/bin/env python3

# Standard library imports
from random import random, randint, choice as rc
import os
import json


# Remote library imports


# Local imports
from app import app
from models import db
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
with app.app_context():

   print("Starting seed...")

   
   
   print("Seed successful")
