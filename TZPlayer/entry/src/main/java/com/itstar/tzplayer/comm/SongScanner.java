package com.itstar.tzplayer.comm;

import ohos.app.Context;
import ohos.media.photokit.common.AVLoggerConnectionClient;
import ohos.media.photokit.metadata.AVLoggerConnection;
import ohos.utils.net.Uri;

public class SongScanner implements AVLoggerConnectionClient {
    private AVLoggerConnection scanConn;
    private SongScanner(Context context) {
        // 实例化
        scanConn = new AVLoggerConnection(context, this);
        scanConn.connect();
    }
    public static void scan_sd(Context context){
        SongScanner songScanner = new SongScanner(context);
    }

    @Override
    public void onLoggerConnected() {
        String path = "/sdcard/Download";
        String mimeType = "mp3/Audio/m4a";
        scanConn.performLoggerFile(path, mimeType); // 服务回调执行扫描，指定要扫描的路径和文件类型
    }

    @Override
    public void onLogCompleted(String path, Uri uri) {
        // 回调函数返回扫描到的URI和path的值
        System.out.println(path);
        scanConn.disconnect(); // 断开扫描服务
    }
}
