package nhl.nhlodds;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.Arrays;
import java.util.List;

public class TeamSelection extends AppCompatActivity implements Database.AsyncResponse {
    public List<String> teams, abbreviations;
    public Team selected_team = new Team();

    private String games_played_query, wins_query, losses_query, overtime_losses_query, rank_query, points_query, streak_query, elo_query, probability_query;

    public void ExecuteQueries() {
        new Database(TeamSelection.this, games_played_query).execute();
        new Database(TeamSelection.this, wins_query).execute();
        new Database(TeamSelection.this, losses_query).execute();
        new Database(TeamSelection.this, overtime_losses_query).execute();
        new Database(TeamSelection.this, rank_query).execute();
        new Database(TeamSelection.this, points_query).execute();
        new Database(TeamSelection.this, streak_query).execute();
        new Database(TeamSelection.this, elo_query).execute();
        new Database(TeamSelection.this, probability_query).execute();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_team_selection);

        teams = Arrays.asList(getResources().getStringArray(R.array.teams));
        abbreviations = Arrays.asList(getResources().getStringArray(R.array.abbreviations));

        final Button start_button = (Button)findViewById(R.id.start_button);
        start_button.setVisibility(View.GONE);

        final ProgressBar progress_bar = (ProgressBar) findViewById(R.id.progress_bar);
        progress_bar.setVisibility(View.GONE);

        final ArrayAdapter team_adapter = ArrayAdapter.createFromResource(this, R.array.teams, R.layout.team_spinner);
        team_adapter.setDropDownViewResource(R.layout.team_spinner_dropdown);
        final Spinner team_spinner = (Spinner) findViewById(R.id.team_spinner);
        team_spinner.setAdapter(team_adapter);
        team_spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                start_button.setVisibility(View.GONE);
                progress_bar.setVisibility(View.VISIBLE);

                selected_team.clear();
                selected_team.set_name(parent.getItemAtPosition(position).toString());
                selected_team.set_abbreviation(abbreviations.get(teams.indexOf(selected_team.get_name())));
                selected_team.set_logo(teams.indexOf(selected_team.get_name()));

                games_played_query = ";current_standings;games_played;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                wins_query = ";current_standings;wins;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                losses_query = ";current_standings;losses;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                overtime_losses_query = ";current_standings;overtime;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                rank_query = ";current_standings;current_ranking;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                points_query = ";current_standings;points;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                streak_query = ";current_standings;streak;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                elo_query = ";current_standings;elo;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                probability_query = ";current_standings;playoff_probability;name_abbreviation='" + selected_team.get_abbreviation() + "'";
                ExecuteQueries();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });

        start_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent stats = new Intent(TeamSelection.this, Stats.class);
                stats.putExtra("selected_team", selected_team);

                TeamSelection.this.startActivity(stats);
            }
        });
    }

    @Override
    public void processFinish(String output) {
        final ProgressBar progress_bar = (ProgressBar) findViewById(R.id.progress_bar);
        final Button start_button = (Button) findViewById(R.id.start_button);

        output = output.replace("(","");
        output = output.replace(")","");
        output = output.replace(",","");
        output = output.replace("'","");

        if (selected_team.get_games_played().equals("")) {
            selected_team.set_games_played(output);
        }
        else if (selected_team.get_wins().equals("")) {
            selected_team.set_wins(output);
        }
        else if (selected_team.get_losses().equals("")) {
            selected_team.set_losses(output);
        }
        else if (selected_team.get_losses().length() < 4) {
            selected_team.set_losses(selected_team.get_losses() + "-" + output);
        }
        else if (selected_team.get_rank().equals("")) {
            selected_team.set_rank(output);
        }
        else if (selected_team.get_points().equals("")) {
            selected_team.set_points(output);
        }
        else if (selected_team.get_streak().equals("")) {
            selected_team.set_streak(output);
        }
        else if (selected_team.get_elo().equals("")) {
            selected_team.set_elo(output);
        }
        else if (selected_team.get_probability().equals("")) {
            selected_team.set_probability(output);
            progress_bar.setVisibility(View.GONE);
            start_button.setVisibility(View.VISIBLE);
        }
    }
}