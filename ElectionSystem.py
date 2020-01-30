#Mihail Mihaylov 001062346
#Aisha Scacchi 001067045

#LOGIN DETAILS FOR DEMO ARE
#ID - 1
#PASSWORD - 123

import datetime
from tkinter import *
import tkinter
import sys

#Set dimensions for window
window = tkinter.Tk()
window.title("GSU Elections")
window.geometry("+800+400")

#Create empty list which we are going to use later
#To store necessery date
listOfVoters = []
listOfCandidates = []
listOfAvailablePositions = []

#Set the election period
#Currently from 20th January 2020 to 31st January 2020
electionStartDate = datetime.date(2020, 1, 20)
electionEndDate = datetime.date(2020, 1, 31)

#Creating empty variables where we are going to store the winners
#and the current logged in voter
president_winner = ""
officer_winner = ""
faculty_officer_winner = ""
currentVoter = ''


class Candidate:
    def __init__(self, position, firstName, lastName):
        self.position = position
        self.firstName = firstName
        self.lastName = lastName
        self.firstPreference = 0
        self.secondPreference = 0
        self.thirdPreference = 0
        self.fourthPreference = 0


class Voter:
    def __init__(self, studentId, password, firstName, lastName):
        self.studentId = studentId
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.votedForPresident = 0
        self.votedForOfficer = 0
        self.votedForFacultyOfficer = 0


#Login Page
voterId = StringVar()
tkinter.Label(window, text="ID (enter '1')").grid(row=0, column = 0)
tkinter.Entry(window, textvariable = voterId, ).grid(row=0, column=1)

password = StringVar()
tkinter.Label(window, text="Password (enter '123')").grid(row=1, column = 0)
tkinter.Entry(window, show="*", textvariable = password).grid(row=1, column=1)



