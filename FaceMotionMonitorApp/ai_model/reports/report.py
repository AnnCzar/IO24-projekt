from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import date
from FaceMotionMonitorApp import services, views

def make_figures(patient_id):
    dates, mouth, brows = services.get_data_for_reports(patient_id)

    #mouth
    plt.figure(figsize=(12, 8))
    plt.plot(dates, mouth, label='Mouth Corners Distance', marker='o')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=1))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    mouth_fig = plt.gcf()

    #brows
    plt.figure(figsize=(12, 8))
    plt.plot(dates, brows, label='Eyebrows Distance Difference', marker='x', color='orange')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=1))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    eyebrows_fig = plt.gcf()
    return mouth_fig, eyebrows_fig

def distance_comparison(patient_id):
    dates, mouth, brows = services.get_data_for_reports(patient_id)
    mouth_diff_first = mouth[-1]/mouth[0]*100
    mouth_diff_previous = mouth[-1]/mouth[-2]*100

    eyebrows_diff_first = brows[-1]/brows[0]*100
    eyebrows_diff_previous = brows[-1]/brows[-2]*100
    return mouth_diff_first, mouth_diff_previous, eyebrows_diff_first, eyebrows_diff_previous


def create_report(patient_id):
    today = date.today()
    patient_data = services.get_patient_details(patient_id)
    file_name = patient_data["name"] + "_report_" + str(today)
    mouth_fig, eyebrows_fig = make_figures(patient_id)
    mouth_diff_first, mouth_diff_previous, eyebrows_diff_first, eyebrows_diff_previous = distance_comparison(patient_id)
    report = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    text_mouth = "MOUTH CORNERS AREA"
    report.drawString(100, height - 50, text_mouth)
    mouth_fig.savefig('mouth_corners.png')
    report.drawImage('mouth_corners.png', 100, height - 300, width=400, height=200)
    analysis_mouth =  str(mouth_diff_previous) + "% " + " difference from the previous measurement" + "\n" + str(mouth_diff_first)+ "% " + " difference from the first measurement"
    report.drawString(100, height - 350, analysis_mouth)


    text_eyebrows = "EYEBROWS AREA"
    report.drawString(100, height - 400, text_eyebrows)
    eyebrows_fig.savefig('eyebrows.png')
    report.drawImage('eyebrows.png', 100, height - 650, width=400, height=200)
    analysis_eyebrows =  str(eyebrows_diff_previous) + "% " + " difference from the previous measurement" + "\n" + str(eyebrows_diff_first)+ "% " + " difference from the first measurement"
    report.drawString(100, height - 700, analysis_eyebrows)
    report.save()

    # usuwamy te tymczasowe zeby bez syfu bylo
    os.remove("mouth_corners.png")
    os.remove("eyebrows.png")