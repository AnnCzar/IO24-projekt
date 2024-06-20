from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import date

#
#
# brudnopisowa wersja
#

def create_report(mouth_fig, eyebrows_fig, mouth_diff_prev, mouth_diff_first, eyebrows_diff_prev, eyebrows_diff_first, username):
    today = date.today()
    file_name = username + "_report_" + str(today)
    report = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    text_mouth = "MOUTH CORNERS AREA"
    report.drawString(100, height - 50, text_mouth)
    mouth_fig.savefig('mouth_corners.png')
    report.drawImage('mouth_corners.png', 100, height - 300, width=400, height=200)
    analysis_mouth =  str(mouth_diff_prev) + "% " + " difference from the previous measurement" + "\n" + str(mouth_diff_first)+ "% " + " difference from the first measurement"
    report.drawString(100, height - 350, analysis_mouth)


    text_eyebrows = "EYEBROWS AREA"
    report.drawString(100, height - 400, text_eyebrows)
    eyebrows_fig.savefig('eyebrows.png')
    report.drawImage('eyebrows.png', 100, height - 650, width=400, height=200)
    analysis_eyebrows =  str(eyebrows_diff_prev) + "% " + " difference from the previous measurement" + "\n" + str(eyebrows_diff_first)+ "% " + " difference from the first measurement"
    report.drawString(100, height - 700, analysis_eyebrows)
    report.save()

    # usuwamy te tymczasowe zeby bez syfu bylo
    os.remove("mouth_corners.png")
    os.remove("eyebrows.png")