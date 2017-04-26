package nhl.nhlodds;

public class GameEntity {
    public String team1_name;
    public int team1_logo;
    public int team2_name;
    public int team2_logo;

    public GameEntity (String team1_name, int team1_logo, int team2_name, int team2_logo) {
        this.team1_name = team1_name;
        this.team1_logo = team1_logo;
        this.team2_name = team2_name;
        this.team2_logo = team2_logo;
    }
}
