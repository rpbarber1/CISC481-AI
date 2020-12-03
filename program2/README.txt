Ryan Barber
CISC 481 
Program 2

Setup: (None required)
    Languages javascript, jquery, html, css

    Jquery is linked through a url, this may require an internet connection.
        I'm not sure though.

    No server environment software required just whats in the folder.


Board Display:
    If No Queens specified by user:
        There will be N number of boards shown
    If 'm' Queens specified by user:
        There will be N-(m-1) boards shown

    This means if you choose the location of some queens,
    the first board will have those queens placed already.

=================================================
=================================================
Open any of the html files in the folder to start. 
=================================================
=================================================
On the web page:
    Select Number of Queens button:
        click the one you want

    Queen selctor buttons:
        Q-x = the column of the Queen
        Button = the row of the queen placement

    Reset Queens button:
        This will clear your selections

    Solve button:
        This will solve and draw boards
        
Time to sove and draw boards:
    8 Queens:
        instant; 1 second
    12 Queens:
        10 seconds
    16 Queens:
        20 seconds

If browser asks to wait; let it wait.

If any problems:
    Try:
        'Reset Queens' button
    Try:
        Refresh page, then 'Reset Queens' button
    Else:
        Close browser tab. Reopen one of the html files.


If web page not working:
    Install Node.js or other javascript environment.
    Uncomment the lines at the bottom of the 'barber-prog2.js' file
    Execute in shell:
        node barber-prog2.js  (if using node.js)
        
    This should return a solution to the problem