def login():
    entered_id = voterId.get()
    entered_password = password.get()

    #check login details
    if any(x.studentId == entered_id and x.password == entered_password for x in listOfVoters):
        #check election date
        if electionStartDate <= currentDate <= electionEndDate:
            #get current logged in voter
            for voter in listOfVoters:
                if voter.studentId == entered_id and voter.password == entered_password:
                    currentVoter = voter

            def vote(*args):

                chosen_position = drop_down_menu.get()

                if chosen_position == 'President':
                 #Get all the candidates appling for President
                    listOfCandPresidents = []
                    for cand in listOfCandidates:
                        if cand.position == 'President':
                            listOfCandPresidents.append(cand.firstName + " " + cand.lastName)

                    def submit():
                        #Check if the current logged in user have already voted for the given positon
                        readVotedPeopleFile = open("PeopleWhoHaveVoted.txt", "r").readlines()
                        for person in readVotedPeopleFile:
                            if currentVoter.firstName + " " + currentVoter.lastName + " " + "President\n" == person:
                                currentVoter.votedForPresident = 1

                        #Save 1st, 2nd, 3rd, 4th preference into Votes.txt

                        if currentVoter.votedForPresident == 0:
                            writeVotedPeopleFile = open("PeopleWhoHaveVoted.txt", "a")
                            writeVotedPeopleFile.writelines(currentVoter.firstName + " " + currentVoter.lastName + " President\n")
                            first_preference_person = first_preference.get()
                            second_preference_person = second_preference.get()
                            third_preference_person = third_preference.get()
                            fourth_preference_person = fourth_preference.get()

                            votes_file = open("Votes.txt", "a")
                            votes_file.writelines(first_preference_person + " " + "1\n")
                            votes_file.writelines(second_preference_person + " " + "2\n")
                            votes_file.writelines(third_preference_person + " " + "3\n")
                            votes_file.writelines(fourth_preference_person + " " + "4\n")
                            votes_file.close()

                            def results():
                                #Read the votes and pick a winner
                                result_file = open("Votes.txt", "r")
                                file_lines = result_file.readlines()

                                votesCounter = 0

                                for line in file_lines:
                                    votesCounter += 1
                                    first_name = line.split()[0]
                                    last_name = line.split()[1]
                                    preference = line.split()[2]
                                    for candToCheck in listOfCandidates:
                                        if candToCheck.firstName + ' ' + candToCheck.lastName == first_name + ' ' + last_name:
                                            if preference == "1":
                                                candToCheck.firstPreference += 1
                                            if preference == "2":
                                                candToCheck.secondPreference += 1
                                            if preference == "3":
                                                candToCheck.thirdPreference += 1
                                            if preference == "4":
                                                candToCheck.fourthPreference += 1
                                            break
                                listWinners = []
                                for winner in listOfCandidates:
                                    if winner.position == "President":
                                        listWinners.append(winner)

                                #Sort the winners by 1st preference, if there is a tie
                                #We look at the 2nd preference and so on

                                sorted_winners = sorted(listWinners, key=lambda x: x.firstPreference, reverse=True)

                                if sorted_winners[0].firstPreference == sorted_winners[1].firstPreference:
                                    if sorted_winners[0].secondPreference == sorted_winners[1].secondPreference:
                                        if sorted_winners[0].thirdPreference == sorted_winners[1].thirdPreference:
                                            if sorted_winners[0].fourthPreference == sorted_winners[1].fourthPreference:
                                                sorted_winners = sorted(listWinners, key=lambda x: (
                                                x.firstPreference, x.fourthPreference), reverse=True)
                                        else:
                                            sorted_winners = sorted(listWinners, key=lambda x: (
                                            x.firstPreference, x.thirdPreference), reverse=True)
                                    else:
                                        sorted_winners = sorted(listWinners,
                                                                key=lambda x: (x.firstPreference, x.secondPreference),
                                                                reverse=True)

                                #Print out the results
                                tkinter.Label(window, text="Position: GSU " + cand.position).grid(row=15, column=0)
                                tkinter.Label(window,
                                              text="Candidate     1stPreference    2ndPreference    3rdPreference   4thPreference").grid(
                                    row=16, column=0)
                                rowCounter = 16
                                for winner in sorted_winners:
                                    rowCounter += 1
                                    tkinter.Label(window,
                                                  text=winner.firstName + " " + winner.lastName + "         " + str(
                                                      winner.firstPreference) + "         " + str(
                                                      winner.secondPreference) + "         " + str(
                                                      winner.thirdPreference) + "         " + str(
                                                      winner.fourthPreference)).grid(row=rowCounter, column=0)
                                president_winner = sorted_winners[0].firstName + " " + sorted_winners[0].lastName
                                tkinter.Label(window,
                                              text="Winner: " + sorted_winners[0].firstName + " " + sorted_winners[
                                                  0].lastName).grid(row=rowCounter + 1, column=0)
                                tkinter.Label(window,
                                              text="Votes Received: " + str(sorted_winners[0].firstPreference)).grid(
                                    row=rowCounter + 2, column=0)
                                tkinter.Label(window, text="Total votes cast overall: " + str(votesCounter)).grid(
                                    row=rowCounter + 3, column=0)
                                percentsOfVoters = (sorted_winners[0].firstPreference * 100) / votesCounter
                                tkinter.Label(window,
                                              text=str(round(percentsOfVoters, 1)) + " % of the voters voted for " +
                                                   sorted_winners[0].firstName + " " + sorted_winners[0].lastName).grid(
                                    row=rowCounter + 4, column=0)
                                winners_file = open("winners.txt", "a")
                                winners_file.writelines(
                                    "Winner for position " + sorted_winners[0].position + " " + "is " + sorted_winners[
                                        0].firstName + " " + sorted_winners[0].lastName + "\n")

                                def summary():
                                    #Get a summary of the winners for all the position
                                    read_winners_file = open("winners.txt", "r")
                                    lineCounter = rowCounter + 6
                                    for line in read_winners_file:
                                        tkinter.Label(window, text=line).grid(row=lineCounter, column=0)
                                        lineCounter += 1

                                tkinter.Button(window, command=summary, text='Summary').grid(row=rowCounter + 5,
                                                                                             column=2)

                            tkinter.Button(window, command=results, text='Show election results').grid(row=13, column=2)
                        else:
                            tkinter.Label(window, text="You have already voted for President", fg="red").grid(row=11, column=0)


                    first_preference = tkinter.StringVar(window)
                    first_preference.set("---")

                    tkinter.Label(window, text="Select 1st Preference").grid(row=7, column=0)
                    w_president = tkinter.OptionMenu(window, first_preference, *listOfCandPresidents)
                    w_president.grid(row=7, column=1)

                    second_preference = tkinter.StringVar(window)
                    second_preference.set("---")

                    tkinter.Label(window, text="Select 2nd Preference").grid(row=8, column=0)
                    w_president = tkinter.OptionMenu(window, second_preference, *listOfCandPresidents)
                    w_president.grid(row=8, column=1)

                    third_preference = tkinter.StringVar(window)
                    third_preference.set("---")

                    tkinter.Label(window, text="Select 3rd Preference").grid(row=9, column=0)
                    w_president = tkinter.OptionMenu(window, third_preference, *listOfCandPresidents)
                    w_president.grid(row=9, column=1)

                    fourth_preference = tkinter.StringVar(window)
                    fourth_preference.set("---")

                    tkinter.Label(window, text="Select 4th Preference").grid(row=10, column=0)
                    w_president = tkinter.OptionMenu(window, fourth_preference, *listOfCandPresidents)
                    w_president.grid(row=10, column=1)

                    tkinter.Button(window, command=submit, text='Submit').grid(row=11, column=2)

                if chosen_position == 'Officer':
                    # Get all the candidates appling for Officer
                    listOfCandOfficer = []
                    for cand in listOfCandidates:
                        if cand.position == 'Officer':
                            listOfCandOfficer.append(cand.firstName + " " + cand.lastName)

                    def submit():
                        # Check if the current logged in user have already voted for the given positon
                        readVotedPeopleFile = open("PeopleWhoHaveVoted.txt", "r").readlines()
                        for person in readVotedPeopleFile:
                            if currentVoter.firstName + " " + currentVoter.lastName + " Officer\n" == person:
                                currentVoter.votedForOfficer = 1
                        # Save 1st, 2nd, 3rd, 4th preference into Votes.txt
                        if currentVoter.votedForOfficer == 0:
                            writeVotedPeopleFile = open("PeopleWhoHaveVoted.txt", "a")
                            writeVotedPeopleFile.writelines(currentVoter.firstName + " " + currentVoter.lastName + " Officer\n")

                            first_preference_person = first_preference.get()
                            second_preference_person = second_preference.get()
                            third_preference_person = third_preference.get()
                            fourth_preference_person = fourth_preference.get()

                            votes_file = open("Votes.txt", "a")
                            votes_file.writelines(first_preference_person + " " + "1\n")
                            votes_file.writelines(second_preference_person + " " + "2\n")
                            votes_file.writelines(third_preference_person + " " + "3\n")
                            votes_file.writelines(fourth_preference_person + " " + "4\n")
                            votes_file.close()

                            def results():
                                # Read the votes and pick a winner
                                result_file = open("Votes.txt", "r")
                                file_lines = result_file.readlines()

                                votesCounter = 0

                                for line in file_lines:
                                    votesCounter += 1
                                    first_name = line.split()[0]
                                    last_name = line.split()[1]
                                    preference = line.split()[2]
                                    for candToCheck in listOfCandidates:
                                        if candToCheck.firstName + ' ' + candToCheck.lastName == first_name + ' ' + last_name:
                                            if preference == "1":
                                                candToCheck.firstPreference += 1
                                            if preference == "2":
                                                candToCheck.secondPreference += 1
                                            if preference == "3":
                                                candToCheck.thirdPreference += 1
                                            if preference == "4":
                                                candToCheck.fourthPreference += 1
                                            break
                                listWinners = []
                                for winner in listOfCandidates:
                                    if winner.position == "Officer":
                                        listWinners.append(winner)

                                # Sort the winners by 1st preference, if there is a tie
                                # We look at the 2nd preference and so on
                                sorted_winners = sorted(listWinners, key=lambda x: x.firstPreference, reverse=True)

                                if sorted_winners[0].firstPreference == sorted_winners[1].firstPreference:
                                    if sorted_winners[0].secondPreference == sorted_winners[1].secondPreference:
                                        if sorted_winners[0].thirdPreference == sorted_winners[1].thirdPreference:
                                            if sorted_winners[0].fourthPreference == sorted_winners[1].fourthPreference:
                                                sorted_winners = sorted(listWinners, key=lambda x: (
                                                x.firstPreference, x.fourthPreference), reverse=True)
                                        else:
                                            sorted_winners = sorted(listWinners, key=lambda x: (
                                            x.firstPreference, x.thirdPreference), reverse=True)
                                    else:
                                        sorted_winners = sorted(listWinners,
                                                                key=lambda x: (x.firstPreference, x.secondPreference),
                                                                reverse=True)
                                # Print out the results
                                tkinter.Label(window, text="Position: GSU Officer").grid(row=15, column=0)
                                tkinter.Label(window,
                                              text="Candidate     1stPreference    2ndPreference    3rdPreference   4thPreference").grid(
                                    row=16, column=0)
                                rowCounter = 16
                                for winner in sorted_winners:
                                    rowCounter += 1
                                    tkinter.Label(window,text=winner.firstName + " " + winner.lastName + "         " + str(winner.firstPreference) + "         " + str(winner.secondPreference) + "         " + str(winner.thirdPreference) + "         " + str(winner.fourthPreference)).grid(row=rowCounter, column=0)

                                officer_winner = sorted_winners[0].firstName + " " + sorted_winners[1].lastName
                                tkinter.Label(window,text="Winner: " + sorted_winners[0].firstName + " " + sorted_winners[0].lastName).grid(row=rowCounter + 1, column=0)
                                tkinter.Label(window,text="Votes Received: " + str(sorted_winners[0].firstPreference)).grid(row=rowCounter + 2, column=0)
                                tkinter.Label(window, text="Total votes cast overall: " + str(votesCounter)).grid(row=rowCounter + 3, column=0)
                                percentsOfVoters = (sorted_winners[0].firstPreference * 100) / votesCounter
                                tkinter.Label(window,
                                              text=str(round(percentsOfVoters, 1)) + " % of the voters voted for " +
                                                   sorted_winners[0].firstName + " " + sorted_winners[0].lastName).grid(
                                    row=rowCounter + 4, column=0)

                                winners_file = open("winners.txt", "a")

                                winners_file.writelines(
                                    "Winner for position " + sorted_winners[0].position + " " + "is " + sorted_winners[
                                        0].firstName + " " + sorted_winners[0].lastName + "\n")

                                def summary():
                                    # Get a summary of the winners for all the position
                                    read_winners_file = open("winners.txt", "r")
                                    lineCounter = rowCounter + 6
                                    for line in read_winners_file:
                                        tkinter.Label(window, text=line).grid(row=lineCounter, column=0)
                                        lineCounter += 1

                                tkinter.Button(window, command=summary, text='Summary').grid(row=rowCounter + 5,
                                                                                             column=2)

                                rowCounter = 16
                                for winner in sorted_winners:
                                    rowCounter += 1
                                    tkinter.Label(window, text=winner.firstName + " " + winner.lastName + "     " + str(
                                        winner.firstPreference) + "     " + str(winner.secondPreference) + "    " + str(
                                        winner.thirdPreference) + "    " + str(winner.fourthPreference)).grid(
                                        row=rowCounter, column=0)

                            tkinter.Button(window, command=results, text='Show election results').grid(row=13, column=2)

                        else:
                            tkinter.Label(window, text="You have already voted for Officer", fg="red").grid(row=11, column=0)

                    first_preference = tkinter.StringVar(window)
                    first_preference.set("---")

                    tkinter.Label(window, text="Select 1st Preference").grid(row=7, column=0)
                    w_president = tkinter.OptionMenu(window, first_preference, *listOfCandOfficer)
                    w_president.grid(row=7, column=1)

                    second_preference = tkinter.StringVar(window)
                    second_preference.set("---")

                    tkinter.Label(window, text="Select 2nd Preference").grid(row=8, column=0)
                    w_president = tkinter.OptionMenu(window, second_preference, *listOfCandOfficer)
                    w_president.grid(row=8, column=1)

                    third_preference = tkinter.StringVar(window)
                    third_preference.set("---")

                    tkinter.Label(window, text="Select 3rd Preference").grid(row=9, column=0)
                    w_president = tkinter.OptionMenu(window, third_preference, *listOfCandOfficer)
                    w_president.grid(row=9, column=1)

                    fourth_preference = tkinter.StringVar(window)
                    fourth_preference.set("---")

                    tkinter.Label(window, text="Select 4th Preference").grid(row=10, column=0)
                    w_president = tkinter.OptionMenu(window, fourth_preference, *listOfCandOfficer)
                    w_president.grid(row=10, column=1)
                    tkinter.Button(window, command=submit, text='Submit').grid(row=11, column=2)

                if chosen_position == 'Faculty Officer':
                    # Get all the candidates appling for Faculty Officer
                    listOfCandFacultyOfficer = []
                    for cand in listOfCandidates:
                        if cand.position == 'Faculty Officer':
                            listOfCandFacultyOfficer.append(cand.firstName + " " + cand.lastName)

                    def submit():
                        # Check if the current logged in user have already voted for the given positon
                        readVotedPeopleFile = open("PeopleWhoHaveVoted.txt", "r").readlines()
                        for person in readVotedPeopleFile:
                            if currentVoter.firstName + " " + currentVoter.lastName + " " + "Faculty Officer\n" == person:
                                currentVoter.votedForFacultyOfficer = 1

                        # Save 1st, 2nd, 3rd, 4th preference into Votes.txt
                        if currentVoter.votedForFacultyOfficer == 0:
                            writeVotedPeopleFile = open("PeopleWhoHaveVoted.txt", "a")
                            writeVotedPeopleFile.writelines(currentVoter.firstName + " " + currentVoter.lastName + " Faculty Officer\n")
                            first_preference_person = first_preference.get()
                            second_preference_person = second_preference.get()
                            third_preference_person = third_preference.get()
                            fourth_preference_person = fourth_preference.get()

                            votes_file = open("Votes.txt", "a")
                            votes_file.writelines(first_preference_person + " " + "1\n")
                            votes_file.writelines(second_preference_person + " " + "2\n")
                            votes_file.writelines(third_preference_person + " " + "3\n")
                            votes_file.writelines(fourth_preference_person + " " + "4\n")
                            votes_file.close()

                            def results():
                                # Read the votes and pick a winner
                                result_file = open("Votes.txt", "r")
                                file_lines = result_file.readlines()

                                votesCounter = 0
                                for line in file_lines:
                                    votesCounter += 1
                                    first_name = line.split()[0]
                                    last_name = line.split()[1]
                                    preference = line.split()[2]
                                    for candToCheck in listOfCandidates:
                                        if candToCheck.firstName + ' ' + candToCheck.lastName == first_name + ' ' + last_name:
                                            if preference == "1":
                                                candToCheck.firstPreference += 1
                                            if preference == "2":
                                                candToCheck.secondPreference += 1
                                            if preference == "3":
                                                candToCheck.thirdPreference += 1
                                            if preference == "4":
                                                candToCheck.fourthPreference += 1
                                            break
                                listWinners = []
                                for winner in listOfCandidates:
                                    if winner.position == "Faculty Officer":
                                        listWinners.append(winner)

                                # Sort the winners by 1st preference, if there is a tie
                                # We look at the 2nd preference and so on

                                sorted_winners = sorted(listWinners, key=lambda x: x.firstPreference, reverse=True)

                                if sorted_winners[0].firstPreference == sorted_winners[1].firstPreference:
                                    if sorted_winners[0].secondPreference == sorted_winners[1].secondPreference:
                                        if sorted_winners[0].thirdPreference == sorted_winners[1].thirdPreference:
                                            if sorted_winners[0].fourthPreference == sorted_winners[1].fourthPreference:
                                                sorted_winners = sorted(listWinners, key=lambda x: (
                                                x.firstPreference, x.fourthPreference), reverse=True)
                                        else:
                                            sorted_winners = sorted(listWinners, key=lambda x: (
                                            x.firstPreference, x.thirdPreference), reverse=True)
                                    else:
                                        sorted_winners = sorted(listWinners,
                                                                key=lambda x: (x.firstPreference, x.secondPreference),
                                                                reverse=True)

                                # Print out the results
                                tkinter.Label(window, text="Position: GSU Faculty Officer").grid(row=15, column=0)
                                tkinter.Label(window,
                                              text="Candidate     1stPreference    2ndPreference    3rdPreference   4thPreference").grid(
                                    row=16, column=0)

                                rowCounter = 16
                                for winner in sorted_winners:
                                    rowCounter += 1
                                    tkinter.Label(window,
                                                  text=winner.firstName + " " + winner.lastName + "         " + str(
                                                      winner.firstPreference) + "         " + str(
                                                      winner.secondPreference) + "         " + str(
                                                      winner.thirdPreference) + "         " + str(
                                                      winner.fourthPreference)).grid(
                                        row=rowCounter, column=0)
                                faculty_officer_winner = sorted_winners[0].firstName + " " + sorted_winners[1].lastName
                                tkinter.Label(window,
                                              text="Winner: " + sorted_winners[0].firstName + " " + sorted_winners[
                                                  0].lastName).grid(row=rowCounter + 1, column=0)
                                tkinter.Label(window,
                                              text="Votes Received: " + str(sorted_winners[0].firstPreference)).grid(
                                    row=rowCounter + 2, column=0)
                                tkinter.Label(window, text="Total votes cast overall: " + str(votesCounter)).grid(
                                    row=rowCounter + 3, column=0)
                                percentsOfVoters = (sorted_winners[0].firstPreference * 100) / votesCounter
                                tkinter.Label(window,
                                              text=str(round(percentsOfVoters, 1)) + " % of the voters voted for " +
                                                   sorted_winners[0].firstName + " " + sorted_winners[0].lastName).grid(
                                    row=rowCounter + 4, column=0)

                                winners_file = open("winners.txt", "a")
                                winners_file.writelines(
                                    "Winner for position " + sorted_winners[0].position + " " + "is " + sorted_winners[
                                        0].firstName + " " + sorted_winners[0].lastName + "\n")

                                def summary():
                                    # Get a summary of the winners for all the position
                                    read_winners_file = open("winners.txt", "r")
                                    lineCounter = rowCounter + 6
                                    for line in read_winners_file:
                                        tkinter.Label(window, text=line).grid(row=lineCounter, column=0)
                                        lineCounter += 1

                                tkinter.Button(window, command=summary, text='Summary').grid(row=rowCounter + 5,
                                                                                             column=2)

                                rowCounter = 16
                                for winner in sorted_winners:
                                    rowCounter += 1
                                    tkinter.Label(window, text=winner.firstName + " " + winner.lastName + "     " + str(
                                        winner.firstPreference) + "     " + str(winner.secondPreference) + "    " + str(
                                        winner.thirdPreference) + "    " + str(winner.fourthPreference)).grid(
                                        row=rowCounter, column=0)

                            tkinter.Button(window, command=results, text='Show election results').grid(row=13, column=2)

                        else:
                            tkinter.Label(window, text="You have already voted for Faculty Officer", fg="red").grid(row=11, column=0)

                    first_preference = tkinter.StringVar(window)
                    first_preference.set("---")

                    tkinter.Label(window, text="Select 1st Preference").grid(row=7, column=0)
                    w_president = tkinter.OptionMenu(window, first_preference, *listOfCandFacultyOfficer)
                    w_president.grid(row=7, column=1)

                    second_preference = tkinter.StringVar(window)
                    second_preference.set("---")

                    tkinter.Label(window, text="Select 2nd Preference").grid(row=8, column=0)
                    w_president = tkinter.OptionMenu(window, second_preference, *listOfCandFacultyOfficer)
                    w_president.grid(row=8, column=1)

                    third_preference = tkinter.StringVar(window)
                    third_preference.set("---")

                    tkinter.Label(window, text="Select 3rd Preference").grid(row=9, column=0)
                    w_president = tkinter.OptionMenu(window, third_preference, *listOfCandFacultyOfficer)
                    w_president.grid(row=9, column=1)

                    fourth_preference = tkinter.StringVar(window)
                    fourth_preference.set("---")

                    tkinter.Label(window, text="Select 4th Preference").grid(row=10, column=0)
                    w_president = tkinter.OptionMenu(window, fourth_preference, *listOfCandFacultyOfficer)
                    w_president.grid(row=10, column=1)

                    tkinter.Button(window, command=submit, text='Submit').grid(row=11, column=2)

            drop_down_menu = tkinter.StringVar(window)
            drop_down_menu.set(listOfAvailablePositions[0])
            drop_down_menu.trace("w", vote)

            #Dropdown menu for the logged in voter to choose for which position is voting
            tkinter.Label(window, text="Choose position").grid(row=6, column=0)
            w = tkinter.OptionMenu(window, drop_down_menu, *listOfAvailablePositions)
            w.grid(row=6, column=1)
