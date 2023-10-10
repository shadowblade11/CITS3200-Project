import wave
import matplotlib.pyplot as plt
import numpy as np
from app import db

# sample code to grab scores given our database.
user_id=3
db.session.query(Question).filter_by(user_id=user_id, ) # gives all questions attempted by a student. Would need to then order by which test it is within.
test_scores = {}

def plot_aggregate_scores(weeks, output_path, filename):
    """
    For now format is a little bit of a mystery so just making assumptions that can easily be fixed later
    Plots average scores per week for all students as bar graph and saves as .png
    Parameters:
    scores -- A list of students' scores -- assume their . like [{student1's scores}, {student2's scores}...]
        where objects are of form {"Score": [list of scores], "name":"student name"} still more to be figured out. 
    output_path -- the path to output the image.
    filename -- The name of the file to keep the image.
    """
    
    avgs = []
    # need to figure out what to put here

    plt.switch_backend('Agg')

    length = np.linspace(0, avgs.length, num=avgs.length)

    plt.figure(figsize=(20,5))
    plt.title(f"Average Scores")
    plt.plot(length, np.array(avgs))
    
    plt.savefig(f"{output_path}/{filename}")
    plt.close()
    return


def plot_individual_scores(scores, output_path, filename):
    """
    Plots individual scores for students as line graph and saves as .png
    Parameters:
    scores -- A list of students' scores. like [{student1's scores}, {student2's scores}...]
        where objects are of form {"Score": [list of scores], "name":"student name"} still more to be figured out. 
    output_path -- the path to output the image.
    filename -- The name of the file to keep the image.
    """

    # plt.switch_backend('Agg')

    # length = np.linspace(0, .length, num=avgs.length)

    # plt.figure(figsize=(20,5))
    # plt.title(f"Average Scores")
    # plt.plot(length, numpy.array(avgs))
    
    # plt.savefig(f"{output_path}/{filename}")
    # plt.close()

    return 0
