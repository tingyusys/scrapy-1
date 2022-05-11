package com.itstar.tzplayer.slice;

import com.itstar.tzplayer.Bean.SongItem;
import com.itstar.tzplayer.ResourceTable;
import com.itstar.tzplayer.comm.TZHandler;
import com.itstar.tzplayer.provider.BannerProvider;
import ohos.aafwk.ability.AbilitySlice;
import ohos.aafwk.content.Intent;
import ohos.aafwk.content.Operation;
import ohos.agp.components.Component;
import ohos.agp.components.Image;
import ohos.agp.components.PageSlider;
import ohos.agp.window.service.WindowManager;
import ohos.eventhandler.EventHandler;
import ohos.eventhandler.EventRunner;
import ohos.eventhandler.InnerEvent;
import ohos.multimodalinput.event.TouchEvent;

import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

import static ohos.multimodalinput.event.TouchEvent.*;

public class MainAbilitySlice extends AbilitySlice {
    private Timer timer = null;
    private TimerTask timerTask = null;
    private ArrayList<SongItem> banner_items;
    private TZHandler tzHandler;
    @Override
    public void onStart(Intent intent) {
        super.onStart(intent);
        super.setUIContent(ResourceTable.Layout_ability_main);
        getWindow().addFlags(WindowManager.LayoutConfig.MARK_TRANSLUCENT_STATUS);
        init_banner();
        load_page();
    }

    private void load_page() {
        Image btn = (Image) findComponentById(ResourceTable.Id_song_load_icon);
        btn.setClickedListener(component ->{
            Intent intent = new Intent();
            Operation operation = new Intent.OperationBuilder()
                    .withDeviceId("")
                    .withBundleName("com.itstar.tzplayer")
                    .withAbilityName(".LoadAbility")
                    .build();
            intent.setOperation(operation);
            startAbility(intent);
        });
    }

    private void init_banner() {
        PageSlider banner = (PageSlider) findComponentById(ResourceTable.Id_banner);
        //初始化banner图里面的数据
        banner_items = new ArrayList<>();
        SongItem item1 = new SongItem();
        SongItem item2 = new SongItem();
        SongItem item3 = new SongItem();
        //如果加载网络图片则需要联网
        if (item1.getPhoto_resource() == 0) {
            //加载网络图片
        }else{
            item1.setPhoto_resource(ResourceTable.Media_album1);
        }
        item2.setPhoto_resource(ResourceTable.Media_album2);
        item3.setPhoto_resource(ResourceTable.Media_album3);
        banner_items.add(item1);
        banner_items.add(item2);
        banner_items.add(item3);
        //加载数据
        BannerProvider bannerProvider = new BannerProvider(banner_items, this);
        banner.setProvider(bannerProvider);
        banner.setCircularModeEnabled(true);
        //设置投递事件的eventHandler
        EventRunner runner = EventRunner.create();
        tzHandler = new TZHandler(runner, this, banner);
        startTask();
        banner.setTouchEventListener(new Component.TouchEventListener() {
            @Override
            public boolean onTouchEvent(Component component, TouchEvent touchEvent) {
                int action = touchEvent.getAction();
                if(action  == PRIMARY_POINT_DOWN){
                    //如果手指按下则,停止轮播
                    stopTask();
                }else if (action == PRIMARY_POINT_UP || action ==CANCEL || action == NONE){
                    //启动轮播
                    startTask();
                }
                return true;
            }
        });
    }

    @Override
    public void onActive() {
        super.onActive();
    }

    @Override
    public void onForeground(Intent intent) {
        super.onForeground(intent);
    }

    //启动Banner
    private void startTask(){
        stopTask();
        timerTask = new TimerTask() {
            @Override
            public void run() {
                //执行滚动图片的方法
                InnerEvent innerEvent = InnerEvent.get(1, banner_items.size());
                tzHandler.sendEvent(innerEvent, EventHandler.Priority.IMMEDIATE);
            }
        };
        timer = new Timer();
        timer.schedule(timerTask,1000,3000);
    }
    //停止Banner
    private void stopTask(){
        if (timer!=null && timerTask !=null){
            timer.cancel();
            timer = null;
            timerTask = null;
        }
    }
}
