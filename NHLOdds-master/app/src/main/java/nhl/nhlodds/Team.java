package nhl.nhlodds;

import android.os.Parcel;
import android.os.Parcelable;

public class Team implements Parcelable {
    private String name, abbreviation, games_played, wins, losses, rank, points, streak, elo, probability;
    private int logo;

    public Team() {
        super();
    }

    public Team(Parcel parcel) {
        this.name = parcel.readString();
        this.abbreviation = parcel.readString();
        this.games_played = parcel.readString();
        this.wins = parcel.readString();
        this.losses = parcel.readString();
        this.rank = parcel.readString();
        this.points = parcel.readString();
        this.streak = parcel.readString();
        this.elo = parcel.readString();
        this.probability = parcel.readString();
        this.logo = parcel.readInt();
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeString(this.name);
        parcel.writeString(this.abbreviation);
        parcel.writeString(this.games_played);
        parcel.writeString(this.wins);
        parcel.writeString(this.losses);
        parcel.writeString(this.rank);
        parcel.writeString(this.points);
        parcel.writeString(this.streak);
        parcel.writeString(this.elo);
        parcel.writeString(this.probability);
        parcel.writeInt(this.logo);
    }

    public static final Creator<Team> CREATOR=new Creator<Team>() {
        @Override
        public Team createFromParcel(Parcel parcel) {
            return new Team(parcel);
        }

        @Override
        public Team[] newArray(int i){
            return new Team[i];
        }
    };

    public void clear() {
        name = abbreviation = games_played = wins  = losses = rank = points = streak = elo = probability = "";
        logo = -1;
    }

    public void set_logo (int i) { logo = i; }
    public void set_name (String s) { name = s; }
    public void set_abbreviation (String s) { abbreviation = s; }
    public void set_games_played (String s) { games_played = s; }
    public void set_wins(String s) { wins = s; }
    public void set_losses(String s) { losses = s; }
    public void set_rank (String s) { rank = s; }
    public void set_points (String s) { points = s; }
    public void set_streak (String s) { streak = s; }
    public void set_elo (String s) { elo = s; }
    public void set_probability (String s) { probability = s; }


    public int get_logo() { return logo; }
    public String get_name() { return name; }
    public String get_abbreviation() { return abbreviation; }
    public String get_games_played() { return games_played; }
    public String get_wins() { return wins; }
    public String get_losses() { return losses; }
    public String get_rank() { return rank; }
    public String get_points() { return points; }
    public String get_streak() { return streak; }
    public String get_elo() { return elo; }
    public String get_probability() { return probability; }
}