#In case that we are out of the voting period
#Calculate how much time (in days) is left until we are in the period
        else:
            if electionStartDate > currentDate:
                gap=(electionStartDate - currentDate).days
            else:
                gap = (currentDate - electionStartDate).days
                gap = 365 - gap
            tkinter.Label(window, text="You are out of voting period. Try again in " + str(gap) + ' days', fg='red').grid(row=3, column = 1)
#Messega appears if login details are wrong
    else:
        tkinter.Label(window, text="Wrong ID and/or password", fg="red").grid(row=3, column = 1)


tkinter.Button(window, command=login, text='Login').grid(columnspan = 2)


#Reading the candidates and the voters from the .txt files
candidates = open("GSUCandidates.txt","r")
voters = open("StudentVoters.txt","r")

#Saving the candidates and the voters into the empty lists
#that we created earlier using class for both Candidates and Voters
for candidate in candidates.readlines():
    if len(candidate.split()) == 3:
        candidatePosition = candidate.split()[0]
        candidateFirstName = candidate.split()[1]
        candidateLastName = candidate.split()[2]

        if not any(candidate.firstName == candidateFirstName and candidate.lastName == candidateLastName for candidate in listOfCandidates):
            listOfCandidates.append(Candidate(candidatePosition, candidateFirstName, candidateLastName))
            if candidatePosition not in listOfAvailablePositions:
                listOfAvailablePositions.append(candidatePosition)


    if len(candidate.split()) == 4:
        candidatePosition = candidate.split()[0] + ' ' + candidate.split()[1]
        candidateFirstName = candidate.split()[2]
        candidateLastName = candidate.split()[3]
        if not any(candidate.firstName == candidateFirstName and candidate.lastName == candidateLastName for candidate in listOfCandidates):
            listOfCandidates.append(Candidate(candidatePosition, candidateFirstName, candidateLastName))
            if candidatePosition not in listOfAvailablePositions:
                listOfAvailablePositions.append(candidatePosition)


for voter in voters.readlines():
    voterStudentId = voter.split()[0]
    voterPassword = voter.split()[1]
    voterFirstName = voter.split()[2]
    voterLastName = voter.split()[3]

    listOfVoters.append(Voter(voterStudentId, voterPassword, voterFirstName, voterLastName))


currentDate = datetime.datetime.now().date()



#Terminate the program when exit button is clicked
def close():
      exit()


tkinter.Button(window, command=close, text='Exit').grid(row = 5, column = 5)

window.mainloop()