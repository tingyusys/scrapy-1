package com.itstar.tzplayer.provider;

import com.itstar.tzplayer.Bean.SongItem;
import ohos.agp.components.*;
import ohos.app.Context;
import ohos.eventhandler.InnerEvent;

import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class BannerProvider extends PageSliderProvider {
    private List<SongItem> items;
    private Context context;


    public BannerProvider(List<SongItem> items, Context context) {
        this.items = items;
        this.context = context;
    }

    @Override
    public int getCount() {
        return items.size();
    }

    @Override
    public Object createPageInContainer(ComponentContainer componentContainer, int i) {
        SongItem songItem = items.get(i);
        Image image = new Image(context);
        //设置图片的参数宽和高
        image.setLayoutConfig(new StackLayout.LayoutConfig(
                StackLayout.LayoutConfig.MATCH_PARENT,
                StackLayout.LayoutConfig.MATCH_PARENT
        ));
        //设置图片平铺Image.等等....
        image.setScaleMode(Image.ScaleMode.CLIP_CENTER);
        image.setCornerRadius(40);
        image.setMarginsLeftAndRight(60,60);
        image.setMarginsTopAndBottom(10,10);
        //加载图片数据
        image.setPixelMap(songItem.getPhoto_resource());
        //将image组件加入布局
        StackLayout sl = new StackLayout(context);
        sl.setLayoutConfig(new StackLayout.LayoutConfig(
                StackLayout.LayoutConfig.MATCH_PARENT,
                StackLayout.LayoutConfig.MATCH_PARENT
        ));
        sl.addComponent(image);
        componentContainer.addComponent(sl);

        return sl;
    }

    @Override
    public void destroyPageFromContainer(ComponentContainer componentContainer, int i, Object o) {
        //滑出屏幕的组件移除
        componentContainer.removeComponent((Component) o);
    }

    @Override
    public boolean isPageMatchToObject(Component component, Object o) {
        //判断滑页上的每一页组件和内容是否保持一致
        return component == o;
    }

}
