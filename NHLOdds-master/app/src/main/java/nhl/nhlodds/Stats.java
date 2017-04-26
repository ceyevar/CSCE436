package nhl.nhlodds;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

import it.moondroid.coverflow.components.ui.containers.FeatureCoverFlow;

public class Stats extends ActionBarActivity {
    public Team selected_team = new Team();
    public String team, abbreviation, games_played, wins, losses, rank, points, streak;
    public int logo;

    private String games_played_query, wins_query, losses_query, overtime_losses_query, rank_query, points_query, streak_query;

    int logos[] = { R.mipmap.ana, R.mipmap.phx, R.mipmap.bos, R.mipmap.buf, R.mipmap.cgy, R.mipmap.car, R.mipmap.chi, R.mipmap.col, R.mipmap.cbj, R.mipmap.dal,
                    R.mipmap.det, R.mipmap.edm, R.mipmap.fla, R.mipmap.lak, R.mipmap.min, R.mipmap.mtl, R.mipmap.nsh, R.mipmap.njd, R.mipmap.nyi, R.mipmap.nyr,
                    R.mipmap.ott, R.mipmap.phi, R.mipmap.pit, R.mipmap.stl, R.mipmap.sjs, R.mipmap.tbl, R.mipmap.tor, R.mipmap.van, R.mipmap.wsh, R.mipmap.wpg};

    private FeatureCoverFlow mCoverFlow;
    private CoverFlowAdapter mAdapter;
    private ArrayList<GameEntity> mData = new ArrayList<>(0);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stats);

        selected_team = getIntent().getParcelableExtra("selected_team");

        final ImageView team_logo = (ImageView) findViewById(R.id.team_logo);
        team_logo.setImageResource(logos[selected_team.get_logo()]);

        final TextView team_name = (TextView) findViewById(R.id.team_name);
        team_name.setText(selected_team.get_name());

        final TextView gp = (TextView) findViewById(R.id.gp);
        gp.setText(selected_team.get_games_played());

        final TextView w = (TextView) findViewById(R.id.w);
        w.setText(selected_team.get_wins());

        final TextView l_otl = (TextView) findViewById(R.id.l_otl);
        l_otl.setText(selected_team.get_losses());

        final TextView rnk = (TextView) findViewById(R.id.rnk);
        rnk.setText(selected_team.get_rank());

        final TextView p = (TextView) findViewById(R.id.p);
        p.setText(selected_team.get_points());

        final TextView strk = (TextView) findViewById(R.id.strk);
        strk.setText(selected_team.get_streak());

        final TextView elo = (TextView) findViewById(R.id.elo);
        elo.setText(selected_team.get_elo());

        final TextView prob = (TextView) findViewById(R.id.prob);
        prob.setText(selected_team.get_probability());

        mData.add(new GameEntity(selected_team.get_abbreviation(), logos[selected_team.get_logo()], R.string.team1_name, R.mipmap.buf));
        mData.add(new GameEntity(selected_team.get_abbreviation(), logos[selected_team.get_logo()], R.string.team2_name, R.mipmap.buf));
        mData.add(new GameEntity(selected_team.get_abbreviation(), logos[selected_team.get_logo()], R.string.team3_name, R.mipmap.buf));
        mData.add(new GameEntity(selected_team.get_abbreviation(), logos[selected_team.get_logo()], R.string.team4_name, R.mipmap.buf));

        mAdapter = new CoverFlowAdapter(this);
        mAdapter.setData(mData);
        mCoverFlow = (FeatureCoverFlow) findViewById(R.id.coverflow);
        mCoverFlow.setAdapter(mAdapter);

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_coverflow_activity, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

}
