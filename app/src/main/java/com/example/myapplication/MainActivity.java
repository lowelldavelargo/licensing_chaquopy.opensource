package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.ByteArrayOutputStream;

public class MainActivity extends AppCompatActivity {

    Button btn;
    TextView tv;
    ImageView iv,iv1;

    BitmapDrawable drawable;
    Bitmap bitmap;
    String imageString = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btn = (Button)findViewById(R.id.btn);
        tv = (TextView)findViewById(R.id.text_view);
        iv = (ImageView)findViewById(R.id.image_view);
        iv1 = (ImageView)findViewById(R.id.image_view1);
        if(!Python.isStarted())
            Python.start(new AndroidPlatform(this));

        final Python py = Python.getInstance();
        PyObject pyobj = py.getModule("script");

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                drawable = (BitmapDrawable)iv.getDrawable();
                bitmap = drawable.getBitmap();
                imageString = getImageString(bitmap);
                PyObject obj = pyobj.callAttr("main",imageString);
                String str = obj.toString();
                byte data[] = android.util.Base64.decode(str,Base64.DEFAULT);
                Bitmap bmp = BitmapFactory.decodeByteArray(data, 0,data.length);
                iv1.setImageBitmap(bmp);
                PyObject obj1 = pyobj.callAttr("main1",imageString);
                tv.setText(obj1.toString());


            }
        });


    }
    private String getImageString(Bitmap bitmap){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100,baos);
        byte[]imageBytes = baos.toByteArray();
        String encodedImage = android.util.Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;
    }
}