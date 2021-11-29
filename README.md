# Ticket-Viewer

To run viewer, simply cd to the directory and run: </br>
pip install --editable . </br>
python3 viewer.py </br>
Enter the OAuth token, as sent in the email, as is when prompted (no quotation marks). </br>
Follow the prompts to view the tickets. </br>
Currently, looking at all the tickets prints out 10 at a time because 25 was too much with the given format. </br>
</br>
</br>
To run tests, first enter the viewer source code and change the testing variable at the top to True. </br>
Then, set the token equal to the OAuth code to run the tests with the valid token and leave it equal to anything else to run the tests for an invalid token.</br>
cd to the Ticket-Viewer folder and run python3 test.py </br>


</br>

I ran into a few problems testing the UI in the test.py file, and I did not want to stray away from the instructions that said to only use unittest, so I tested the UI/CLI inputs separately. The library I used for the CLI required a different testing library to be implemented. If I had more time, I would have done much more thorough testing for the UI to ensure that no improper input allowed for a security breach. The helper methods were thoroughly tested, which is where most of the backend takes place, but I do acknowledge that the user interface can be equally as important as the backend. I would have also worked to avoid a bit of sloppy backend work with requiring a testing = True/False variable to prevent method hopping while testing.</br>
I would have also worked to utilize some more python libraries such as django to avoid unnecessary code.</br>

Thank you for taking the time to review my submission! I hope to hear from you soon! </br>
