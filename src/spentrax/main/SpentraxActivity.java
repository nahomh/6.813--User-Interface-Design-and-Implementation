package spentrax.main;

import android.app.Activity;
import android.os.Bundle;

public class SpentraxActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    //this works-nahoms
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }
}