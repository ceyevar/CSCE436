package nhl.nhlodds;

import android.os.AsyncTask;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Database extends AsyncTask<String, Void, String> {
    public AsyncResponse delegate = null;
    private String query = null;

    public interface AsyncResponse {
        void processFinish(String output);
    }

    public Database(AsyncResponse delegate, String query){
        this.delegate = delegate;
        this.query = query;
    }

    @Override
    public String doInBackground(String... userInput) {
        try {
            Socket s = new Socket("ec2-54-81-59-253.compute-1.amazonaws.com", 5432);
            PrintWriter out = new PrintWriter(s.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));

            out.println(query);
            String result = in.readLine();
            s.close();
            return result;
        }
        catch (IOException e) {
            System.out.print("CONNECTION FAILED: printing stack trace.");
            e.printStackTrace();
        }

        return "";
    }

    @Override
    protected void onPostExecute(String result) {
        delegate.processFinish(result);
    }
}