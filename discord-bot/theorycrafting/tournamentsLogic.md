<h1>Tournament Logic</h1>

<h2>Introduction</h2>

<p>Tournaments are brackets of players that compete against each other in organized play. Tournaments can be created and customized by users with the appropriate permissions.</p>

<h2>Creating a Tournament</h2>
<p>Users can create a tournament by using the <a>`/create-tournament`</a> Command. There will be a popup allowing the user to enter the following optional information:
<ul>
    <li>Tournament Name</li>
    <li>Tournament Description</li>
    <li>Number of Players</li>
    <li>Tournament Visibility</li>
    <li>Player list</li>
    <li>Player Schedules</li>
    <li>Start Date</li>
    <li>End Date</li>
    <li>Game Format</li>
    <li>Matchmaking Format</li>
    <li>Power Level</li>
    <li>Deck Submissions</li>
    <li>Prize</li>
</ul>
If values are not provided, the tournament will use default values. The tournament will be created, the tournament name will be the user's username, and the user will be added as the tournament Owner. The rest of the options will be left blank</p>

<h2>Joining a Tournament</h2>
<p>Users can join a tournament by using the <a>`/tournaments`</a> Command. There will be a popup allowing the user to see the active tournaments and join if they are public. Additionally, they will be able to see the the bracket if available, as well as the tournament's status.  If the tournament is private, the user will need to be manually added by the owner.</p>

<h2>Generating a Bracket</h2>
<p>If a tournament has the desired number of players, the owner can generate a bracket using the <a>`/generate-bracket`</a> Command.
The bracket will be created and the tournament's status will shift to Bracket Posted. Owners who wish to manually create a bracket can do so by using the <a>`/create-bracket`</a> Command.</p>

<h2>Starting a Tournament</h2>
<p>Once the bracket has been posted, the owner can start the tournament using the <a>`/start-tournament`</a> Command. The tournament status will change to In Progress and the first match will be posted for all preliminary games.</p>

<h2>Playing a Match</h2>
<p>Players can play their matches by using the <a>`/play-match`</a> Command. Once confirmed by at least two players, the match will be marked as complete and the winner will be advanced to the next round. The tournament status will be updated accordingly.</p>

<h2>Starting Next Round</h2>
<p>Once all matches in a round have been completed, the owner can start the next round using the <a>`/start-next-round`</a> Command. The tournament status will be updated accordingly.</p>

<h2>Set Round Results</h2>
<p>The owner can set the round results using the <a>`/set-round-results`</a> Command. This ends all active rounds. The tournament status will be updated accordingly.</p>

<h2>End Tournament</h2>
<p>The owner can end the tournament using the <a>`/end-tournament`</a> Command. The tournament status will be updated accordingly.</p>

<h2>Viewing Tournament Information</h2>
<p>Users can view the tournament information by using the <a>`/tournament-info`</a> Command. This will display the tournament's details, including the bracket, schedule, and player list.</p>

<h2>Viewing Tournament Results</h2>
<p>Users can view the tournament results by using the <a>`/tournament-results`</a> Command. This will display the tournament's results, including the winner, runner-up, and other participants.</p>